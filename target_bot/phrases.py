import json
import random
import hashlib
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

file_path = "data/phrases.json"


async def add_new_phrase(phrase: str) -> bool:
    """
    Adds a new phrase to a JSON file

    Args:
        phrase: the phrase to add
    """
    uuid = hashlib.sha1(phrase.encode('utf-8')).hexdigest()
    logging.log(logging.INFO, f"Calculated hash for new phrase: {uuid}")

    with open(file_path, 'r') as f:
        phrases_data = json.load(f)

    if uuid not in phrases_data:
        phrases_data[uuid] = phrase

        with open(file_path, 'w') as f:
            json.dump(phrases_data, f)

        return True
    else:
        return False


async def get_random_phrase() -> str:
    try:
        with open(file_path, 'r') as f:
            phrases_data = json.load(f)
    except FileNotFoundError:
        return 'File not found.'

    if not phrases_data:
        return "File is empty"

    phrases = list(phrases_data.values())

    return random.choice(phrases)
