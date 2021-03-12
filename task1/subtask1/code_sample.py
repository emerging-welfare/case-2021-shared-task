import json
import random
import argparse
from sklearn.metrics import precision_recall_fscore_support

class RandomModel():
    def __init__(self):
        pass

    def fit(self,data):
        """
        Learns the seed for future prediction.
        Doesn't use the given data.
        """
        self.seed = random.choice(range(100))


    def predict(self,test_data):
        """
        Takes some data and makes predictions based on the seed which was learnt in the fit() part.
        Returns the predictions.
        """
        random.seed(self.seed)
        preds = [{"id":instance['id'], "prediction":random.choice([0,1])} for instance in test_data]
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


def evaluate(goldfile, sysfile):
    """
    Takes goldfile (json) and sysfile (json) paths.
    Prints out the results on the terminal.
    The metric used is F1-Macro implementation from sklearn library (Its documentation is at https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html).

    This function is the exact way the subtask1's submissions will be evaluated.
    """
    gold = {i["id"]:i["label"] for i in read(goldfile)}
    sys = {i["id"]:i["prediction"] for i in read(sysfile)}

    labels, preds = [], []
    for idx in gold:
        labels.append(gold[idx])
        preds.append(sys[idx])

    precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(labels, preds, labels=[0,1], average="macro")
    print("F1-macro score for test data predictions are: %.4f" %f1_macro)

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-train_file', '--train_file', required=True, help="The path to the training data json file")
    parser.add_argument('-prediction_output_file', '--prediction_output_file', required=True, help="The path to the prediction output json file")
    parser.add_argument('-test_file', '--test_file', required=False, help="The path to the test data json file")
    args = parser.parse_args()
    return args

def main(train_file, prediction_output_file, test_file=None):

    # Create model.
    model = RandomModel()

    # Read training data.
    train_data = read(train_file)

    # Fit.
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
