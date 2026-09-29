import os
import pandas as pd
from datetime import datetime
from config import HISTORY_FILE


# ==========================================================
# HISTORY COLUMNS
# ==========================================================

REQUIRED_COLUMNS = [
    "date_time",
    "source",
    "sender",
    "message",
    "language",
    "result",
    "phishing_status",
    "phishing_reasons",
    "url",
    "url_status",
    "url_details"
]


# ==========================================================
# SAVE HISTORY
# ==========================================================

def save_history(
    message,
    result,
    sender="",
    source="Text",
    phishing_status="",
    phishing_reasons=None,
    url="",
    url_status="",
    url_details="",
    language=""
):

    if phishing_reasons is None:
        phishing_reasons = []

    new_record = pd.DataFrame([{
        "date_time": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        
        "source": source,
        "sender": sender,
        "message": message,
        "language": language,
        "result": result,
        "phishing_status": phishing_status,
        "phishing_reasons": "; ".join(
            phishing_reasons
        ),
        "url": url,
        "url_status": url_status,
        "url_details": url_details
    }])

    # ======================================================
    # EXISTING HISTORY
    # ======================================================

    if os.path.exists(HISTORY_FILE):

        try:

            history = pd.read_csv(
                HISTORY_FILE
            )

            # ------------------------------------------------
            # Add missing columns for old history
            # ------------------------------------------------

            for column in REQUIRED_COLUMNS:

                if column not in history.columns:

                    history[column] = ""

            # ------------------------------------------------
            # Keep correct column order
            # ------------------------------------------------

            history = history[
                REQUIRED_COLUMNS
            ]

            # ------------------------------------------------
            # Add new record
            # ------------------------------------------------

            history = pd.concat(
                [
                    history,
                    new_record
                ],
                ignore_index=True
            )

            # ------------------------------------------------
            # Save complete history
            # ------------------------------------------------

            history.to_csv(
                HISTORY_FILE,
                index=False
            )

        except Exception as e:

            print(
                "History file error:",
                e
            )

            # Create a new history file
            new_record.to_csv(
                HISTORY_FILE,
                mode="w",
                header=True,
                index=False
            )

    # ======================================================
    # NEW HISTORY FILE
    # ======================================================

    else:

        new_record.to_csv(
            HISTORY_FILE,
            mode="w",
            header=True,
            index=False
        )


# ==========================================================
# LOAD HISTORY
# ==========================================================

def load_history():
    """Load message history."""

    if os.path.exists(HISTORY_FILE):

        history = pd.read_csv(
            HISTORY_FILE
        )

        # ==================================================
        # OLD HISTORY COMPATIBILITY
        # ==================================================

        for column in REQUIRED_COLUMNS:

            if column not in history.columns:

                history[column] = ""

        # ==================================================
        # CORRECT COLUMN ORDER
        # ==================================================

        history = history[
            REQUIRED_COLUMNS
        ]

        return history

    # ======================================================
    # EMPTY HISTORY
    # ======================================================

    return pd.DataFrame(
        columns=REQUIRED_COLUMNS
    )


# ==========================================================
# CLEAR HISTORY
# ==========================================================

def clear_history():
    """Delete all saved history."""

    if os.path.exists(HISTORY_FILE):

        os.remove(
            HISTORY_FILE
        )