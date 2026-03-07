REMOVE_WORDS = [
    "am", "is", "are", "was", "were",
    "the", "a", "an",
    "to", "of", "for"
]

def clean_text(text):
    words = text.lower().split()
    words = [w for w in words if w not in REMOVE_WORDS]
    return words


def convert_to_isl(text):

    words = clean_text(text)

    if len(words) < 3:
        return " ".join(words).upper()

    subject = words[0]
    verb = words[1]
    obj = words[2:]

    isl_order = [subject] + obj + [verb]

    return " ".join(isl_order).upper()