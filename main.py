import tkinter as tk
from tkinter import messagebox
import re
import pyttsx3

from dataset import load_dataset
from model import SpamModel
from history import save_history, load_history, clear_history
from graph import (
    show_dataset_graph,
    show_confusion_matrix,
    show_hindi_dataset_graph,
    show_hindi_confusion_matrix,
    show_language_detection_graph,
    show_user_detection_graph,
    show_image_detection_graph
)

from dashboard import create_dashboard
from phishing import check_phishing
from language_detector import detect_language
from url_checker import  extract_url, check_url_online 
from hindi_model import HindiSpamModel
from image_detector import extract_text_from_image
from tkinter import filedialog
from dotenv import load_dotenv 
import os
import pandas as pd
from ai_chatbot import open_ai_chatbot

# load environment variables 

load_dotenv( )
VIRUSTOTAL_API_KEY=os.getenv("VIRUSTOTAL_API_KEY"," ")

# ==================================================
# COLORS
# ==================================================

BG = "#eef4ff"
CARD = "#ffffff"
NAVY = "#102a56"
BLUE = "#1769ff"
BLUE_DARK = "#0d47c9"
LIGHT_BLUE = "#e8f0ff"
TEXT = "#17233c"
MUTED = "#667085"
GREEN = "#16803c"
RED = "#d92d20"
BORDER = "#d7e2f5"



# ==================================================
# INITIAL SETUP
# ==================================================

df = load_dataset()

spam_total = int((df["label"] == 1).sum())
ham_total = int((df["label"] == 0).sum())
total_messages = len(df)

# ==========================================================
# HINDI DATASET
# ==========================================================

hindi_df = pd.read_csv("hindi_spam.csv")

hindi_spam_total = int(
    (hindi_df["label"].astype(str).str.lower() == "spam").sum()
)

hindi_ham_total = int(
    (hindi_df["label"].astype(str).str.lower() == "ham").sum()
)

hindi_total_messages = len(hindi_df)

spam_model = SpamModel()
metrics = spam_model.get_metrics()
hindi_model = HindiSpamModel()
hindi_metrics = hindi_model.get_metrics()

session_spam = 0
session_ham = 0
session_english = 0
session_hindi = 0 
session_hinglish = 0

voice_enabled = True

engine = pyttsx3.init()

# ===============================================
# image detection
#=================================================

image_processed = 0
image_spam =0
image_ham = 0

# ==================================================
# MAIN WINDOW
# ==================================================

root = tk.Tk()

root.title("Spam Message Detection System")
root.geometry("1100x700")
root.minsize(900, 600)
root.configure(bg=BG)


# ==================================================
# FUNCTIONS
# ==================================================

def speak(text):
    if voice_enabled:
        engine.say(text)
        engine.runAndWait()

def analyze_for_chatbot(message):

    message = message.strip()

    if not message:
        return "⚠️ Please enter a message."

    # Language Detection
    detected_language = detect_language(message)

    # Spam Detection
    if detected_language == "Hindi":
        result = hindi_model.predict(message)

    elif detected_language == "Hinglish":
        result = hindi_model.predict(message)

    else:
        result = spam_model.predict(message)

    if str(result).lower() == "spam":
        result = "Spam"
    else:
        result = "Ham"

    # Phishing Detection
    phishing_status, phishing_reasons = check_phishing(message)

    # URL Detection
    url = extract_url(message)

    if url:
        url_status, url_details = check_url_online(
            url,
            VIRUSTOTAL_API_KEY
        )
    else:
        url_status = "No URL Found"
        url_details = "Message me koi URL nahi mila."

    # Prepare result
    output = (
        "🛡️ SECURITY ANALYSIS\n\n"
        f"🌐 Language: {detected_language}\n"
        f"📩 Spam Result: {result}\n"
        f"🎣 Phishing: {phishing_status}\n"
        f"🔗 URL: {url if url else 'No URL Found'}\n"
        f"🔎 URL Status: {url_status}\n"
        f"📋 URL Details: {url_details}\n"
    )

    if phishing_reasons:
        output += "\n⚠️ Phishing Reasons:\n"

        for reason in phishing_reasons:
            output += f"• {reason}\n"

    return output

def validate_email(email):

    if email == "":
        return True

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    return re.match(pattern, email) is not None


def clear_message():

    sender_entry.delete(0, tk.END)
    message_box.delete("1.0", tk.END)

    result_label.config(
        text="Result will appear here",
        fg=MUTED,
        bg=LIGHT_BLUE
    )
    language_label.config(
        text="Detected Language: -",
        fg=MUTED,
        bg=LIGHT_BLUE
    )

    phishing_label.config(
        text="Phishing result will appear here",
        fg=MUTED,
        bg=LIGHT_BLUE
    )


