import inspect
import os
from pathlib import Path

import toml


__all__ = ['read_secret', 'SecretsError']


class SecretsError(Exception):
    pass


def read_secret(name):
    v = os.environ.get(name)
    if v is None:
        raise SecretsError('Missing environment variable {}'.format(name))

    if not v.startswith('@'):
        return v

    secrets_filename = Path(v[1:])
    if not secrets_filename.is_absolute():
        outer_frame = inspect.currentframe().f_back
        caller_filename, *_ = inspect.getframeinfo(outer_frame)
        caller_directory = Path(caller_filename).parent
        secrets_filename = _find_secrets_file(secrets_filename, caller_directory)

    return _read_secret_from_file(name, secrets_filename)


def _find_secrets_file(filename, directory):
    given_directory = directory
    while 1:
        pathname = directory / filename
        if pathname.exists():
            return pathname
        if str(directory.parent) == str(directory):
            raise SecretsError('No file named {filename} found in {given_directory} or any of its parents'.format(
                filename=filename, given_directory=given_directory))
        directory = directory.parent


def _read_secret_from_file(name, secrets_filename):
    try:
        data = toml.load(secrets_filename)
    except toml.TomlDecodeError as e:
        raise SecretsError('Secrets file {} cannot be parsed as TOML'.format(secrets_filename)) from e

    if name in data:
        return data[name]
    else:
        raise SecretsError('Secrets file {secrets_filename} does not define {name}'.format(
            secrets_filename=secrets_filename, name=name))
