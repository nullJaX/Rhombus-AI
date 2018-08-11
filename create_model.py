from os import path
from keras import Sequential
from keras.metrics import categorical_accuracy
from keras.layers import Conv2D, Dropout, MaxPooling2D, Flatten, Dense

IMG_HEIGHT = 180
IMG_WIDTH = 180
IMG_DEPTH = 1
MODEL_FILE_PATH = "./data/rhombus_ai.hdf5"
INPUT_SHAPE = (IMG_HEIGHT, IMG_WIDTH, IMG_DEPTH)


def main():
    if path.isfile(MODEL_FILE_PATH):
        print("Model already exists!")
    else:
        create_model().save(MODEL_FILE_PATH)


def create_model():
    model = Sequential()
    model.add(Conv2D(32, (7, 7), padding="same", activation="relu", input_shape=INPUT_SHAPE))
    model.add(Dropout(0.25))
    model.add(MaxPooling2D(padding="same"))
    model.add(Conv2D(64, (3, 3), padding="same", activation="relu"))
    model.add(Dropout(0.25))
    model.add(Conv2D(64, (3, 3), padding="same", activation="relu"))
    model.add(MaxPooling2D(padding="same"))
    model.add(Dropout(0.33))
    model.add(Conv2D(128, (3, 3), padding="same", activation="relu"))
    model.add(MaxPooling2D(padding="same", strides=3))
    model.add(Conv2D(512, (3, 3), padding="same", activation="relu"))
    model.add(MaxPooling2D(padding="same", strides=3))
    model.add(Flatten())
    model.add(Dropout(0.25))
    model.add(Dense(125, activation="relu"))
    model.add(Dropout(0.45))
    model.add(Dense(25, activation="relu"))
    model.add(Dense(5, activation="softmax"))
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=[categorical_accuracy, "accuracy"])
    model.summary()
    return model


if __name__ == "__main__":
    main()
