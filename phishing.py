import re


def check_phishing(message):
    """
    Check a message for common suspicious phishing patterns.

    Returns:
        (status, reasons)
    """

    message = message.strip()

    if not message:
        return "No suspicious phishing pattern detected", []

    reasons = []

    # 1. Detect URLs
    url_pattern = r"(https?://|www\.)[^\s]+"
    urls = re.findall(url_pattern, message, re.IGNORECASE)

    if urls:
        reasons.append("Contains a web link")

    # 2. Suspicious URL patterns
    suspicious_url_patterns = [
        r"bit\.ly",
        r"tinyurl\.com",
        r"t\.co",
        r"is\.gd",
        r"goo\.gl",
        r"cutt\.ly",
        r"rb\.gy",
        r"shorturl\.at"
    ]

    for pattern in suspicious_url_patterns:
        if re.search(pattern, message, re.IGNORECASE):
            reasons.append("Uses a URL-shortening service")
            break

    # 3. Suspicious phishing words/phrases
    suspicious_words = [
        "verify your account",
        "verify account",
        "confirm your account",
        "account will be blocked",
        "account suspended",
        "click here",
        "click the link",
        "login immediately",
        "update your password",
        "enter your password",
        "confirm your password",
        "verify your password",
        "urgent action required",
        "security alert",
        "claim your reward",
        "claim your prize",
        "you have won",
        "winner",
        "free prize",
        "bank account",
        "credit card",
        "otp",
        "one time password"
    ]

    message_lower = message.lower()

    for word in suspicious_words:
        if word in message_lower:
            reasons.append(f"Suspicious phrase: {word}")
    
    # Remove duplicate reasons
    reasons = list(dict.fromkeys(reasons))

    # 4. Final decision
    if reasons:
        return "Possible Phishing", reasons

    return "No suspicious phishing pattern detected", []


# Testing the module directly
if __name__ == "__main__":

    test_messages = [
        "Congratulations! You won a prize. Click http://example.com to claim now.",
        "Hi, I will reach college at 10 AM tomorrow.",
        "Your account will be blocked. Verify your password immediately.",
        "Thank you for your help."
    ]

    for message in test_messages:

        status, reasons = check_phishing(message)

        print("\nMessage:")
        print(message)

        print("Result:")
        print(status)

        if reasons:
            print("Reasons:")
            for reason in reasons:
                print("-", reason)