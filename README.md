# devsecrets: read secrets from environment variables or files

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

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details

## Related Projects

[python-dotenv](https://github.com/theskumar/python-dotenv)
