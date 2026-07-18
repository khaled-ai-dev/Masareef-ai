import re

def normalize_text(text):
    text = str(text).lower() # handles upper or lower case version of a word
    text = re.sub(r"[إأآا]", "ا", text) # handles different arabic patterns ("أوبر", "اوبر")
    text = re.sub(r"ي", "ى", text)
    text = re.sub(r"ه", "ة", text)
    text = re.sub(r"[0-9]+", " ", text) # replaces any digits with a space to learn proberly real language patterns.
    text = re.sub(r"[^\w\s]", " ", text) # replaces anything that is NOT a word chaaracter or whitespace like punctuation and symbols with a space.
    text = re.sub(r"\s+", " ", text).strip() #replaces any run of multiple spaces with a single space.
    return text #returns the cleaned text 

