import json
import random
import argparse
import pandas as pd
from sklearn.metrics import adjusted_rand_score, v_measure_score

class OneClusterModel():
    def __init__(self):
        pass
    
    def fit(self,train_file):  
        return
    
    def predict(self,test_file,prediction_output_file):
        """
        Takes test file (.json) and path for prediction outputs to be save in required format (.json).
        
        Predicts given sentences as single cluster.
        """
        
        data = read(test_file)
        
        for idx,instance in enumerate(data):
            data[idx]['event_clusters'] = [data[idx]['sentence_no']]
        with open(prediction_output_file,"w") as f:
            for doc in data:
                json.dump(doc,f)
                f.write("\n")
                
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
    gold_df = pd.read_json(goldfile, orient="records", lines=True)
    pred_df = pd.read_json(sysfile, orient="records", lines=True)

    gold_clusters = [convert_to_sklearn_format(g) for g in gold_df["event_clusters"]]
    pred_clusters = [convert_to_sklearn_format(p) for p in pred_df["event_clusters"]]
    
    ari_scores = [ adjusted_rand_score(g, p) for g, p in zip(gold_clusters, pred_clusters) ]
    macro_ari = sum(ari_scores) / len(gold_df)
    micro_ari = sum(s * len(c) for s, c in zip(ari_scores, gold_df["sentence_no"])) / sum(len(s) for s in gold_df["sentence_no"])
    
    v_scores = [ v_measure_score(g, p) for g, p in zip(gold_clusters, pred_clusters) ]
    macro_v = sum(v_scores) / len(gold_df)
    micro_v = sum(s * len(c) for s, c in zip(v_scores, gold_df["sentence_no"])) / sum(len(s) for s in gold_df["sentence_no"])
    results = "-"*40+"\n"+"\t"*3+"Macro\tMicro\n"+"-"*40+"\nAdjusted Rand Index:\t%.4f\t%.4f\n"%(macro_ari,micro_ari)+"-"*40+"\nF1 - Measure Score :\t%.4f\t%.4f"%(macro_v,micro_v)+"\n"+"-"*40
    print(results)
    with open(results_file,'w') as r:
        r.write(results)

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
    
    #Fit. 
    model.fit(train_file)
    
    #Predict and save your results in the required format to the given path (prediction_output_file).
    model.predict(test_file,prediction_output_file)
    
    evaluate(test_file,
             prediction_output_file,
             results_file)

if __name__ == "__main__":
    main(*vars(parse()).values())