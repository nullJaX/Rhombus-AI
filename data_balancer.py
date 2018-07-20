import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
from tqdm import tqdm

LEVELS = ["EASY", "NORMAL", "HARD", "EXPERT"]
FILENAME_INPUT = "./data/capture/training_data_{}.npy"
FILENAME_OUTPUT = "./data/balanced/training_data_balanced.npy"


def main():
    final_data = []
    for level in tqdm(LEVELS):
        train_data = np.load(FILENAME_INPUT.format(level))
        df = pd.DataFrame(train_data)
        print(Counter(df[1].apply(str)))

        lefts = []
        rights = []
        ups = []
        downs = []
        spaces = []

        shuffle(train_data)

        for data in tqdm(train_data):
            img = data[0]
            choice = data[1]

            if choice == [1, 0, 0, 0, 0]:
                ups.append([img, choice])
            elif choice == [0, 1, 0, 0, 0]:
                lefts.append([img, choice])
            elif choice == [0, 0, 1, 0, 0]:
                downs.append([img, choice])
            elif choice == [0, 0, 0, 1, 0]:
                rights.append([img, choice])
            elif choice == [0, 0, 0, 0, 1]:
                spaces.append([img, choice])
            else:
                print('NO MATCHES!')
        shuffle(ups)
        shuffle(downs)
        shuffle(lefts)
        shuffle(rights)
        shuffle(spaces)
        min_length = np.min([len(ups), len(downs), len(lefts), len(rights), len(spaces)])
        ups = ups[:min_length]
        spaces = spaces[:min_length]
        downs = downs[:min_length]
        lefts = lefts[:min_length]
        rights = rights[:min_length]
        final_data.extend(ups)
        final_data.extend(downs)
        final_data.extend(lefts)
        final_data.extend(rights)
        final_data.extend(spaces)
        shuffle(final_data)
        np.save(FILENAME_OUTPUT, final_data)
    print(len(final_data))


if __name__ == '__main__':
    main()
