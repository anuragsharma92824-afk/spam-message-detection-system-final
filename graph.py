import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay


# ==========================================================
# ENGLISH DATASET DISTRIBUTION
# ==========================================================

def show_dataset_graph(ham_count, spam_count):
    """Show English ham vs spam message distribution."""

    labels = ["Ham", "Spam"]
    values = [ham_count, spam_count]

    plt.figure(figsize=(7, 5))

    plt.bar(
        labels,
        values
    )

    plt.title(
        "English Dataset Distribution"
    )

    plt.xlabel(
        "Message Type"
    )

    plt.ylabel(
        "Number of Messages"
    )

    plt.tight_layout()
    plt.show()


# ==========================================================
# ENGLISH CONFUSION MATRIX
# ==========================================================

def show_confusion_matrix(confusion):
    """Show English model confusion matrix."""

    display = ConfusionMatrixDisplay(
        confusion_matrix=confusion,
        display_labels=["Ham", "Spam"]
    )

    display.plot()

    plt.title(
        "English Model Confusion Matrix"
    )

    plt.tight_layout()
    plt.show()


# ==========================================================
# HINDI DATASET DISTRIBUTION
# ==========================================================

def show_hindi_dataset_graph(
    ham_count,
    spam_count
):
    """Show Hindi ham vs spam dataset distribution."""

    labels = ["Ham", "Spam"]
    values = [ham_count, spam_count]

    plt.figure(figsize=(7, 5))

    plt.bar(
        labels,
        values
    )

    plt.title(
        "Hindi Dataset Distribution"
    )

    plt.xlabel(
        "Message Type"
    )

    plt.ylabel(
        "Number of Messages"
    )

    plt.tight_layout()
    plt.show()


# ==========================================================
# HINDI CONFUSION MATRIX
# ==========================================================

def show_hindi_confusion_matrix(
    confusion
):
    """Show Hindi model confusion matrix."""

    display = ConfusionMatrixDisplay(
        confusion_matrix=confusion,
        display_labels=["Ham", "Spam"]
    )

    display.plot()

    plt.title(
        "Hindi Model Confusion Matrix"
    )

    plt.tight_layout()
    plt.show()


# ==========================================================
# LANGUAGE-WISE DETECTION
# ==========================================================

def show_language_detection_graph(
    english_count,
    hindi_count,
    hinglish_count
):
    """Show language-wise detection results."""

    labels = [
        "English",
        "Hindi",
        "Hinglish"
    ]

    values = [
        english_count,
        hindi_count,
        hinglish_count
    ]

    plt.figure(figsize=(8, 5))

    plt.bar(
        labels,
        values
    )

    plt.title(
        "Language-wise Message Detection"
    )

    plt.xlabel(
        "Language"
    )

    plt.ylabel(
        "Number of Messages"
    )

    plt.tight_layout()
    plt.show()


# ==========================================================
# CURRENT SESSION DETECTION
# ==========================================================

def show_user_detection_graph(
    spam_count,
    ham_count
):
    """Show current session detection results."""

    labels = [
        "Spam",
        "Ham"
    ]

    values = [
        spam_count,
        ham_count
    ]

    plt.figure(figsize=(7, 5))

    plt.bar(
        labels,
        values
    )

    plt.title(
        "Current Session Detection"
    )

    plt.xlabel(
        "Message Type"
    )

    plt.ylabel(
        "Number of Messages"
    )

    plt.tight_layout()
    plt.show()
    # ==========================================================
# IMAGE DETECTION
# ==========================================================

def show_image_detection_graph(
    spam_count,
    ham_count
):
    """Show image spam vs ham detection results."""

    labels = [
        "Image Spam",
        "Image Ham"
    ]

    values = [
        spam_count,
        ham_count
    ]

    plt.figure(figsize=(7, 5))

    plt.bar(
        labels,
        values
    )

    plt.title(
        "Image Detection Results"
    )

    plt.xlabel(
        "Image Message Type"
    )

    plt.ylabel(
        "Number of Images"
    )

    plt.tight_layout()
    plt.show()