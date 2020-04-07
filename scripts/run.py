import argparse
import time

from surprise import (
    BaselineOnly,
    KNNBasic, KNNWithMeans, KNNWithZScore, KNNBaseline,
    SVD, SVDpp, NMF,
    SlopeOne,
    CoClustering
)
from surprise import Dataset, model_selection, accuracy
from surprise.dump import dump
from surprise.reader import Reader
from surprise.model_selection import cross_validate
from surprise.model_selection.validation import fit_and_score

parser = argparse.ArgumentParser(description='Train model.')
parser.add_argument('model', choices=['KNNBasic', 'KNNWithMeans', 'KNNWithZScore', 'KNNBaseline', 'SVD', 'SVDpp', 'NMF', 'SlopeOne', 'CoClustering'],
                    default='ml-100k', help='Model to use')
parser.add_argument('--dataset', '-d', dest='dataset', default='ml-100k',
                    choices=['ml-100k', 'ml-1m', 'ml-10m'],
                    help='dataset to be used')
parser.add_argument('--output', '-o', dest='filename', help='Model output file')
parser.add_argument('--fit-only', dest='fit_only', action='store_true')
parser.add_argument('--verbose', dest='verbose', action='store_true')

args = parser.parse_args()

def get_dataset(dataset_id):
    BUILTIN_DATASETS = {
        'ml-100k': {
            'path':'./ml-100k/u.data',
            'line_format': 'user item rating timestamp',
            'rating_scale': (1, 5),
            'sep':'\t'
        },
        'ml-1m': {
            'path':'./ml-1m/ratings.dat',
            'line_format': 'user item rating timestamp',
            'rating_scale': (1, 5),
            'sep':'::'
         },
        'ml-10m': {
            'path':'./ml-10M100K/ratings.dat',
            'line_format': 'user item rating timestamp',
            'rating_scale': (1, 5),
            'sep':'::'
        }
    }
    dataset_props = BUILTIN_DATASETS[dataset_id]
    return Dataset.load_from_file(
        dataset_props.get('path'),
        Reader(line_format=dataset_props.get('line_format'),
            rating_scale=dataset_props.get('rating_scale'),
            sep=dataset_props.get('sep')))

def fit(algo, trainset):
    start_fit = time.time()
    algo.fit(trainset)
    fit_time = time.time() - start_fit
    return fit_time

def score(algo, testset, measures):
    start_test = time.time()
    predictions = algo.test(testset)
    test_time = time.time() - start_test

    test_measures = dict()
    train_measures = dict()
    for m in measures:
        f = getattr(accuracy, m.lower())
        test_measures[m] = f(predictions)

    return test_measures, test_time


import sys
original_stdout = sys.stdout
sys.stdout = open('/tmp/stdout.txt', 'w')

dataset_id = args.dataset
model_class = args.model
fit_only = args.fit_only
filename = args.filename
if args.verbose:
    print("Dataset: %s", dataset_id, file=original_stdout)

start_loaddata = time.time()
data = get_dataset(dataset_id)
loaddata_time = time.time() - start_loaddata
if args.verbose:
    print('Data loaded: %s' % loaddata_time, file=original_stdout)

start_splitdata = time.time()
trainset,testset = model_selection.train_test_split(data)
splitdata_time = time.time() - start_splitdata
if args.verbose:
    print('Train test set created: %s' %splitdata_time, file=original_stdout)

model = eval(model_class)()
fit_time = fit(model, trainset)
if args.verbose:
    print('Fit time: %s' % fit_time, file=original_stdout)
if not fit_only:
    test_measures, test_time = score(model, testset, ['RMSE', 'MAE'])
    if args.verbose:
        print('Test time: %s' % test_time, file=original_stdout)
        print('RMSE: %s' % test_measures.get('RMSE'), file=original_stdout)
        print('MAE: %s' % test_measures.get('MAE'), file=original_stdout)

if filename:
    dump(filename, algo=model)
    if args.verbose:
        print('Model saved: %s' % filename, file=original_stdout)

sys.stdout = original_stdout
print(fit_time, test_time, test_measures.get('RMSE'), test_measures.get('MAE'), file=original_stdout)
