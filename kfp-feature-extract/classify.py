import os
import numpy as np
from sklearn.model_selection import train_test_split
from kfp import rf_train

def load_features(folder):
    """
    """
    print(f'Loading features from {folder}')
    feature_vecs = []           # List of feature vectors.
    labels = []                 # List of labels (webpage ids).
    wid = []                    # List of webpage-load ids.

    files = [os.path.join(folder, x) for x in os.listdir(folder)]
    files = [x for x in files if x.endswith('.features')]

    for f in files:
        f_base = os.path.basename(f).replace('.features', '')
        # A file is considered only if its name is in the format
        # "page_id-load_id".
        page_id, load_id = f_base.split('-')
        f = np.genfromtxt(f, delimiter=',').reshape(1,-1)
        feature_vecs.append(f)
        labels.append(int(page_id))
        wid.append(f_base)


    X = np.vstack(feature_vecs)
    labels = np.array(labels)
    n_pages = len(set(labels))
    n_loads = -1

    print(f'Loaded {n_pages} pages, {n_loads} loads each')
    print(f'Number of objects: {len(X)}')
    print(f'Length of a feature vector: {X.shape[1]}')

    return X, labels, wid, n_pages, n_loads


def main():
    test_size = 0.05
    seed = 1
    feature_dir = './out'

    X,Y,_,n_pages, n_loads = load_features(feature_dir)
    n = len(X)
    n_test = int(n * test_size)
    n_train = n - n_test
    print(f'Training set size: {n_train}. Test set size: {n_test}.')
    print('Splitting into training/test set keeping uniform labels')
    I = range(n) # Indexes
    Itrain, Itest = train_test_split(I, test_size=test_size, stratify=Y, random_state = seed)
    Xtest = X[Itest,:]
    Ytest = Y[Itest]
    Xtrain = X[Itrain,:]
    Ytrain = Y[Itrain]

    for num_trees in [20, 50, 100, 500, 1000, 5000]:
        result = rf_train(Xtrain,Ytrain,Xtest,Ytest,num_trees=num_trees)
        print(f"Results[{num_trees}]: {result}")

if __name__ == "__main__":
    main()