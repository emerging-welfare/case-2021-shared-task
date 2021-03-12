import json
import random
import itertools
import argparse
import subprocess

class OneClusterModel():
    def __init__(self):
        pass
    
    def fit(self,train_data):  
        return
    
    def predict(self,test_data):
        """
        Takes test file (.json) and path for prediction outputs to be save in required format (.json).
        
        Predicts given sentences as single cluster.
        """
        
        predictions = test_data
        
        for idx,instance in enumerate(predictions):
            predictions[idx]['event_clusters'] = [predictions[idx]['sentence_no']]
        
        return predictions
                
def read(path):
    data = []
    with open(path,"r") as file:
        for instance in file:
            data.append(json.loads(instance))
    return data


def convert_to_sklearn_format(clusters):
    sentences = sorted(sum(clusters, []))
    labels = list(sentences)
    assert len(set(labels)) == len(labels)
    
    for i, cl in enumerate(clusters): 
        for e in cl: 
            labels[sentences.index(e)] = i

    return labels

def evaluate(goldfile,sysfile,results_file):
    """
    Uses scorch for evaluation. > https://github.com/LoicGrobol/scorch | pip install scorch
    
    Takes gold file path (.json), predicted file path (.json) and file name (.txt) to save the results.
    """
    gold = read(goldfile)
    sys = read(sysfile)

    gold_clusters = sum([[[str(idx)+"_"+str(event) for event in cluster] for cluster in doc["event_clusters"]] for idx,doc in enumerate(gold)],[])
    sys_clusters = sum([[[str(idx)+"_"+str(event) for event in cluster] for cluster in doc["event_clusters"]] for idx,doc in enumerate(sys)],[])

    gold_links = sum([list(itertools.combinations(cluster,2)) for cluster in gold_clusters],[])
    gold_events = [event for pair in gold_links for event in pair]

    sys_links = sum([list(itertools.combinations(cluster,2)) for cluster in sys_clusters],[])
    sys_events = [event for pair in sys_links for event in pair]

    with open("gold.json","w") as f:
        json.dump({"type":"graph","mentions":gold_events,"links":gold_links},f)
    with open("sys.json","w") as f:
        json.dump({"type":"graph","mentions":sys_events,"links":sys_links},f)
        
    subprocess.run(["scorch","gold.json","sys.json",results_file])
    subprocess.run(["rm","gold.json","sys.json"])
    
    print(open(results_file,"r").read())
    

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
    model = OneClusterModel()
    #Read training data.
    train_data = read(train_file)
    #Fit. 
    model.fit(train_data)
    
    #Read test data.
    test_data = read(test_file)
    #Predict and save your results in the required format to the given path (prediction_output_file).
    predictions = model.predict(test_data)
    
    #Saving the predictions in required format.
    with open(prediction_output_file,"w") as f:
        for doc in predictions:
            json.dump(doc,f)
            f.write("\n")
    
    evaluate(test_file,
             prediction_output_file,
             results_file)

if __name__ == "__main__":
    main(*vars(parse()).values())