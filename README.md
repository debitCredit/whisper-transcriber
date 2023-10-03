# Whisper Transcriber

Whisper Transcriber is a Python application that transcribes audio files using the OpenAI Whisper ASR API. 
This repository contains the necessary source code and related files for the Whisper Transcriber.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Functionality Overview](#functionality-overview)
- [Error Handling and Retries](#error-handling-and-retries)
- [Tests](#tests)
- [Linting](#linting)
- [Contribute](#contribute)
- [License](#license)

## Installation

To set up this project:

1. Make sure you have Python 3.11 installed.
2. Clone the repository:

```bash
git clone https://github.com/yourusername/whisper-transcriber.git
cd whisper-transcriber
```

3. Install the required dependencies using poetry:

```bash
poetry install
```


## Usage
To use the transcriber, ensure you have the necessary environment variable set up: OPENAI_API_KEY. 
Then, you can utilize the audio_transcription.py script within the transcriber directory.

Run the transcriber with:

```bash
python -m transcriber.audio_transcription <path_to_file>
```

Example usage:

```bash
python -m transcriber.audio_transcription /whisper_transcriber/jfk.flac
INFO:root:Opened audio file: /whisper_transcriber/jfk.flac
INFO:root:Transcribing audio...
INFO:root:And so my fellow Americans, ask not what your country can do for you, ask what you can do for your country.
```

The repository includes a short audio file for testing: `jfk.flac`

## Functionality Overview

- **Initialization**: Before any transcription, the script initializes OpenAI's API key from environment variables and sets up basic logging.

- **Transcription**: The script provides a function to transcribe audio directly from a file object. 
This function communicates with the OpenAI API, attempting to convert the audio to text. 
If successful, it logs and returns the transcribed text.

- **File Handling**: The primary function handles reading from a file and then uses the previously mentioned function to transcribe it.

## Error Handling and Retries

The script employs a retry mechanism using the `tenacity` library for the following OpenAI exceptions:

- Timeout
- APIError
- APIConnectionError
- RateLimitError
- ServiceUnavailableError

This mechanism waits for a random exponential amount of time with a maximum of 60 seconds, retrying a total of 3 times before failing and reraising the error.

## Tests

The `whisper-transcriber` repository is equipped with unit tests to validate the core functionalities. 
To run the tests, follow these steps:

1. Ensure you're in the root directory of the cloned repository.
2. Run the tests using the following command:

```bash
poetry run pytest
```
Upon execution, pytest will discover and run all tests in the tests directory, and you will see the results in your terminal.

## Linting

Linting helps maintain a consistent code style and catches potential issues. 
The project uses tools like `black`, `pylint`, and `mypy` for linting and type-checking.

To lint the code, follow these steps:

1. Ensure you're in the root directory of the cloned repository.
2. Run the linting tasks using:

```bash
poetry run task lint
```
This command checks the code format with black, analyzes the source with pylint, and verifies type annotations with mypy.


## Contribute

1. Ensure that you adhere to the coding standards provided by the linting tools.
2. Write unit tests for new functionality or bug fixes.
3. Always run tests before submitting a pull request.

## License

Whisper Transcriber is licensed under the terms provided in the LICENSE.txt file.
