import json
import itertools
import argparse
import subprocess

class OneClusterModel():
    def __init__(self):
        pass

    def fit(self,data):
        """
        Doesn't use the given data.
        Returns nothing.
        """
        return

    def predict(self,data):
        """
        Takes some data (.json) and makes predictions.
        Simply puts all sentences in a single cluster.
        """
        preds = []
        for idx,instance in enumerate(data):
            preds.append({"id":instance["id"], "pred_clusters": [instance['sentence_no']]})

        return preds

def read(path):
    """
    Reads the file from the given path (json file).
    Returns list of instance dictionaries.
    """
    data = []
    with open(path, "r", encoding="utf-8") as file:
        for instance in file:
            data.append(json.loads(instance))

    return data


def convert_to_scorch_format(docs, cluster_key="event_clusters"):
    # Merge all documents' clusters in a single list

    all_clusters = []
    for idx, doc in enumerate(docs):
        for cluster in doc[cluster_key]:
            all_clusters.append([str(idx) + "_" + str(sent_id) for sent_id in cluster])

    all_links = sum([list(itertools.combinations(cluster,2)) for cluster in all_clusters],[])
    all_events = [event for pair in all_links for event in pair]

    return all_links, all_events

def evaluate(goldfile, sysfile):
    """
    Uses scorch -a python implementaion of CoNLL-2012 average score- for evaluation. > https://github.com/LoicGrobol/scorch | pip install scorch
    Takes gold file path (.json), predicted file path (.json) and prints out the results.

	This function is the exact way the subtask3's submissions will be evaluated.
    """
    gold = read(goldfile)
    sys = read(sysfile)

    gold_links, gold_events = convert_to_scorch_format(gold)
    sys_links, sys_events = convert_to_scorch_format(sys, cluster_key="pred_clusters")

    with open("gold.json", "w") as f:
        json.dump({"type":"graph", "mentions":gold_events, "links":gold_links}, f)
    with open("sys.json", "w") as f:
        json.dump({"type":"graph", "mentions":sys_events, "links":sys_links}, f)

    subprocess.run(["scorch", "gold.json", "sys.json", "results.txt"])
    print(open("results.txt", "r").read())
    subprocess.run(["rm", "gold.json", "sys.json", "results.txt"])

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-train_file', '--train_file', required=True, help="The path to the training data json file")
    parser.add_argument('-prediction_output_file', '--prediction_output_file', required=True, help="The path to the prediction output json file")
    parser.add_argument('-test_file', '--test_file', required=False, help="The path to the test data json file")
    args = parser.parse_args()
    return args

def main(train_file,prediction_output_file,test_file=None):

    #Create model.
    model = OneClusterModel()

    #Read training data.
    train_data = read(train_file)

    #Fit.
    model.fit(train_data)

    # Predict train data so that we can evaluate our system
    train_predictions = model.predict(train_data)
    with open(prediction_output_file, "w", encoding="utf-8") as f:
        for doc in train_predictions:
            f.write(json.dumps(doc) + "\n")

    # Evaluate sys outputs and print results.
    evaluate(train_file, prediction_output_file)

    # If there is a test file provided, make predictions and write them to file.
    if test_file:
        # Read test data.
        test_data = read(test_file)
        # Predict and save your predictions in the required format.
        test_predictions = model.predict(test_data)
        with open("sample_submission.json", "w", encoding="utf-8") as f:
            for doc in test_predictions:
                f.write(json.dumps(doc) + "\n")

if __name__ == "__main__":
    args = parse()
    main(args.train_file, args.prediction_output_file, args.test_file)
