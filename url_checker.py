import re
import time
import requests


VIRUSTOTAL_SCAN_URL = "https://www.virustotal.com/api/v3/urls"
VIRUSTOTAL_ANALYSIS_URL = "https://www.virustotal.com/api/v3/analyses"


def extract_url(message):
    """
    Message me se pehla URL find karta hai.
    """

    pattern = r"https?://[^\s]+|www\.[^\s]+"

    match = re.search(
        pattern,
        message,
        re.IGNORECASE
    )

    if match:
        return match.group(0).rstrip(".,!?;)")

    return None


def check_url_online(url, api_key):
    """
    VirusTotal par URL submit karke analysis result check karta hai.

    Returns:
        status, details
    """

    if not url:
        return "No URL Found", "Message me koi URL nahi mila."

    if not api_key:
        return "API Key Missing", "VirusTotal API key set nahi hai."

    headers = {
        "x-apikey": api_key
    }

    try:

        # URL submit
        response = requests.post(
            VIRUSTOTAL_SCAN_URL,
            headers=headers,
            data={"url": url},
            timeout=20
        )

        if response.status_code != 200:
            return (
                "API Error",
                f"VirusTotal returned status code: {response.status_code}"
            )

        data = response.json()

        analysis_id = data["data"]["id"]

        # Analysis complete hone ka wait
        for _ in range(10):

            time.sleep(2)

            analysis_response = requests.get(
                f"{VIRUSTOTAL_ANALYSIS_URL}/{analysis_id}",
                headers=headers,
                timeout=20
            )

            if analysis_response.status_code != 200:
                return (
                    "API Error",
                    f"Analysis request failed: "
                    f"{analysis_response.status_code}"
                )

            analysis_data = analysis_response.json()

            attributes = analysis_data["data"]["attributes"]

            status = attributes.get(
                "status",
                "unknown"
            )

            if status == "completed":

                stats = attributes.get(
                    "stats",
                    {}
                )

                malicious = stats.get(
                    "malicious",
                    0
                )

                suspicious = stats.get(
                    "suspicious",
                    0
                )

                harmless = stats.get(
                    "harmless",
                    0
                )

                undetected = stats.get(
                    "undetected",
                    0
                )

                if malicious > 0:

                    result = "Malicious"

                elif suspicious > 0:

                    result = "Suspicious"

                elif harmless > 0:

                    result = "Safe"

                else:

                    result = "Unknown"

                details = (
                    f"URL: {url}\n"
                    f"Status: {result}\n"
                    f"Malicious: {malicious}\n"
                    f"Suspicious: {suspicious}\n"
                    f"Harmless: {harmless}\n"
                    f"Undetected: {undetected}"
                )

                return result, details

        return (
            "Analysis Pending",
            f"VirusTotal analysis is still processing.\n"
            f"Analysis ID: {analysis_id}"
        )

    except requests.exceptions.RequestException as error:

        return (
            "Connection Error",
            f"Could not connect to VirusTotal.\n{error}"
        )

    except Exception as error:

        return (
            "Error",
            str(error)
        )