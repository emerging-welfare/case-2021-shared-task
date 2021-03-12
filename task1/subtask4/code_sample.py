from numpy.random import choice
import random
import argparse
from conlleval import evaluate as conll_evaluate # https://github.com/sighsmile/conlleval

class RandomModel():
    def __init__(self):
        pass
    
    def fit(self,tokens,labels):
        """
        Learns the seed for future prediction and markov chain of states (O, B-etime, I-etime, etc.).
        """
        self.seed = random.choice(range(100))
        
        self.transitions = {label: {label:0 for label in set(sum(labels,[]))} for label in set(sum(labels,[]))}
        for sent in labels:
            for idx,label in enumerate(sent[:-1]):
                    self.transitions[label][sent[idx+1]] += 1

        for label in self.transitions:
            sumOfAll = sum(self.transitions[label].values())
            for l in self.transitions[label]:
                self.transitions[label][l] = round(self.transitions[label][l]/sumOfAll,2)
                
    def predict(self,tokens):
        """
        Reads the test file and makes predictions based on the seed and markov chain which was learnt in the fit() part.
        Returns the predictions.
        """
        random.seed(self.seed)
        
        labels = []
        last_prediction = "O"
        for sent in tokens:
            lbls = []
            for token in sent:
                last_prediction = choice(list(self.transitions[last_prediction].keys()),
                                         p=list(self.transitions[last_prediction].values()))
                lbls.append(last_prediction)
                    
            labels.append(lbls)
        return labels
    
def evaluate(gold,sys,results_file):
    """
    conll 2003 evaluation will be here.
    should save the results!
    """
    gold_labels = sum(read(gold)[1],[])
    sys_labels = sum(read(sys)[1],[])
    
    # This should be replaced by CONLL2003_NER_EVALUATION script
    conll_evaluate(gold_labels,sys_labels) # https://github.com/sighsmile/conlleval
    

def read(path):
    """
    Reads the file from the given path (.txt file).
    Returns list tokens and list of labels if it is training file.
    Returns list of tokens if it is test file.
    """
    try:
        with open(path,'r') as r:
            data = r.read()
            data = [[tuple(word.split('\t')) for word in instance.strip().split('\n')] for idx,instance in enumerate(data.split("SAMPLE_START\tO")) if len(instance)>1]
            tokens = [[tupl[0] for tupl in sent] for sent in data]
            labels = [[tupl[1] for tupl in sent] for sent in data]
            return tokens,labels
    except:
        with open(path,'r') as r:
            tokens = [[word for word in instance.strip().split('\n')] for idx,instance in enumerate(r.read().split("SAMPLE_START")) if len(instance)>1]
            return tokens,None
    
def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-train_file','--train_file', required=True)
    parser.add_argument('-test_file','--test_file',required=False)
    parser.add_argument('-prediction_output_file','--prediction_output_file',required=False)
    parser.add_argument('-results_output_file','--results_output_file', required=False)

    args = parser.parse_args()
    return args

def main(train_file,test_file,prediction_output_file,results_file):
    
    #Create model.
    model = RandomModel()
    
    #Read training data.
    tokens,labels = read(train_file)
    #Fit. 
    model.fit(tokens,labels)

    #Read test data.
    test_tokens,_ = read(test_file)
    #Predict.
    test_labels = model.predict(test_tokens)
    
    #Save in required format.
    with open(prediction_output_file,"w") as f:
        for tokens,labels in zip(test_tokens,test_labels):
            f.write("SAMPLE_START\tO\n")
            for token,label in zip(tokens,labels):
                f.write(f"{token}\t{label}\n")
            f.write("\n")
    
    
    evaluate(test_file,
             prediction_output_file,
             results_file)

if __name__ == "__main__":
    main(*vars(parse()).values())