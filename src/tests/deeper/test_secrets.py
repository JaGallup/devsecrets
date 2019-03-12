import os
from pathlib import Path
from unittest import mock

import pytest

from devsecrets import read_secret, SecretsError


local_testfile_path = str(
    Path(__file__).parents[1] / 'off-branch' / '.secrets-test-file-absolute')


@mock.patch.dict(os.environ, {'a': '@.secrets-test-file-good'})
def test_relative():
    a = read_secret('a')
    assert a == 'a'


@mock.patch.dict(os.environ, {'c': '@.secrets-test-file-good'})
def test_non_ascii_value():
    assert read_secret('c') == 'Sævör'


@mock.patch.dict(os.environ, {'Sævör': '@.secrets-test-file-good'})
def test_non_ascii_key():
    assert read_secret('Sævör') == 1


@mock.patch.dict(os.environ, {'d': '@.secrets-test-file-good'})
def test_unicode_escape_in_value():
    assert read_secret('d') == '\N{GRINNING FACE}'


@mock.patch.dict(os.environ, {'DB': '@.secrets-test-file-good'})
def test_trailing_space():
        assert read_secret('DB') == (
            'postgresql://user:YA0t%DY@ELDMT6v^Ehq3@r0&6IXQBS'
            '@ídéenna.example.com/fönkýdíbí ')


@mock.patch.dict(os.environ, {'a': '@.secrets-test-file-bad'})
def test_parse_error():
    with pytest.raises(SecretsError) as excinfo:
        read_secret('a')
    assert 'parse' in str(excinfo)


@mock.patch.dict(os.environ, {'a': '@.secrets-test-file-nonexistent'})
def test_missing_file():
    with pytest.raises(SecretsError) as excinfo:
        read_secret('a')
    assert 'parent' in str(excinfo)


def test_missing_from_environment():
    with pytest.raises(SecretsError) as excinfo:
        read_secret('not-in-environment')
    assert 'variable' in str(excinfo)


@mock.patch.dict(os.environ, {'not-in-file': '@.secrets-test-file-good'})
def test_missing_from_file():
    with pytest.raises(SecretsError) as excinfo:
        read_secret('not-in-file')
    assert 'define' in str(excinfo)


@mock.patch.dict(os.environ, {'a': '@{}'.format(local_testfile_path)})
def test_absolute():
    a = read_secret('a')
    assert a == 'b'
