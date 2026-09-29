from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0


# Common Hinglish/Roman-Hindi words
HINGLISH_WORDS = {
    "aap", "apka", "apne", "aapka",
    "hai", "hain", "ho", "hoga",
    "ka", "ki", "ke",
    "ko", "se", "me", "mein",
    "par", "pe", "ye", "yah",
    "wo", "woh", "kya",
    "kaise", "kese", "kab",
    "kyu", "kyon", "kyunki",
    "mujhe", "mujhse",
    "mera", "meri", "mere",
    "ham", "hum", "hame",
    "aapko", "unhe",
    "kar", "karo", "kare",
    "kiya", "kiye",
    "raha", "rahi", "rahe",
    "gaya", "gayi", "gaye",
    "ja", "jana",
    "chahiye", "nahi",
    "nahin", "abhi",
    "bhi", "bahut",
    "accha", "achha",
    "paisa", "paise",
    "rupaye", "rupay",
    "link", "click"
}


def is_hinglish(message):

    words = message.lower().split()

    # Punctuation remove karo
    clean_words = []

    for word in words:
        word = word.strip(".,!?;:'\"()[]{}")
        clean_words.append(word)

    matches = 0

    for word in clean_words:
        if word in HINGLISH_WORDS:
            matches += 1

    # Kam se kam 2 common Roman-Hindi words
    return matches >= 2


def detect_language(message):

    message = message.strip()

    if not message:
        return "Unknown"

    # Pehle Hinglish check
    if is_hinglish(message):
        return "Hinglish"

    try:
        language = detect(message)

        language_names = {
            "en": "English",
            "hi": "Hindi",
            "bn": "Bengali",
            "mr": "Marathi",
            "gu": "Gujarati",
            "ta": "Tamil",
            "te": "Telugu",
            "pa": "Punjabi",
            "ur": "Urdu",
            "ne": "Nepali"
        }

        return language_names.get(language, "Other")

    except Exception:
        return "Unknown"


# Testing
if __name__ == "__main__":
    print("Language Detector Test Started")
    print("--------------------------------")

test_messages = [
    "Congratulations! You won a prize.",
    "आपने इनाम जीता है।",
    "Aapne prize jeeta hai, link par click karo."
]

for message in test_messages:

    print("Message:", message)
    print("Language:", detect_language(message))
    print()