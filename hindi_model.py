import pandas as pd
import re

from sklearn.model_selection import train_test_split
from sklearn.pipeline import FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


class HindiSpamModel:

    # ==================================================
    # TRAIN MODEL
    # ==================================================

    def train_model(self):

        # Load Hindi dataset
        df = pd.read_csv("hindi_spam.csv")

        # Clean message column
        df["message"] = (
            df["message"]
            .fillna("")
            .astype(str)
        )

        # Clean label column
        df["label"] = (
            df["label"]
            .fillna("")
            .astype(str)
            .str.lower()
            .str.strip()
        )

        # Keep only ham and spam
        df = df[
            df["label"].isin(
                ["ham", "spam"]
            )
        ].copy()

        X = df["message"]
        y = df["label"]

        # Train / Test split
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
            stratify=y
        )

        # ==================================================
        # WORD + CHARACTER TF-IDF
        # ==================================================

        self.vectorizer = FeatureUnion([

            (
                "word",

                TfidfVectorizer(
                    ngram_range=(1, 2),
                    min_df=1,
                    sublinear_tf=True,
                    max_features=60000
                )
            ),

            (
                "char",

                TfidfVectorizer(
                    analyzer="char",
                    ngram_range=(2, 5),
                    min_df=1,
                    sublinear_tf=True,
                    max_features=80000
                )
            )

        ])

        # Convert training messages
        X_train_vectorized = (
            self.vectorizer.fit_transform(
                X_train
            )
        )

        # Convert test messages
        X_test_vectorized = (
            self.vectorizer.transform(
                X_test
            )
        )

        # ==================================================
        # LINEAR SVM
        # ==================================================

        self.model = LinearSVC(
            class_weight="balanced",
            C=1.5
        )

        # Train
        self.model.fit(
            X_train_vectorized,
            y_train
        )

        # Test prediction
        y_pred = self.model.predict(
            X_test_vectorized
        )

        # ==================================================
        # METRICS
        # ==================================================

        self.accuracy = accuracy_score(
            y_test,
            y_pred
        )

        self.precision = precision_score(
            y_test,
            y_pred,
            pos_label="spam",
            zero_division=0
        )

        self.recall = recall_score(
            y_test,
            y_pred,
            pos_label="spam",
            zero_division=0
        )

        self.f1 = f1_score(
            y_test,
            y_pred,
            pos_label="spam",
            zero_division=0
        )

        self.confusion_matrix = confusion_matrix(
            y_test,
            y_pred,
            labels=[
                "ham",
                "spam"
            ]
        )

    # ==================================================
    # GET METRICS
    # ==================================================

    def get_metrics(self):

        self.train_model()

        return {

            "accuracy":
                self.accuracy,

            "precision":
                self.precision,

            "recall":
                self.recall,

            "f1":
                self.f1,

            "confusion_matrix":
                self.confusion_matrix

        }

    # ==================================================
    # ML PREDICTION
    # ==================================================

    def predict_ml(self, message):

        message_vectorized = (
            self.vectorizer.transform(
                [message]
            )
        )

        result = self.model.predict(
            message_vectorized
        )[0]

        return result

    # ==================================================
    # HINDI SPAM RULE CHECK
    # ==================================================

    def rule_check(self, message):

        text = message.lower().strip()

        patterns = [

            # Prize / reward
            r"\bइनाम\b",
            r"\bप्राइज़\b",
            r"\bप्राइज\b",
            r"\bprize\b",

            # Claim
            r"\bclaim\b",
            r"\bक्लेम\b",

            # Click
            r"\bclick\b",
            r"\bक्लिक\b",

            # OTP
            r"\botp\b",
            r"\bओटीपी\b",

            # Password
            r"\bpassword\b",
            r"\bपासवर्ड\b",

            # Verification
            r"\bverify\b",
            r"\bverification\b",
            r"\bवेरिफाइ\b",
            r"\bसत्यापित\b",

            # Account blocked
            r"\bअकाउंट\b.*\bबंद\b",
            r"\bअकाउंट\b.*\bब्लॉक\b",

            r"\baccount\b.*\bblocked\b",
            r"\baccount\b.*\bverify\b",
            r"\baccount\b.*\bबंद\b",

            # Free mobile
            r"\bफ्री\b.*\bमोबाइल\b",
            r"\bfree\b.*\bmobile\b",

            # Money
            r"\bपैसे\b.*\bजीते\b",
            r"\bपैसे\b.*\bमिले\b",
            r"\bपैसे\b.*\bजमा\b",

            # Specific money pattern
            r"\b5000\b.*\bजमा\b",
            r"\b5000\b.*\bमिले\b",

            # Link
            r"\bलिंक\b.*\bक्लिक\b",
            r"\bलिंक\b.*\bखोल\b",

            r"\blink\b.*\bclick\b",
            r"\blink\b.*\bopen\b",

            # Urgency
            r"\bअभी\b.*\bक्लिक\b",
            r"\bतुरंत\b.*\bverify\b",
            r"\bतुरंत\b.*\botp\b"

        ]

        matched_patterns = []

        for pattern in patterns:

            if re.search(
                pattern,
                text,
                re.IGNORECASE
            ):

                matched_patterns.append(
                    pattern
                )

        if matched_patterns:

            return True

        return False

    # ==================================================
    # FINAL PREDICTION
    # ==================================================

    def predict(self, message):

        # ML result
        ml_result = self.predict_ml(
            message
        )

        # Rule result
        rule_spam = self.rule_check(
            message
        )

        # Strong spam indicator found
        if rule_spam:

            return "spam"

        # Otherwise use ML result
        return ml_result