def check_message():

    global session_spam, session_ham
    global session_english, session_hindi, session_hinglish

    sender = sender_entry.get().strip()
    message = message_box.get("1.0", tk.END).strip()

    # Empty message check
    if not message:

        messagebox.showwarning(
            "Warning",
            "Please enter a message."
        )

        return

    # Email validation
    if sender and "@" not in sender:

        messagebox.showwarning(
            "Warning",
            "Please enter a valid sender email."
        )

        return
    #=========================================================
    #Language detection
    #=========================================================

    detected_language = detect_language(message)

    if detected_language == "English":
        session_english += 1

    elif detected_language == "Hindi":
        session_hindi += 1

    elif detected_language == "Hinglish":
        session_hinglish += 1
    language_label.config(
        text=f"Detected Language:{detected_language}",
        fg=TEXT,
        bg=LIGHT_BLUE
    )

    # ==========================================================
    # SPAM DETECTION
    # ==========================================================

    if detected_language == "Hindi":

        result = hindi_model.predict(message)

    elif detected_language == "Hinglish":

        result = hindi_model.predict(message)

    else:

       result = spam_model.predict(message)

# Hindi model returns lowercase result
# English model returns "Spam" / "Ham"

    if result.lower() == "spam":
        result = "Spam"
    else:
        result = "Ham"

    # ==========================================================
    # PHISHING DETECTION
    # ==========================================================

    phishing_status, phishing_reasons = check_phishing(message)

    # ==========================================================
    # ONLINE URL VERIFICATION
    # ==========================================================

    url = extract_url(message)

    if url:

        url_status, url_details = check_url_online(
            url,
            VIRUSTOTAL_API_KEY
        )

    else:

        url_status = "No URL Found"
        url_details = "Message me koi URL nahi mila."

    # ==========================================================
    # DISPLAY ONLINE URL VERIFICATION RESULT
    # ==========================================================

    if url_status == "Malicious":

        url_color = RED

    elif url_status == "Suspicious":

        url_color = "#D97706"

    elif url_status == "Safe":

        url_color = GREEN

    else:

        url_color = MUTED

    url_label.config(
        text=f"ONLINE URL VERIFICATION\n\n{url_details}",
        fg=url_color,
        bg=LIGHT_BLUE
    )

    # ==========================================================
    # SPAM RESULT
    # ==========================================================

    if result == "Spam":

        session_spam += 1

        result_label.config(
            text="⚠️  SPAM MESSAGE",
            fg=RED,
            bg="#fff1f0"
        )

        speak(
            "Warning. This message is spam."
        )

    else:

        session_ham += 1

        result_label.config(
            text="✓  HAM MESSAGE",
            fg=GREEN,
            bg="#ecfdf3"
        )

        speak(
            "This message is not spam."
        )

    # ==========================================================
    # PHISHING DETECTION RESULT
    # ==========================================================

    if phishing_status == "Possible Phishing":

        phishing_text = "⚠️  POSSIBLE PHISHING\n\n"

        for reason in phishing_reasons:

            phishing_text += "• " + reason + "\n"

        phishing_label.config(
            text=phishing_text,
            fg=RED,
            bg="#fff1f0"
        )

    else:

        phishing_label.config(
            text="✓  NO SUSPICIOUS PHISHING PATTERN DETECTED",
            fg=GREEN,
            bg="#ecfdf3"
        )

    # ==========================================================
    # SAVE HISTORY
    # ==========================================================

    save_history(
        message,
        result,
        sender,
        phishing_status,
        phishing_reasons,
        url,
        url_status,
        url_details,
        language=detected_language
    )


# ==================================================
# IMAGE DETECTION
# ==================================================

