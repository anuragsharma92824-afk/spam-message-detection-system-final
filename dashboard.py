import tkinter as tk


def create_stat_card(parent, title, value, row, column, bg_color):
    """Create a simple dashboard statistic card."""

    card = tk.Frame(
        parent,
        bg=bg_color,
        width=200,
        height=120,
        relief="solid",
        borderwidth=1
    )

    card.grid(
        row=row,
        column=column,
        padx=10,
        pady=10
    )

    card.grid_propagate(False)

    title_label = tk.Label(
        card,
        text=title,
        font=("Arial", 12),
        bg=bg_color,
        fg="#555555"
    )

    title_label.pack(pady=(20, 5))

    value_label = tk.Label(
        card,
        text=value,
        font=("Arial", 24, "bold"),
        bg=bg_color,
        fg="#222222"
    )

    value_label.pack()


def create_section_title(parent, text):
    """Create a dashboard section title."""

    title = tk.Label(
        parent,
        text=text,
        font=("Arial", 18, "bold"),
        bg="#f5f5f5",
        fg="#222222"
    )

    title.pack(
        anchor="w",
        padx=30,
        pady=(20, 5)
    )


def create_dashboard(
    parent,
    metrics,
    total_messages,
    spam_count,
    ham_count,
    hindi_metrics,
    hindi_total,
    hindi_spam,
    hindi_ham,
    image_processed,
    image_spam,
    image_ham
):
    """Create the complete English + Hindi dashboard."""

    for widget in parent.winfo_children():
        widget.destroy()

    title = tk.Label(
        parent,
        text="Dashboard",
        font=("Arial", 24, "bold"),
        bg="#f5f5f5",
        fg="#222222"
    )

    title.pack(
        anchor="w",
        padx=30,
        pady=(25, 10)
    )

    # ==================================================
    # ENGLISH MODEL
    # ==================================================

    create_section_title(
        parent,
        "🇬🇧 English Model Performance"
    )

    english_frame = tk.Frame(
        parent,
        bg="#f5f5f5"
    )

    english_frame.pack(
        fill="x",
        padx=20
    )

    accuracy = f"{metrics['accuracy'] * 100:.2f}%"
    precision = f"{metrics['precision'] * 100:.2f}%"
    recall = f"{metrics['recall'] * 100:.2f}%"
    f1 = f"{metrics['f1'] * 100:.2f}%"

    create_stat_card(
        english_frame,
        "Total Messages",
        total_messages,
        0,
        0,
        "#DDEEFF"
    )

    create_stat_card(
        english_frame,
        "Spam Messages",
        spam_count,
        0,
        1,
        "#FFE0E0"
    )

    create_stat_card(
        english_frame,
        "Ham Messages",
        ham_count,
        0,
        2,
        "#DFF5E1"
    )

    create_stat_card(
        english_frame,
        "Accuracy",
        accuracy,
        1,
        0,
        "#E8DFFF"
    )

    create_stat_card(
        english_frame,
        "Precision",
        precision,
        1,
        1,
        "#FFE8CC"
    )

    create_stat_card(
        english_frame,
        "Recall",
        recall,
        1,
        2,
        "#DDF5F5"
    )

    create_stat_card(
        english_frame,
        "F1 Score",
        f1,
        2,
        0,
        "#FFF2CC"
    )

    english_info = tk.Label(
        parent,
        text="Multinomial Naive Bayes + CountVectorizer",
        font=("Arial", 12),
        bg="#f5f5f5",
        fg="#555555"
    )

    english_info.pack(
        anchor="w",
        padx=30,
        pady=(5, 10)
    )

    # ==================================================
    # HINDI MODEL
    # ==================================================

    create_section_title(
        parent,
        "🇮🇳 Hindi Model Performance"
    )

    hindi_frame = tk.Frame(
        parent,
        bg="#f5f5f5"
    )

    hindi_frame.pack(
        fill="x",
        padx=20
    )

    hindi_accuracy = f"{hindi_metrics['accuracy'] * 100:.2f}%"
    hindi_precision = f"{hindi_metrics['precision'] * 100:.2f}%"
    hindi_recall = f"{hindi_metrics['recall'] * 100:.2f}%"
    hindi_f1 = f"{hindi_metrics['f1'] * 100:.2f}%"

    create_stat_card(
        hindi_frame,
        "Total Messages",
        hindi_total,
        0,
        0,
        "#DDEEFF"
    )

    create_stat_card(
        hindi_frame,
        "Spam Messages",
        hindi_spam,
        0,
        1,
        "#FFE0E0"
    )

    create_stat_card(
        hindi_frame,
        "Ham Messages",
        hindi_ham,
        0,
        2,
        "#DFF5E1"
    )

    create_stat_card(
        hindi_frame,
        "Accuracy",
        hindi_accuracy,
        1,
        0,
        "#E8DFFF"
    )

    create_stat_card(
        hindi_frame,
        "Precision",
        hindi_precision,
        1,
        1,
        "#FFE8CC"
    )

    create_stat_card(
        hindi_frame,
        "Recall",
        hindi_recall,
        1,
        2,
        "#DDF5F5"
    )

    create_stat_card(
        hindi_frame,
        "F1 Score",
        hindi_f1,
        2,
        0,
        "#FFF2CC"
    )

    hindi_info = tk.Label(
        parent,
        text="Linear SVM + Word & Character TF-IDF",
        font=("Arial", 12),
        bg="#f5f5f5",
        fg="#555555"
    )

    hindi_info.pack(
        anchor="w",
        padx=30,
        pady=(5, 20)
    )

    # ==========================================================
    # IMAGE DETECTION
    # ==========================================================

    create_section_title(
        parent,
        "🖼️ Image Detection"
    )

    image_frame = tk.Frame(
        parent,
        bg="#f5f5f5"
    )

    image_frame.pack(
        fill="x",
        padx=20
    )

    create_stat_card(
        image_frame,
        "Images Processed",
        image_processed,
        0,
        0,
        "#E8F4FF"
    )

    create_stat_card(
        image_frame,
        "Image Spam",
        image_spam,
        0,
        1,
        "#FFE0E0"
    )

    create_stat_card(
        image_frame,
        "Image Ham",
        image_ham,
        0,
        2,
        "#DFF5E1"
    )