# ======================================================
# MAIN TEST PROGRAM
# ======================================================

if __name__ == "__main__":

    print()
    print("==========================================")
    print("       HINDI SPAM DETECTION SYSTEM")
    print("==========================================")

    print()
    print(
        "Loading dataset and training model..."
    )

    print()

    # Create model
    model = HindiSpamModel()

    # Train and get metrics
    metrics = model.get_metrics()

    # ==================================================
    # MODEL PERFORMANCE
    # ==================================================

    print(
        "========== MODEL PERFORMANCE =========="
    )

    print()

    print(
        "Accuracy  :",
        round(
            metrics["accuracy"] * 100,
            2
        ),
        "%"
    )

    print(
        "Precision :",
        round(
            metrics["precision"] * 100,
            2
        ),
        "%"
    )

    print(
        "Recall    :",
        round(
            metrics["recall"] * 100,
            2
        ),
        "%"
    )

    print(
        "F1 Score  :",
        round(
            metrics["f1"] * 100,
            2
        ),
        "%"
    )

    # ==================================================
    # CONFUSION MATRIX
    # ==================================================

    print()
    print(
        "========== CONFUSION MATRIX =========="
    )

    print()

    print(
        metrics["confusion_matrix"]
    )

    print()

    print(
        "Matrix format:"
    )

    print(
        "[[Ham Correct, Ham as Spam]"
    )

    print(
        " [Spam as Ham, Spam Correct]]"
    )

    # ==================================================
    # TEST MESSAGES
    # ==================================================

    test_messages = [

        # Spam
        "आपने इनाम जीता है, अभी क्लिक करें",

        # Ham
        "कल कॉलेज कितने बजे जाना है",

        # Spam
        "आपका अकाउंट बंद होने वाला है, तुरंत verify करें",

        # Ham
        "मुझे कल नोट्स भेज देना",

        # Spam
        "आपके खाते में 5000 रुपये जमा हुए हैं, लिंक पर क्लिक करें",

        # Ham
        "भाई कल कॉलेज आना है क्या",

        # Spam
        "बधाई हो आपने 10 लाख रुपये जीते हैं, अभी अपना इनाम प्राप्त करें",

        # Spam
        "आपका बैंक अकाउंट बंद होने वाला है, तुरंत अपना OTP भेजें",

        # Ham
        "आज शाम को मिलते हैं",

        # Ham
        "मुझे कल सुबह जल्दी उठा देना",

        # Spam
        "आपको फ्री मोबाइल जीतने का मौका मिला है, अभी लिंक पर क्लिक करें",

        # Spam
        "आपके मोबाइल नंबर पर इनाम आया है, claim करने के लिए लिंक खोलें",

        # Ham
        "भाई आज क्रिकेट खेलने चलना है",

        # Ham
        "कल assignment लेकर कॉलेज आ जाना",

        # Spam
        "आपका account verify नहीं हुआ है, अभी password और OTP डालें"

    ]

    # ==================================================
    # MESSAGE TESTING
    # ==================================================

    print()
    print(
        "========== MESSAGE TESTING =========="
    )

    for i, message in enumerate(
        test_messages,
        start=1
    ):

        # ML prediction
        ml_result = model.predict_ml(
            message
        )

        # Rule check
        rule_result = model.rule_check(
            message
        )

        # Final result
        final_result = model.predict(
            message
        )

        print()

        print(
            "Test",
            i
        )

        print(
            "Message:",
            message
        )

        print(
            "ML Result:",
            ml_result.upper()
        )

        if rule_result:

            print(
                "Rule Check: SPAM INDICATOR"
            )

        else:

            print(
                "Rule Check: No strong indicator"
            )

        print(
            "Final Result:",
            final_result.upper()
        )

    # ==================================================
    # END
    # ==================================================

    print()
    print(
        "=========================================="
    )

    print(
        "             TEST COMPLETED"
    )

    print(
        "=========================================="
    )