def detect_image():

    global image_processed
    global image_spam
    global image_ham

    image_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg *.bmp *.webp"),
            ("All Files", ".")
        ]
    )

    if not image_path:
        return

    # ==================================================
    # OCR
    # ==================================================

    image_text = extract_text_from_image(image_path)

    if not image_text:

        messagebox.showwarning(
            "OCR Failed",
            "Image se readable text nahi mila."
        )

        return

    # ==================================================
    # PHISHING CHECK
    # ==================================================

    phishing_status, phishing_reasons = check_phishing(
        image_text
    )

    # ==================================================
    # URL CHECK
    # ==================================================

    image_url = extract_url(image_text)

    if image_url:

        image_url_status, image_url_details = check_url_online(
            image_url, VIRUSTOTAL_API_KEY
        )

    else:

        image_url_status = "No URL"
        image_url_details = ""

    # ==================================================
    # LANGUAGE DETECTION
    # ==================================================

    language = detect_language(image_text)

    # ==================================================
    # SPAM DETECTION
    # ==================================================

    if language == "Hindi":

        result = hindi_model.predict(image_text)

        if result == "spam":
            result = "Spam"
        else:
            result = "Ham"

    else:

        result = spam_model.predict(image_text)

    # ==================================================
    # IMAGE COUNTERS
    # ==================================================

    image_processed += 1

    if result == "Spam":
        image_spam += 1
    else:
        image_ham += 1

    # ==================================================
    # SAVE IMAGE DETECTION IN HISTORY
    # ==================================================

    save_history(
        message=image_text,
        result=result,
        sender="",
        source="Image",
        language=language,
        phishing_status=phishing_status,
        phishing_reasons=phishing_reasons,
        url=image_url,
        url_status=image_url_status,
        url_details=image_url_details
    )

    # ==================================================
    # RESULT WINDOW
    # ==================================================

    result_window = tk.Toplevel(root)

    result_window.title(
        "Image Detection Result"
    )

    result_window.geometry(
        "700x650"
    )

    result_window.configure(
        bg=BG
    )

    title = tk.Label(
        result_window,
        text="🖼️ Image Detection Result",
        font=("Arial", 22, "bold"),
        bg=BG,
        fg=NAVY
    )

    title.pack(
        pady=20
    )

    # Result
    if result == "Spam":

        result_text = "⚠️ IMAGE SPAM"
        result_color = RED

    else:

        result_text = "✓ IMAGE HAM"
        result_color = GREEN

    result_label = tk.Label(
        result_window,
        text=result_text,
        font=("Arial", 20, "bold"),
        bg=LIGHT_BLUE,
        fg=result_color,
        padx=25,
        pady=15
    )

    result_label.pack(
        fill="x",
        padx=30,
        pady=10
    )

    # Language
    language_label = tk.Label(
        result_window,
        text=f"Detected Language: {language}",
        font=("Arial", 13, "bold"),
        bg=BG,
        fg=TEXT
    )

    language_label.pack(
        pady=10
    )

    # Phishing
    phishing_label = tk.Label(
        result_window,
        text=f"Phishing: {phishing_status}",
        font=("Arial", 12, "bold"),
        bg=BG,
        fg=TEXT
    )

    phishing_label.pack(
        pady=5
    )

    # URL
    url_label = tk.Label(
        result_window,
        text=f"URL Status: {image_url_status}",
        font=("Arial", 12, "bold"),
        bg=BG,
        fg=TEXT
    )

    url_label.pack(
        pady=5
    )

    # OCR Text title
    text_title = tk.Label(
        result_window,
        text="OCR Extracted Text",
        font=("Arial", 14, "bold"),
        bg=BG,
        fg=NAVY
    )

    text_title.pack(
        anchor="w",
        padx=30,
        pady=(15, 5)
    )

    # OCR Text box
    text_box = tk.Text(
        result_window,
        height=12,
        wrap="word",
        font=("Arial", 11),
        bg=CARD,
        fg=TEXT
    )

    text_box.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 20)
    )

    text_box.insert(
        tk.END,
        image_text
    )

    text_box.config(
        state="disabled"
    )

    # Voice
    if result == "Spam":

        speak(
            "Warning. This image contains a spam message."
        )

    else:

        speak(
            "This image contains a ham message."
        )

# ==================================================
# HOME
# ==================================================

