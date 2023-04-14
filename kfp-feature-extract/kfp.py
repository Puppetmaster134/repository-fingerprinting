from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import numpy as np

def rf_train(tr_data, tr_label, te_data, te_label, num_trees = 1000):
    '''Closed world RF classification of data -- only uses sk.learn classification - does not do additional k-nn.'''
    print("Training...")
    model = RandomForestClassifier(n_jobs=2, n_estimators=num_trees, oob_score = True)
    model.fit(tr_data, tr_label)
    predictions = model.predict(te_data)
    accuracy = sum(predictions == te_label) / len(te_label)
    print(f"RF accuracy = {accuracy}")

    #print "Feature importance scores:"
    #print model.feature_importances_

    scores = cross_val_score(model, np.array(tr_data), np.array(tr_label))
    print(f"Cross Validation: {scores.mean()}")
    #print "OOB score = ", model.oob_score_(tr_data, tr_label)

    return accuracy, predictions

if __name__ == '__main__':
    pass