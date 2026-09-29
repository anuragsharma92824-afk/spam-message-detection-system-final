from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

from dataset import load_dataset, split_dataset


class SpamModel:

    def train_model(self):

        df = load_dataset()

        X_train, X_test, y_train, y_test = split_dataset(df)

        # Create vectorizer
        self.vectorizer = CountVectorizer()

        X_train_vectorized = self.vectorizer.fit_transform(X_train)
        X_test_vectorized = self.vectorizer.transform(X_test)

        # Create and train model
        self.model = MultinomialNB()

        self.model.fit(
            X_train_vectorized,
            y_train
        )

        # Test prediction
        y_pred = self.model.predict(
            X_test_vectorized
        )

        # Metrics
        self.accuracy = accuracy_score(
            y_test,
            y_pred
        )

        self.precision = precision_score(
            y_test,
            y_pred,
            zero_division=0
        )

        self.recall = recall_score(
            y_test,
            y_pred,
            zero_division=0
        )

        self.f1 = f1_score(
            y_test,
            y_pred,
            zero_division=0
        )

        self.confusion_matrix = confusion_matrix(
            y_test,
            y_pred
        )

    def get_metrics(self):

        # Directly train the model.
        # No dependency on _init_.
        self.train_model()

        return {
            "accuracy": self.accuracy,
            "precision": self.precision,
            "recall": self.recall,
            "f1": self.f1,
            "confusion_matrix": self.confusion_matrix
        }

    def predict(self, message):

        message_vectorized = self.vectorizer.transform(
            [message]
        )

        prediction = self.model.predict(
            message_vectorized
        )[0]

        if prediction == 1:
            return "Spam"

        return "Ham"