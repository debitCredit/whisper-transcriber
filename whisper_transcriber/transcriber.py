import os
import sys
import logging
import openai

from tenacity import retry, wait_random_exponential, stop_after_attempt
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AUDIO_ENGINE_ID = "whisper-1"


def initialize_openai_api_and_logging():
    if not OPENAI_API_KEY:
        logging.error("Error - OPENAI_API_KEY not set")
        sys.exit(1)
    else:
        openai.api_key = OPENAI_API_KEY

    logging.basicConfig(level=logging.INFO)


@retry(wait=wait_random_exponential(multiplier=0.5, max=60), stop=stop_after_attempt(3))
def transcribe_audio(file_name):
    try:
        with open(file_name, "rb") as audio_file_obj:
            logging.info("Opened audio file: %s", file_name)
            logging.info("Transcribing audio...")
            transcript = openai.Audio.transcribe(AUDIO_ENGINE_ID, audio_file_obj)

            logging.info(transcript["text"])

    except FileNotFoundError as e:  # pylint: disable=C0103
        logging.error("Could not find audio file: %s", file_name)
        raise e
    except openai.error.OpenAIError as e:  # pylint: disable=C0103
        logging.error("Error calling OpenAI API: %s", e)


if __name__ == "__main__":
    initialize_openai_api_and_logging()

    if len(sys.argv) < 2:
        logging.error("Usage: python transcribe.py <audio_file>")
        sys.exit(1)

    audio_file = sys.argv[1]
    transcribe_audio(audio_file)
