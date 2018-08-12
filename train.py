from keras.callbacks import TerminateOnNaN, ModelCheckpoint, TensorBoard
from keras.models import load_model
import numpy
from random import shuffle
from os import path
from create_model import create_model

from tqdm import tqdm

DATA_FILE = "./data/balanced/training_data_balanced.npy"
MODEL_FILE_PATH = "./data/rhombus_ai.hdf5"


def init_callbacks():
    terminator = TerminateOnNaN()
    checkpointer = ModelCheckpoint("./data/checkpoints/model_{epoch:02d}_{val_acc:.2f}.hdf5", monitor="val_acc",
                                   save_best_only=True, save_weights_only=False, mode="max", period=1)
    tensorboard = TensorBoard(log_dir="./logs", histogram_freq=1, batch_size=32, write_graph=True, write_grads=True)
    return [terminator, checkpointer, tensorboard]


def load_data(DATA_FILE):
    data = numpy.load(DATA_FILE, encoding="bytes")
    shuffle(data)
    X = []
    Y = []
    for elem in tqdm(data):
        X.append(elem[0].reshape(elem[0].shape+(1,)))
        Y.append(elem[1])
    return numpy.array(X), numpy.array(Y)


def main():
    callbacks = init_callbacks()
    x_train, y_train = load_data(DATA_FILE)
    if not path.isfile(MODEL_FILE_PATH):
        create_model().save(MODEL_FILE_PATH)
    model = load_model(MODEL_FILE_PATH)
    model.fit(x_train, y_train, batch_size=32, epochs=1, verbose=1, callbacks=callbacks, validation_split=0.3,
              shuffle=True)


if __name__ == "__main__":
    main()
