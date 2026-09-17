import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    # print(load_data(sys.argv[1]))
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    # print(evaluate(y_test, predictions))
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # if data 'revenue' then add that to label else evidence (columns)
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        try:
            # data-processing loop
            evidence, labels = [], []
            months_labelencoder = {'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4,  # month label encoder
                                   'June': 5, 'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9,
                                   'Nov': 10, 'Dec': 11}
            weekend_labelencoder = {'TRUE': 1, 'FALSE': 0}
            returning_labelencoder = {'Returning_Visitor': 1, 'New_Visitor': 0, "Other": 0}
            revenue_labelencoder = {'TRUE': 1, 'FALSE': 0}
            for i, row in enumerate(reader):
                if i == 0:
                    # index column names to refer row index
                    columns = {column: index for index, column in enumerate(row)}
                    # print(columns)

                if 0 < i:  # cut out the column names
                    evidence.append(row[:-1])  # split evidence
                    labels.append(row[-1])  # split label
                    evidence[i-1][columns['Month']] = months_labelencoder[evidence[i-1]
                                                                          [columns['Month']]]  # convert months to int
                    evidence[i-1][columns['VisitorType']
                                  ] = returning_labelencoder[evidence[i-1][columns['VisitorType']]]
                    evidence[i-1][columns['Weekend']
                                  ] = weekend_labelencoder[evidence[i-1][columns['Weekend']]]
                    labels[i-1] = revenue_labelencoder[labels[i-1]]
                    for feature_index, feature in enumerate(evidence[i-1]):
                        if (
                            feature is evidence[i-1][columns['Administrative']] or
                            feature is evidence[i-1][columns['Informational']] or
                            feature is evidence[i-1][columns['ProductRelated']] or
                            feature is evidence[i-1][columns['Month']] or
                            feature is evidence[i-1][columns['OperatingSystems']] or
                            feature is evidence[i-1][columns['Browser']] or
                            feature is evidence[i-1][columns['Region']] or
                            feature is evidence[i-1][columns['TrafficType']] or
                            feature is evidence[i-1][columns['VisitorType']] or
                            feature is evidence[i-1][columns['Weekend']]
                        ):
                            evidence[i-1][feature_index] = int(feature)
                        elif (
                            feature is evidence[i-1][columns['Administrative_Duration']] or
                            feature is evidence[i-1][columns['Informational_Duration']] or
                            feature is evidence[i-1][columns['ProductRelated_Duration']] or
                            feature is evidence[i-1][columns['BounceRates']] or
                            feature is evidence[i-1][columns['ExitRates']] or
                            feature is evidence[i-1][columns['PageValues']] or
                            feature is evidence[i-1][columns['SpecialDay']]
                        ):
                            evidence[i-1][feature_index] = float(feature)

            return (evidence, labels)

            # print(evidence[1][columns['Month']], labels[1])

        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    tn, fp, fn, tp = confusion_matrix(labels, predictions).ravel()
    specificity = float(tn / (tn+fp))
    sensitivity = float(tp / (tp+fn))

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
