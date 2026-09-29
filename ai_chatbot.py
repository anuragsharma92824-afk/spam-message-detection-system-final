import os
import sys
import json
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

from dotenv import load_dotenv
from openai import OpenAI


# =========================================================
# ENVIRONMENT / OPENAI
# =========================================================

def get_app_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))

    return os.path.dirname(os.path.abspath(__file__))


APP_DIR = get_app_dir()

ENV_FILE = os.path.join(
    APP_DIR,
    ".env"
)

CHAT_HISTORY_FILE = os.path.join(
    APP_DIR,
    "chat_history.json"
)

load_dotenv(ENV_FILE)

MODEL = "gpt-5.6-luna"


SYSTEM_PROMPT = """
You are the AI assistant inside a Spam Message Detection System.

Help the user with:
- Spam and Ham messages
- Phishing messages
- Suspicious URLs
- Hindi and Hinglish messages
- Machine Learning concepts
- How this Spam Detection System works
- Explaining detection results

Give simple, clear and useful answers.

When detector results are provided, explain them instead of
inventing results.
"""


# =========================================================
# CHAT HISTORY LOAD / SAVE
# =========================================================

def load_chat_history():
    if not os.path.exists(CHAT_HISTORY_FILE):
        return []

    try:
        with open(
            CHAT_HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except Exception:
        return []


def save_chat_history(sessions):
    try:
        temp_file = CHAT_HISTORY_FILE + ".tmp"

        with open(
            temp_file,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                sessions,
                file,
                ensure_ascii=False,
                indent=2
            )

        os.replace(
            temp_file,
            CHAT_HISTORY_FILE
        )

    except Exception as e:
        print(
            "Chat history save error:",
            e
        )


# =========================================================
# AI FUNCTION
# =========================================================

def ask_ai(message, conversation=None):
    """
    Send user message to OpenAI and return the AI response.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return (
            "⚠️ OpenAI API key nahi mili.\n\n"
            "Apni .env file me OPENAI_API_KEY check karo."
        )

    try:

        client = OpenAI(
            api_key=api_key
        )

        history_text = ""

        if conversation:

            for item in conversation:

                history_text += (
                    f"{item['role'].capitalize()}: "
                    f"{item['content']}\n"
                )

        full_prompt = (
            SYSTEM_PROMPT
            + "\n\nConversation:\n"
            + history_text
            + f"\nUser: {message}\nAssistant:"
        )

        response = client.responses.create(
            model=MODEL,
            input=full_prompt
        )

        return response.output_text

    except Exception as e:

        error = str(e)

        # API quota / credits
        if (
            "429" in error
            or "insufficient_quota" in error
        ):

            return (
                "⚠️ OpenAI API quota/credits "
                "available nahi hain.\n\n"
                "API key sahi hai, lekin API account "
                "me credits check karo."
            )

        # Invalid API key
        if (
            "401" in error
            or "invalid_api_key" in error
        ):

            return (
                "⚠️ OpenAI API key invalid hai.\n\n"
                "Apni .env file me API key check karo."
            )

        # Other error
        return (
            f"⚠️ AI Error:\n{error}"
        )


# =========================================================
# CHATBOT WINDOW
# =========================================================

def open_ai_chatbot(
    root,
    analyze_callback=None
):

    chatbot = tk.Toplevel(root)

    chatbot.title(
        "🤖 AI Chatbot"
    )

    chatbot.geometry(
        "850x650"
    )

    chatbot.minsize(
        700,
        550
    )

    # =====================================================
    # DATA
    # =====================================================

    conversation = []

    # Load previous chats automatically
    chat_sessions = load_chat_history()

    # Index of currently active saved chat
    current_session_index = [None]

    last_ai_response = [""]


    # =====================================================
    # SAVE CURRENT CONVERSATION
    # =====================================================

    def save_current_session():

        if not conversation:
            return

        session_copy = []

        for item in conversation:

            session_copy.append(
                {
                    "role": item.get(
                        "role",
                        ""
                    ),
                    "content": item.get(
                        "content",
                        ""
                    )
                }
            )

        # New session
        if current_session_index[0] is None:

            chat_sessions.append(
                session_copy
            )

            current_session_index[0] = (
                len(chat_sessions) - 1
            )

        # Existing session
        else:

            index = current_session_index[0]

            if (
                0 <= index < len(chat_sessions)
            ):

                chat_sessions[index] = (
                    session_copy
                )

            else:

                chat_sessions.append(
                    session_copy
                )

                current_session_index[0] = (
                    len(chat_sessions) - 1
                )

        save_chat_history(
            chat_sessions
        )


    # =====================================================
    # TOP BAR
    # =====================================================

    top_frame = tk.Frame(
        chatbot
    )

    top_frame.pack(
        fill="x",
        padx=10,
        pady=10
    )


    title = tk.Label(
        top_frame,
        text="🤖 AI Chatbot",
        font=("Arial", 18, "bold")
    )

    title.pack(
        side="left"
    )


    # =====================================================
    # CHAT AREA
    # =====================================================

    chat_box = tk.Text(
        chatbot,
        wrap="word",
        font=("Arial", 11),
        state="disabled"
    )

    chat_box.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=(0, 10)
    )


    # =====================================================
    # CHAT TEXT STYLE
    # =====================================================

    chat_box.tag_config(
        "sender",
        font=("Arial", 11, "bold")
    )


    # =====================================================
    # INPUT FRAME
    # =====================================================

    input_frame = tk.Frame(
        chatbot
    )

    input_frame.pack(
        fill="x",
        padx=10,
        pady=5
    )


    message_entry = tk.Entry(
        input_frame,
        font=("Arial", 12)
    )

    message_entry.pack(
        side="left",
        fill="x",
        expand=True,
        padx=(0, 5)
    )


    send_button = tk.Button(
        input_frame,
        text="📤 Send",
        width=10
    )

    send_button.pack(
        side="right"
    )


    # =====================================================
    # STATUS
    # =====================================================

    status_label = tk.Label(
        chatbot,
        text="Ready",
        anchor="w",
        font=("Arial", 9)
    )

    status_label.pack(
        fill="x",
        padx=10
    )


    # =====================================================
    # ADD MESSAGE TO CHAT
    # =====================================================

    def add_message(
        sender,
        message
    ):

        chat_box.config(
            state="normal"
        )

        chat_box.insert(
            "end",
            f"\n{sender}:\n",
            ("sender",)
        )

        chat_box.insert(
            "end",
            str(message) + "\n"
        )

        chat_box.see(
            "end"
        )

        chat_box.config(
            state="disabled"
        )


    # =====================================================
    # SEND MESSAGE
    # =====================================================

    def send_message():

        message = (
            message_entry
            .get()
            .strip()
        )

        if not message:
            return


        # Clear input
        message_entry.delete(
            0,
            "end"
        )


        # Show user message
        add_message(
            "You",
            message
        )


        # Save conversation
        conversation.append(
            {
                "role": "user",
                "content": message
            }
        )


        # Disable controls
        send_button.config(
            state="disabled"
        )

        message_entry.config(
            state="disabled"
        )


        status_label.config(
            text="🤖 AI is thinking..."
        )


        # =================================================
        # AI BACKGROUND THREAD
        # =================================================

        def ai_worker():

            answer = ask_ai(
                message,
                conversation[:-1]
            )


            # Update Tkinter from main thread
            def update_ui():

                try:

                    add_message(
                        "AI",
                        answer
                    )


                    # Save AI response
                    conversation.append(
                        {
                            "role": "assistant",
                            "content": answer
                        }
                    )


                    # Save latest response
                    last_ai_response[0] = answer


                    # Automatically save chat
                    save_current_session()


                    # Enable controls
                    send_button.config(
                        state="normal"
                    )

                    message_entry.config(
                        state="normal"
                    )


                    status_label.config(
                        text="Ready"
                    )


                    message_entry.focus_set()

                except tk.TclError:
                    pass


            chatbot.after(
                0,
                update_ui
            )


        threading.Thread(
            target=ai_worker,
            daemon=True
        ).start()


    # =====================================================
    # SEND BUTTON
    # =====================================================

    send_button.config(
        command=send_message
    )


    # =====================================================
    # ENTER KEY = SEND
    # =====================================================

    message_entry.bind(
        "<Return>",
        lambda event: send_message()
    )


    # =====================================================
    # BOTTOM BUTTON FRAME
    # =====================================================

    button_frame = tk.Frame(
        chatbot
    )

    button_frame.pack(
        fill="x",
        padx=10,
        pady=10
    )


    # =====================================================
    # COPY RESPONSE
    # =====================================================

    def copy_response():

        response = last_ai_response[0]

        if not response:

            messagebox.showinfo(
                "Copy Response",
                "Abhi koi AI response nahi hai."
            )

            return


        chatbot.clipboard_clear()

        chatbot.clipboard_append(
            response
        )

        chatbot.update()


        status_label.config(
            text="✅ AI response copied."
        )


    tk.Button(
        button_frame,
        text="📋 Copy Response",
        command=copy_response
    ).pack(
        side="left",
        padx=3
    )


    # =====================================================
    # CLEAR CHAT
    # =====================================================

    def clear_chat():

        conversation.clear()

        last_ai_response[0] = ""

        # Next message will start a new session
        current_session_index[0] = None


        chat_box.config(
            state="normal"
        )

        chat_box.delete(
            "1.0",
            "end"
        )

        chat_box.config(
            state="disabled"
        )


        status_label.config(
            text="Chat cleared."
        )

        message_entry.focus_set()


    tk.Button(
        button_frame,
        text="🗑️ Clear Chat",
        command=clear_chat
    ).pack(
        side="left",
        padx=3
    )


    # =====================================================
    # NEW CHAT
    # =====================================================

    def new_chat():

        # Save current conversation
        save_current_session()


        conversation.clear()

        last_ai_response[0] = ""

        current_session_index[0] = None


        chat_box.config(
            state="normal"
        )

        chat_box.delete(
            "1.0",
            "end"
        )

        chat_box.config(
            state="disabled"
        )


        add_message(
            "AI",
            "👋 New chat started.\n"
            "How can I help you?"
        )


        status_label.config(
            text="New chat started."
        )

        message_entry.focus_set()


    tk.Button(
        button_frame,
        text="🔄 New Chat",
        command=new_chat
    ).pack(
        side="left",
        padx=3
    )


    # =====================================================
    # EXPORT CHAT
    # =====================================================

    def export_chat():

        text = chat_box.get(
            "1.0",
            "end"
        ).strip()


        if not text:

            messagebox.showinfo(
                "Export Chat",
                "Export karne ke liye chat empty hai."
            )

            return


        file_path = filedialog.asksaveasfilename(
            title="Export Chat",
            defaultextension=".txt",
            filetypes=[
                ("Text File", "*.txt"),
                ("All Files", "*.*")
            ]
        )


        if not file_path:
            return


        try:

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    text
                )


            messagebox.showinfo(
                "Export Chat",
                "✅ Chat successfully export ho gayi."
            )


        except Exception as e:

            messagebox.showerror(
                "Export Error",
                str(e)
            )


    tk.Button(
        button_frame,
        text="📤 Export Chat",
        command=export_chat
    ).pack(
        side="left",
        padx=3
    )


    # =====================================================
    # CHAT HISTORY
    # =====================================================

    def show_history():

        history_window = tk.Toplevel(
            chatbot
        )


        history_window.title(
            "📜 Chat History"
        )


        history_window.geometry(
            "600x450"
        )


        history_list = tk.Listbox(
            history_window,
            font=("Arial", 11)
        )


        history_list.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )


        # No history
        if not chat_sessions:

            history_list.insert(
                "end",
                "No previous chats available."
            )


        # Show sessions
        for index, session in enumerate(
            chat_sessions,
            start=1
        ):

            user_messages = [
                item.get("content", "")
                for item in session
                if item.get("role") == "user"
            ]


            if user_messages:

                preview = user_messages[0][:70]

            else:

                preview = "Empty Chat"


            history_list.insert(
                "end",
                f"Chat {index}: {preview}"
            )


        # =================================================
        # LOAD SELECTED CHAT
        # =================================================

        def load_selected():

            selection = (
                history_list
                .curselection()
            )


            if not selection:

                messagebox.showwarning(
                    "Chat History",
                    "Pehle koi chat select karo."
                )

                return


            index = selection[0]


            if index >= len(
                chat_sessions
            ):

                return


            session = chat_sessions[index]


            # Replace current conversation
            conversation.clear()

            for item in session:

                conversation.append(
                    {
                        "role": item.get(
                            "role",
                            ""
                        ),
                        "content": item.get(
                            "content",
                            ""
                        )
                    }
                )


            # Loaded chat becomes current session
            current_session_index[0] = index


            # Clear screen
            chat_box.config(
                state="normal"
            )

            chat_box.delete(
                "1.0",
                "end"
            )

            chat_box.config(
                state="disabled"
            )


            last_ai_response[0] = ""


            # Load messages
            for item in conversation:

                if item.get("role") == "user":

                    add_message(
                        "You",
                        item.get(
                            "content",
                            ""
                        )
                    )

                else:

                    add_message(
                        "AI",
                        item.get(
                            "content",
                            ""
                        )
                    )

                    last_ai_response[0] = (
                        item.get(
                            "content",
                            ""
                        )
                    )


            history_window.destroy()


            status_label.config(
                text="Previous chat loaded."
            )

            message_entry.focus_set()


        tk.Button(
            history_window,
            text="📂 Open Chat",
            command=load_selected
        ).pack(
            pady=10
        )


    tk.Button(
        button_frame,
        text="📜 Chat History",
        command=show_history
    ).pack(
        side="left",
        padx=3
    )


    # =====================================================
    # SPAM / PHISHING ANALYSIS
    # =====================================================

    def analyze_message():

        # Check integration
        if analyze_callback is None:

            messagebox.showinfo(
                "Security Analysis",
                "Spam/Phishing integration abhi "
                "main.py se connect nahi hai."
            )

            return


        # First check input box
        message = (
            message_entry
            .get()
            .strip()
        )


        # If input box is empty,
        # use latest user message
        if not message:

            for item in reversed(
                conversation
            ):

                if item.get("role") == "user":

                    message = item.get(
                        "content",
                        ""
                    )

                    break


        # Still empty
        if not message:

            messagebox.showwarning(
                "Security Analysis",
                "Pehle koi message enter ya send karo."
            )

            return


        try:

            status_label.config(
                text="🛡️ Analyzing message..."
            )


            result = analyze_callback(
                message
            )


            add_message(
                "🛡️ Security Analysis",
                str(result)
            )


            status_label.config(
                text="✅ Security analysis completed."
            )


        except Exception as e:

            messagebox.showerror(
                "Analysis Error",
                str(e)
            )


            status_label.config(
                text="Analysis failed."
            )


    # =====================================================
    # ANALYZE BUTTON
    # =====================================================

    tk.Button(
        button_frame,
        text="🛡️ Analyze",
        command=analyze_message
    ).pack(
        side="left",
        padx=3
    )


    # =====================================================
    # WELCOME MESSAGE
    # =====================================================

    add_message(
        "AI",
        "👋 Hello! Main aapke Spam Detection System ka "
        "AI Assistant hoon.\n\n"
        "Aap spam, phishing, suspicious URLs, Machine "
        "Learning ya project ke baare me pooch sakte hain."
    )


    # Cursor input box me
    message_entry.focus_set()


    # =====================================================
    # SAVE WHEN CHATBOT IS CLOSED
    # =====================================================

    def close_chatbot():

        save_current_session()

        chatbot.destroy()


    chatbot.protocol(
        "WM_DELETE_WINDOW",
        close_chatbot
    )


# =========================================================
# DIRECT TEST
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.title(
        "AI Chatbot Test"
    )

    root.geometry(
        "400x200"
    )


    tk.Button(
        root,
        text="🤖 Open AI Chatbot",
        command=lambda: open_ai_chatbot(root)
    ).pack(
        pady=70
    )


    root.mainloop()
