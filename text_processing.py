import re

def highlight_privacy_keywords(review, privacy_keywords):
    # Create a regular expression pattern to match the privacy-related keywords
    pattern = r"\b(" + "|".join(re.escape(word) for word in privacy_keywords) + r")\b"
    
    # Use re.sub to replace the matched keywords with HTML for bold formatting
    return re.sub(pattern, r'<b>\1</b>', review, flags=re.IGNORECASE)
