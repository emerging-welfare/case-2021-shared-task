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
        self.seed = choice(range(100))

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
        Takes tokens and makes predictions based on the seed and markov chain which was learnt in the fit() part.
        Returns the predictions.
        """
        random.seed(self.seed)

        predictions = []
        last_prediction = "O"
        for sent in tokens:
            lbls = []
            for token in sent:
                last_prediction = choice(list(self.transitions[last_prediction].keys()),
                                         p=list(self.transitions[last_prediction].values()))
                lbls.append(last_prediction)

            predictions.append(lbls)

        return predictions

def evaluate(gold,sys):
    """
    Takes goldfile (txt) and sysfile (txt) paths.
    Prints out the results on the terminal.
    The metric used is from CoNLL-2003 evaluation. Can be found at https://github.com/sighsmile/conlleval

    This function is the exact way the subtask4's submissions will be evaluated.
    """
    # combine all labels in single arrays.
    gold_labels = sum(read(gold)[1], [])
    sys_labels = sum(read(sys)[1], [])

    conll_evaluate(gold_labels,sys_labels)

def read(path, train=True):
    """
    Reads the file from the given path (txt file).
    Returns list tokens and list of labels if it is training file.
    Returns list of tokens if it is test file.
    """
    with open(path, 'r', encoding="utf-8") as f:
        data = f.read()

    if train:
        data = [[tuple(word.split('\t')) for word in instance.strip().split('\n')] for idx,instance in enumerate(data.split("SAMPLE_START\tO")) if len(instance)>1]
        tokens = [[tupl[0].strip() for tupl in sent] for sent in data]
        labels = [[tupl[1] for tupl in sent] for sent in data]
        return tokens,labels
    else:
        tokens = [[word for word in instance.strip().split('\n')] for idx,instance in enumerate(data.split("SAMPLE_START")) if len(instance)>1]
        return tokens, None

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-train_file', '--train_file', required=True, help="The path to the training data txt file")
    parser.add_argument('-prediction_output_file', '--prediction_output_file', required=True, help="The path to the prediction output txt file")
    parser.add_argument('-test_file', '--test_file', required=False, help="The path to the test data txt file")
    args = parser.parse_args()
    return args

def main(train_file, prediction_output_file, test_file=None):

    #Create model.
    model = RandomModel()

    #Read training data.
    train_tokens, train_labels = read(train_file)

    #Fit.
    model.fit(train_tokens, train_labels)

    # Predict train data so that we can evaluate our system
    train_predictions = model.predict(train_tokens)
    with open(prediction_output_file, "w", encoding="utf-8") as f:
        for tokens, labels in zip(train_tokens, train_predictions):
            f.write("SAMPLE_START\tO\n")
            for token,label in zip(tokens,labels):
                f.write("{}\t{}\n".format(token,label))
            f.write("\n")

    # Evaluate sys outputs and print results.
    evaluate(train_file, prediction_output_file)

    # If there is a test file provided, make predictions and write them to file.
    if test_file:
        # Read test data.
        test_tokens, _ = read(test_file, train=False)
        # Predict and save your predictions in the required format.
        test_predictions = model.predict(test_tokens)
        with open("sample_submission.txt", "w", encoding="utf-8") as f:
            for tokens,labels in zip(test_tokens,test_predictions):
                f.write("SAMPLE_START\tO\n")
                for token,label in zip(tokens,labels):
                    f.write("{}\t{}\n".format(token,label))
                f.write("\n")

if __name__ == "__main__":
    args = parse()
    main(args.train_file, args.prediction_output_file, args.test_file)
