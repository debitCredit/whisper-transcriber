import os
import sys
import pytest
import logging
import builtins
from unittest.mock import patch, Mock, mock_open, ANY
from typing import BinaryIO

from openai import OpenAIError
from openai.error import Timeout

from transcriber.audio_transcription import initialize_openai_api_and_logging, transcribe_audio_from_file, transcribe_audio

# Initialize Mock objects
mock_openai_api = Mock()
mock_audio_file_obj = Mock()
mock_transcript = {'text': 'sample text'}


@pytest.fixture
def setup_logging():
    logging.getLogger().setLevel(logging.INFO)


# Test initialize_openai_api_and_logging function
def test_initialize_openai_api_and_logging_missing_api_key():
    with patch('sys.exit') as mock_exit, patch('logging.error') as mock_error:
        os.environ['OPENAI_API_KEY'] = ''
        initialize_openai_api_and_logging()
        mock_error.assert_called_with('Error - OPENAI_API_KEY not set')
        mock_exit.assert_called_with(1)


def test_initialize_openai_api_and_logging_successful_initialization(setup_logging):
    with patch('dotenv.load_dotenv'):
        os.environ['OPENAI_API_KEY'] = 'fake-key'
        initialize_openai_api_and_logging()
        assert logging.getLogger().getEffectiveLevel() == logging.INFO
        assert os.getenv('OPENAI_API_KEY') == 'fake-key'


def test_transcribe_audio_file_not_found(setup_logging):
    with patch('logging.error') as mock_log_error:
        with pytest.raises(FileNotFoundError):
            transcribe_audio('non_existent_file')
    mock_log_error.assert_called_with('Error accessing audio file %s: %s', 'non_existent_file', ANY)  # using ANY for dynamic error message


def test_transcribe_audio_openai_error(setup_logging):
    m_open = mock_open(read_data="fake audio data")
    
    with patch('builtins.open', m_open), \
         patch('openai.Audio.transcribe', side_effect=OpenAIError('OpenAI Error')), \
         patch('logging.error') as mock_log_error:
        
        with pytest.raises(OpenAIError, match='OpenAI Error'):
            transcribe_audio('fake_audio_file')

    mock_log_error.assert_called_with('Error calling OpenAI API: %s', ANY)  # using ANY for dynamic error message


def test_transcribe_audio_successful(setup_logging):
    m_open = mock_open(read_data="fake audio data")
    fake_transcription = "This is a fake transcription."

    with patch('builtins.open', m_open), \
         patch('openai.Audio.transcribe', return_value={"text": fake_transcription}):
        
        result = transcribe_audio('fake_audio_file')
        
    assert result == fake_transcription


def test_transcribe_audio_retry_on_openai_error(setup_logging):
    m_open = mock_open(read_data="fake audio data")
    
    expected_exception = Timeout('Retry')

    with patch('builtins.open', m_open), \
         patch('openai.Audio.transcribe', side_effect=[expected_exception, mock_transcript]), \
         patch('logging.error') as mock_log_error, \
         patch('logging.info') as mock_log_info:

        transcribe_audio('fake_audio_file')
    
        mock_log_error.assert_called_with('Error calling OpenAI API: %s', expected_exception)
        mock_log_info.assert_called_with(mock_transcript['text'])