def show_home():

    clear_pages()

    home_frame = tk.Frame(
        content_frame,
        bg=BG
    )

    home_frame.pack(
        fill="both",
        expand=True
    )

    title = tk.Label(
        home_frame,
        text="Spam Message Detection",
        font=("Arial", 28, "bold"),
        bg=BG,
        fg=NAVY
    )

    title.pack(
        pady=(25, 5)
    )

    subtitle = tk.Label(
        home_frame,
        text="Machine Learning Based Spam Detection System",
        font=("Arial", 13),
        bg=BG,
        fg=MUTED
    )

    subtitle.pack(
        pady=(0, 20)
    )

    # ==================================================
    # SCROLLABLE MAIN CARD
    # ==================================================

    scroll_container = tk.Frame(
        home_frame,
        bg=BG
    )

    scroll_container.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 15)
    )

    # Canvas

    canvas = tk.Canvas(
        scroll_container,
        bg=BG,
        highlightthickness=0,
        borderwidth=0
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    # Scrollbar

    scrollbar = tk.Scrollbar(
        scroll_container,
        orient="vertical",
        command=canvas.yview
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    # ==================================================
    # INPUT FRAME
    # ==================================================

    input_frame = tk.Frame(
        canvas,
        bg=CARD,
        padx=28,
        pady=22,
        relief="solid",
        borderwidth=1,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    canvas_window = canvas.create_window(
        (0, 0),
        window=input_frame,
        anchor="nw"
    )

    # ==================================================
    # SCROLL REGION UPDATE
    # ==================================================

    def update_scroll_region(event=None):

        canvas.configure(
            scrollregion=canvas.bbox("all")
        )

        canvas.itemconfig(
            canvas_window,
            width=canvas.winfo_width()
        )

    input_frame.bind(
        "<Configure>",
        update_scroll_region
    )

    canvas.bind(
        "<Configure>",
        update_scroll_region
    )

    # ==================================================
    # SENDER
    # ==================================================

    sender_label = tk.Label(
        input_frame,
        text="Sender Email",
        font=("Arial", 12, "bold"),
        bg=CARD,
        fg=TEXT
    )

    sender_label.pack(
        anchor="w"
    )

    global sender_entry

    sender_entry = tk.Entry(
        input_frame,
        font=("Arial", 12),
        bg="#f8faff",
        fg=TEXT,
        relief="solid",
        borderwidth=1
    )

    sender_entry.pack(
        fill="x",
        pady=(7, 18),
        ipady=8
    )

    # ==================================================
    # MESSAGE
    # ==================================================

    message_label = tk.Label(
        input_frame,
        text="Enter Message",
        font=("Arial", 12, "bold"),
        bg=CARD,
        fg=TEXT
    )

    message_label.pack(
        anchor="w"
    )

    global message_box

    message_box = tk.Text(
        input_frame,
        height=7,
        font=("Arial", 12),
        wrap="word",
        bg="#f8faff",
        fg=TEXT,
        relief="solid",
        borderwidth=1
    )

    message_box.pack(
        fill="x",
        pady=(7, 10)
    )

    # ==================================================
    # BUTTONS
    # ==================================================

    button_frame = tk.Frame(
        input_frame,
        bg=CARD
    )

    button_frame.pack(
        pady=15
    )

    check_button = tk.Button(
        button_frame,
        text="🔍  Check Message",
        command=check_message,
        font=("Arial", 11, "bold"),
        bg=BLUE,
        fg="white",
        activebackground=BLUE_DARK,
        activeforeground="white",
        relief="flat",
        padx=22,
        pady=10,
        cursor="hand2"
    )

    check_button.pack(
        side="left",
        padx=7
    )

    clear_button = tk.Button(
        button_frame,
        text="🧹 Clear",
        command=clear_message,
        font=("Arial", 11, "bold"),
        bg="#e53935",
        fg="white",
        activebackground="#b71c1c",
        activeforeground="white",
        relief="flat",
        padx=24,
        pady=10,
        cursor="hand2"
    )

    clear_button.pack(
        side="left",
        padx=7
    )

    # ==================================================
    # RESULT
    # ==================================================

    global result_label

    result_label = tk.Label(
        input_frame,
        text="Result will appear here",
        font=("Arial", 17, "bold"),
        bg=LIGHT_BLUE,
        fg=MUTED,
        padx=20,
        pady=15
    )

    result_label.pack(
        fill="x",
        pady=(10, 0)
    )

    # ==================================================
    # LANGUAGE DETECTION RESULT
    # ==================================================

    global language_label

    language_label = tk.Label(
        input_frame,
        text="Detected Language: -",
        font=("Arial", 13, "bold"),
        bg=LIGHT_BLUE,
        fg=MUTED,
        padx=20,
        pady=12,
        anchor="w"
    )

    language_label.pack(
        fill="x",
        pady=(8, 0)
    )

    # ==================================================
    # PHISHING RESULT
    # ==================================================

    global phishing_label, url_label

    phishing_label = tk.Label(
        input_frame,
        text="Phishing result will appear here",
        font=("Arial", 15, "bold"),
        bg=LIGHT_BLUE,
        fg=MUTED,
        padx=20,
        pady=15,
        justify="left",
        anchor="w"
    )

    phishing_label.pack(
        fill="x",
        pady=(12, 0)
    )

    # ==================================================
    # ONLINE URL VERIFICATION
    # ==================================================

    url_label = tk.Label(
        input_frame,
        text="Online URL verification result will appear here",
        font=("Arial", 13, "bold"),
        bg=LIGHT_BLUE,
        fg=MUTED,
        padx=20,
        pady=15,
        justify="left",
        anchor="w"
    )

    url_label.pack(
        fill="x",
        pady=(5, 12)
    )


def show_dashboard_page():

    clear_pages()

    # ==============================
    # DASHBOARD SCROLL AREA
    # ==============================

    canvas = tk.Canvas(
        content_frame,
        bg=BG,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        content_frame,
        orient="vertical",
        command=canvas.yview
    )

    scrollable_frame = tk.Frame(
        canvas,
        bg=BG
    )

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window(
        (0, 0),
        window=scrollable_frame,
        anchor="nw"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # Mouse wheel scrolling
    canvas.bind_all(
        "<MouseWheel>",
        lambda event: canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )
    )

    # ==============================
    # DASHBOARD
    # ==============================

    create_dashboard(
        scrollable_frame,
        metrics,
        total_messages,
        spam_total,
        ham_total,
        hindi_metrics,
        hindi_total_messages,
        hindi_spam_total,
        hindi_ham_total,
        image_processed,
        image_spam,
        image_ham
    )

# ==========================================================
# GRAPHS
# ==========================================================

def show_graph_page():

    clear_pages()

    page = tk.Frame(
        content_frame,
        bg=BG
    )

    page.pack(
        fill="both",
        expand=True
    )

    title = tk.Label(
        page,
        text="Graphs & Visualization",
        font=("Arial", 25, "bold"),
        bg=BG,
        fg=NAVY
    )

    title.pack(
        pady=(25, 10)
    )

    # ======================================================
    # ENGLISH DATASET
    # ======================================================

    english_dataset_button = tk.Button(
        page,
        text="📊  English Dataset Distribution",
        command=lambda: show_dataset_graph(
            ham_total,
            spam_total
        ),
        font=("Arial", 11, "bold"),
        bg=BLUE,
        fg="white",
        activebackground=BLUE_DARK,
        activeforeground="white",
        relief="flat",
        width=34,
        pady=10,
        cursor="hand2"
    )

    english_dataset_button.pack(
        pady=5
    )

    # ======================================================
    # ENGLISH CONFUSION MATRIX
    # ======================================================

    english_confusion_button = tk.Button(
        page,
        text="🔲  English Model Confusion Matrix",
        command=lambda: show_confusion_matrix(
            metrics["confusion_matrix"]
        ),
        font=("Arial", 11, "bold"),
        bg=NAVY,
        fg="white",
        activebackground="#1c3e73",
        activeforeground="white",
        relief="flat",
        width=34,
        pady=10,
        cursor="hand2"
    )

    english_confusion_button.pack(
        pady=5
    )

    # ======================================================
    # HINDI DATASET
    # ======================================================

    hindi_dataset_button = tk.Button(
        page,
        text="📊  Hindi Dataset Distribution",
        command=lambda: show_hindi_dataset_graph(
            hindi_ham_total,
            hindi_spam_total
        ),
        font=("Arial", 11, "bold"),
        bg=GREEN,
        fg="white",
        activebackground="#126b32",
        activeforeground="white",
        relief="flat",
        width=34,
        pady=10,
        cursor="hand2"
    )

    hindi_dataset_button.pack(
        pady=5
    )

    # ======================================================
    # HINDI CONFUSION MATRIX
    # ======================================================

    hindi_confusion_button = tk.Button(
        page,
        text="🔲  Hindi Model Confusion Matrix",
        command=lambda: show_hindi_confusion_matrix(
            hindi_metrics["confusion_matrix"]
        ),
        font=("Arial", 11, "bold"),
        bg="#7F56D9",
        fg="white",
        activebackground="#6941C6",
        activeforeground="white",
        relief="flat",
        width=34,
        pady=10,
        cursor="hand2"
    )

    hindi_confusion_button.pack(
        pady=5
    )

    # ======================================================
    # LANGUAGE-WISE DETECTION
    # ======================================================

    language_button = tk.Button(
        page,
        text="🌐  Language-wise Detection",
        command=lambda: show_language_detection_graph(
            session_english,
            session_hindi,
            session_hinglish
        ),
        font=("Arial", 11, "bold"),
        bg="#D97706",
        fg="white",
        activebackground="#B45309",
        activeforeground="white",
        relief="flat",
        width=34,
        pady=10,
        cursor="hand2"
    )

    language_button.pack(
        pady=5
    )

    # ======================================================
    # CURRENT SESSION
    # ======================================================

    user_button = tk.Button(
        page,
        text="📈  Current Session Detection",
        command=lambda: show_user_detection_graph(
            session_spam,
            session_ham
        ),
        font=("Arial", 11, "bold"),
        bg="#475467",
        fg="white",
        activebackground="#344054",
        activeforeground="white",
        relief="flat",
        width=34,
        pady=10,
        cursor="hand2"
    )

    user_button.pack(
        pady=5
    )

    # ==========================================================
# IMAGE DETECTION
# ==========================================================

    image_button = tk.Button(
    page,
    text="🖼️ Image Detection Results",
    command=lambda: show_image_detection_graph(
        image_spam,
        image_ham
    ),
    font=("Arial", 11, "bold"),
    bg=BLUE,
    fg="white",
    activebackground=BLUE_DARK,
    activeforeground="white",
    relief="flat",
    width=34,
    pady=10,
    cursor="hand2"
)

    image_button.pack(
        pady=5
)

# ==================================================
# HISTORY
# ==================================================

def show_history_page():

    clear_pages()

    page = tk.Frame(
        content_frame,
        bg=BG
    )

    page.pack(
        fill="both",
        expand=True
    )

    title = tk.Label(
        page,
        text="Message History",
        font=("Arial", 25, "bold"),
        bg=BG,
        fg=NAVY
    )

    title.pack(
        pady=(18, 8)
    )

    # ==================================================
    # SEARCH BAR
    # ==================================================

    search_frame = tk.Frame(
        page,
        bg=BG
    )

    search_frame.pack(
        fill="x",
        padx=30,
        pady=(0, 8)
    )

    search_label = tk.Label(
        search_frame,
        text="🔎 Search:",
        font=("Arial", 11, "bold"),
        bg=BG,
        fg=TEXT
    )

    search_label.pack(
        side="left",
        padx=(0, 8)
    )

    search_entry = tk.Entry(
        search_frame,
        font=("Arial", 11),
        bg="white",
        fg=TEXT,
        relief="solid",
        borderwidth=1
    )

    search_entry.pack(
        side="left",
        fill="x",
        expand=True,
        ipady=6
    )

    # ==================================================
    # HISTORY FRAME
    # ==================================================

    history_frame = tk.Frame(
        page,
        bg=BG
    )

    history_frame.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=5
    )

    scrollbar = tk.Scrollbar(
        history_frame,
        orient="vertical"
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    text_area = tk.Text(
        history_frame,
        font=("Arial", 11),
        wrap="word",
        bg=CARD,
        fg=TEXT,
        relief="solid",
        borderwidth=1,
        yscrollcommand=scrollbar.set
    )

    text_area.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.config(
        command=text_area.yview
    )

    # ==================================================
    # LOAD HISTORY DATA
    # ==================================================

    history_data = load_history()

    # ==================================================
    # DISPLAY HISTORY
    # ==================================================

    def display_history(data):

        text_area.config(
            state="normal"
        )

        text_area.delete(
            "1.0",
            tk.END
        )

        if data.empty:

            text_area.insert(
                tk.END,
                "No matching history found."
            )

        else:

            for _, row in data.iterrows():

                text_area.insert(
                    tk.END,
                    f"Date: {row.get('date_time', '')}\n"
                )

                text_area.insert(
                    tk.END,
                    f"Source: {row.get('source', 'Text')}\n"
                )

                text_area.insert(
                    tk.END,
                    f"Sender: {row.get('sender', '')}\n"
                )

                text_area.insert(
                    tk.END,
                    f"Message: {row.get('message', '')}\n"
                )

                text_area.insert(
                    tk.END,
                    f"Language: {row.get('language', '')}\n"
                )

                text_area.insert(
                    tk.END,
                    f"Result: {row.get('result', '')}\n"
                )

                # Phishing
                phishing_status = str(
                    row.get(
                        "phishing_status",
                        ""
                    )
                ).strip()

                if (
                    phishing_status
                    and phishing_status != "nan"
                ):

                    text_area.insert(
                        tk.END,
                        f"Phishing: {phishing_status}\n"
                    )

                # Phishing reasons
                phishing_reasons = str(
                    row.get(
                        "phishing_reasons",
                        ""
                    )
                ).strip()

                if (
                    phishing_reasons
                    and phishing_reasons != "nan"
                ):

                    text_area.insert(
                        tk.END,
                        "Phishing Reasons:\n"
                    )

                    reasons = phishing_reasons.split(";")

                    for reason in reasons:

                        reason = reason.strip()

                        if reason:

                            text_area.insert(
                                tk.END,
                                f"  • {reason}\n"
                            )

                # URL
                url_value = str(
                    row.get(
                        "url",
                        ""
                    )
                ).strip()

                url_status = str(
                    row.get(
                        "url_status",
                        ""
                    )
                ).strip()

                url_details = str(
                    row.get(
                        "url_details",
                        ""
                    )
                ).strip()

                if (
                    url_value
                    and url_value != "nan"
                ):

                    text_area.insert(
                        tk.END,
                        f"URL: {url_value}\n"
                    )

                    text_area.insert(
                        tk.END,
                        f"URL Status: {url_status}\n"
                    )

                    if (
                        url_details
                        and url_details != "nan"
                    ):

                        text_area.insert(
                            tk.END,
                            f"URL Details: {url_details}\n"
                        )

                text_area.insert(
                    tk.END,
                    "\n------------------------------\n\n"
                )

        text_area.config(
            state="disabled"
        )

    # ==================================================
    # SEARCH FUNCTION
    # ==================================================

    def search_history():

        search_text = (
            search_entry
            .get()
            .strip()
            .lower()
        )

        if not search_text:

            display_history(
                history_data
            )

            return

        # Search across all columns
        mask = history_data.astype(
            str
        ).apply(
            lambda column: column.str.lower().str.contains(
                search_text,
                na=False
            )
        ).any(
            axis=1
        )

        filtered_data = history_data[
            mask
        ]

        display_history(
            filtered_data
        )

    # ==================================================
    # REFRESH / LOAD HISTORY
    # ==================================================

    def refresh_history():

        nonlocal history_data

        history_data = load_history()

        search_entry.delete(
            0,
            tk.END
        )

        display_history(
            history_data
        )

    # ==================================================
    # BUTTONS
    # ==================================================

    button_frame = tk.Frame(
        page,
        bg=BG
    )

    button_frame.pack(
        pady=10
    )

    search_button = tk.Button(
        button_frame,
        text="🔎 Search",
        command=search_history,
        font=("Arial", 11, "bold"),
        bg=BLUE,
        fg="white",
        activebackground=BLUE_DARK,
        activeforeground="white",
        relief="flat",
        padx=25,
        pady=10,
        cursor="hand2"
    )

    search_button.pack(
        side="left",
        padx=5
    )

    load_button = tk.Button(
        button_frame,
        text="🔄 Load History",
        command=refresh_history,
        font=("Arial", 11, "bold"),
        bg=GREEN,
        fg="white",
        activebackground="#126b32",
        activeforeground="white",
        relief="flat",
        padx=25,
        pady=10,
        cursor="hand2"
    )

    load_button.pack(
        side="left",
        padx=5
    )

    clear_button = tk.Button(
        button_frame,
        text="🗑️ Clear History",
        command=delete_history,
        font=("Arial", 11, "bold"),
        bg="#c62828",
        fg="white",
        activebackground="#8e0000",
        activeforeground="white",
        relief="flat",
        padx=25,
        pady=10,
        cursor="hand2"
    )

    clear_button.pack(
        side="left",
        padx=5
    )

    # ==================================================
    # INITIAL DISPLAY
    # ==================================================

    display_history(
        history_data
    )

def delete_history():

    answer = messagebox.askyesno(
        "Clear History",
        "Are you sure you want to delete all history?"
    )

    if answer:

        clear_history()

        messagebox.showinfo(
            "History",
            "History cleared successfully."
        )

        show_history_page()
 
# ==================================================
# SETTINGS
# ==================================================

def show_settings_page():

    clear_pages()

    page = tk.Frame(
        content_frame,
        bg=BG
    )

    page.pack(
        fill="both",
        expand=True
    )

    title = tk.Label(
        page,
        text="Settings",
        font=("Arial", 26, "bold"),
        bg=BG,
        fg=NAVY
    )

    title.pack(
        pady=(25, 15)
    )

    # Voice card

    voice_card = tk.Frame(
        page,
        bg=CARD,
        padx=25,
        pady=20,
        relief="solid",
        borderwidth=1,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    voice_card.pack(
        padx=70,
        fill="x"
    )

    voice_title = tk.Label(
        voice_card,
        text="🔊 Voice Output",
        font=("Arial", 15, "bold"),
        bg=CARD,
        fg=TEXT
    )

    voice_title.pack(
        anchor="w"
    )

    voice_description = tk.Label(
        voice_card,
        text="Enable or disable voice feedback after message detection.",
        font=("Arial", 10),
        bg=CARD,
        fg=MUTED
    )

    voice_description.pack(
        anchor="w",
        pady=(3, 15)
    )

    global voice_enabled

    voice_var = tk.BooleanVar(
        value=voice_enabled
    )

    # Large ON/OFF button

    def change_voice():

        global voice_enabled

        voice_enabled = voice_var.get()

        if voice_enabled:

            voice_button.config(
                text="  ●  ON  ",
                bg=GREEN,
                activebackground="#126b32"
            )

            voice_status.config(
                text="Voice output is ON",
                fg=GREEN
            )

        else:

            voice_button.config(
                text="  ●  OFF  ",
                bg="#667085",
                activebackground="#475467"
            )

            voice_status.config(
                text="Voice output is OFF",
                fg=MUTED
            )

    voice_button = tk.Button(
        voice_card,
        text="  ●  ON  ",
        command=lambda: (
            voice_var.set(not voice_var.get()),
            change_voice()
        ),
        font=("Arial", 13, "bold"),
        bg=GREEN,
        fg="white",
        activebackground="#126b32",
        activeforeground="white",
        relief="flat",
        padx=30,
        pady=10,
        cursor="hand2"
    )

    voice_button.pack(
        side="left",
        padx=(0, 15)
    )

    voice_status = tk.Label(
        voice_card,
        text="Voice output is ON",
        font=("Arial", 11, "bold"),
        bg=CARD,
        fg=GREEN
    )

    voice_status.pack(
        side="left"
    )


    # System information

    info_title = tk.Label(
        page,
        text="System Information",
        font=("Arial", 17, "bold"),
        bg=BG,
        fg=NAVY
    )

    info_title.pack(
        anchor="w",
        padx=70,
        pady=(25, 10)
    )

    info_card = tk.Frame(
        page,
        bg=CARD,
        padx=30,
        pady=20,
        relief="solid",
        borderwidth=1,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    info_card.pack(
        padx=70,
        fill="x"
    )

    info = tk.Label(
        info_card,
        text=(
            "Spam Message Detection System\n\n"
            "Machine Learning     : Multinomial Naive Bayes\n"
            "Feature Extraction   : CountVectorizer\n"
            "GUI                   : Tkinter\n"
            "Dataset               : SMS Spam Collection"
        ),
        font=("Arial", 11),
        bg=CARD,
        fg=TEXT,
        justify="left"
    )

    info.pack(
        anchor="w"
    )
   

# ==================================================
# CLEAR PAGES
# ==================================================

def clear_pages():

    for widget in content_frame.winfo_children():
        widget.destroy()


# ==================================================
# SIDEBAR
# ==================================================

sidebar = tk.Frame(
    root,
    bg=NAVY,
    width=220
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)


app_title = tk.Label(
    sidebar,
    text="SPAM\nDETECTOR",
    font=("Arial", 20, "bold"),
    bg=NAVY,
    fg="white"
)

app_title.pack(
    pady=30
)


def create_menu_button(text, command):

    button = tk.Button(
        sidebar,
        text=text,
        command=command,
        font=("Arial", 11, "bold"),
        bg="#183766",
        fg="white",
        activebackground=BLUE,
        activeforeground="white",
        relief="flat",
        padx=10,
        pady=11,
        cursor="hand2"
    )

    button.pack(
        fill="x",
        padx=15,
        pady=5
    )

create_menu_button(
    "🏠  Home",
    show_home
)

create_menu_button(
    "📊  Dashboard",
    show_dashboard_page
)

create_menu_button(
    "📈  Graphs",
    show_graph_page
)

create_menu_button(
    "🖼️  Image Detection", detect_image)


create_menu_button(
    "📜  History",
    show_history_page
)
create_menu_button(
    "🤖  AI Chatbot",
    lambda: open_ai_chatbot(
        root,
        analyze_callback=analyze_for_chatbot
    )
)

create_menu_button(
    "⚙️  Settings",
    show_settings_page
)

# ==================================================
# SIDEBAR FOOTER
# ==================================================

footer = tk.Label(
    sidebar,
    text="Smarter Messages\nSafer You",
    font=("Arial", 10, "bold"),
    bg=NAVY,
    fg="#a9c7ff"
)

footer.pack(
    side="bottom",
    pady=30
)

# ==================================================
# CONTENT AREA
# ==================================================

content_frame = tk.Frame(
    root,
    bg=BG
)

content_frame.pack(
    side="right",
    fill="both",
    expand=True
)

# ==================================================
# START
# ==================================================

show_home()

root.mainloop()