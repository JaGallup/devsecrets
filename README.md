# devsecrets: read secrets from environment variables or files

[![Linux build][tci]][tcl]
[![Windows build][aci]][acl]
[![Code coverage report][cci]][ccl]

## Why?

It would be nice if a developer could check out a project and immediately run
and debug it through their IDE.

For code that requires sensitive environment variables, you can't have that
because that would entail checking in secrets in run configurations.

## What?

devsecrets gets you just a little closer to the ideal by letting environment
variables point to files containing the sensitive information.

It doesn't help with creating, securing, or distributing those files.
 
## How?

Instead of reading `os.environ` directly, use `devsecrets.read_secret()` in your code.
For instance, if accessing a `DATABASE_URL` variable:
```
from devsecrets import read_secret

DATABASE_URL = read_secret('DATABASE_URL')
```

In development, set the `DATABASE_URL` environment variable to `@.secrets`.

Create a `.secrets` file in your project's directory, containing a line like
```
DATABASE_URL="driver://user:pass@host/dbname"
```

Have your version control system ignore your .secrets file.

## What about non-development environments?

Environment values that don't begin with the @-symbol are returned as-is by
`read_secret()`, so if you already have your secrets in environment variables
in production, there's no need to do anything differently.

If you do want to use secrets files in production, it probably makes sense
to point to them with absolute paths.

## Details

### Where exactly does `read_secret()` look for files?
 
If the filename is absolute, it is used as is.

Otherwise, `read_secret()` discovers where the code that called it lives and
starts there. Then it walks up the path all the way to the root.

### What is the format of the secrets files?

By example:
```
# comment
KEY1 = "value" #comment
key-2="#not-a-comment"

key_3 = "multiline\r\nvalue"

```

Currently, values must be quoted.

This is only because, for reasons of expediency,
a [TOML](https://github.com/toml-lang/toml) parser is used to parse these files.

### Installed code

Beware that how and where your code is installed matters because `read_secrets()`
considers where the calling code lives. If that's in a site-packages
directory under `/usr/lib` or `~/.local/share/virtualenvs` for instance,
then a `.secrets` file in `~/projects/myproject` won't be found.

This is ordinarily not a problem because you install your code with
`python setup.py install --develop` or `pip install --editable` so you run
your code from the same place where you checked it out.

### Installing

```
pip install devsecrets
```

### Running the tests

```
tox
```

## Versioning

We use [SemVer](http://semver.org/) for versioning [releases](https://github.com/JaGallup/devsecrets-precursor/releases). 

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details

## Related Projects

[python-dotenv](https://github.com/theskumar/python-dotenv)


[tci]: https://travis-ci.org/JaGallup/devsecrets.svg?branch=master
[tcl]: https://travis-ci.org/JaGallup/devsecrets

[aci]: https://ci.appveyor.com/api/projects/status/github/JaGallup/devsecrets-precursor?branch=master&svg=true
[acl]: https://ci.appveyor.com/api/projects/status/github/JaGallup/devsecrets-precursor

[cci]: https://codecov.io/gh/JaGallup/devsecrets/branch/master/graph/badge.svg
[ccl]: https://codecov.io/gh/JaGallup/devsecrets
