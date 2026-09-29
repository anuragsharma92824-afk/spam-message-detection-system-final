import pandas as pd
from sklearn.model_selection import train_test_split
from config import DATASET_FILE, TEST_SIZE, RANDOM_STATE


def load_dataset():
    data = []

    with open(DATASET_FILE, "r", encoding="utf-8", errors="replace") as file:
        for line in file:
            parts = line.rstrip("\n").split("\t", 1)

            if len(parts) == 2:
                label, message = parts

                if label == "spam":
                    label = 1
                elif label == "ham":
                    label = 0
                else:
                    continue

                data.append([message, label])

    df = pd.DataFrame(data, columns=["text", "label"])

    return df


def split_dataset(df):
    X = df["text"]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y
    )

    return X_train, X_test, y_train, y_test