from transformers import pipeline


def text_classifier(text: str) -> bool:
    """
    Check if text is possitive or not

    Args:
        text (str): text to check

    Returns:
        bool: True if text is possitive, False otherwise
    """

    classifier = pipeline("sentiment-analysis")
    label_data = classifier(text)[0]["label"]

    if label_data == "POSITIVE":
        label = True
    else:
        label = False

    score = classifier(text)[0]["score"]

    return label, score
