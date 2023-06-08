import argparse
import math
import pandas as pd
from pandas import DataFrame


def parseInput(argv):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('csv_filename',
                        help='Path to csv_file')
    parser.add_argument('train_file',
                        help='ARFF train filename',
                        default='train.arff')
    parser.add_argument('test_file',
                        help='ARFF test filename',
                        default='test.arff')
    return parser.parse_args(args=argv)


def get_valid_data(data: DataFrame):
    df_raw = delete_columns(data)
    df_discretized = discretize_variables(df_raw)
    return df_discretized


def discretize_variables(data: DataFrame):
    continuous_columns = ['normalized-losses', 'price']
    for col in continuous_columns:
        discretize_values(data, col)
    return data.copy(deep=True)


def discretize_values(data: DataFrame, column): # TODO
    """Discretize a value in same-size intervals"""
    print(data)
    df = pd.to_numeric(data[column], errors='coerce').dropna()
    size = (data.max() - data.min()) / 5
    return data


def delete_columns(data: DataFrame):
    columns = [
        'symboling',
        'normalized-losses',
        'make',
        'fuel-type',
        'aspiration',
        'num-of-doors',
        'body-style',
        'drive-wheels',
        'engine-location',
        'price'
    ]
    columns_to_delete = [header for header in list(data.columns) if header not in columns]
    return data.copy(deep=True).drop(columns=columns_to_delete)


def get_train_test_split(df: DataFrame, train_frac: float):
    ID_DIGITS = 57747
    N = math.floor(len(df) * train_frac)
    df.sample(frac=1, random_state=ID_DIGITS)
    train, test = df.iloc[:N], df.iloc[N:]
    print('Check missing samples?', len(df), '=', len(train) + len(test))
    return train, test


def main(argv=None):
    args = parseInput(argv)
    # train_file = open(args.train_file, 'w')
    # test_file = open(args.test_file, 'w')
    df_raw = pd.read_csv(args.csv_filename)
    df = get_valid_data(df_raw)
    # train, test = get_train_test_split(df, .75)
    # print(train)
    # print(test)


if __name__ == '__main__':
    main()
