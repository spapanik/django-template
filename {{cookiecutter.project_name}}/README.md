# {{cookiecutter.project_name}}

[![code style: black][black_badge]][black_url]
[![build automation: yam][yam_badge]][yam_url]
[![Lint: ruff][ruff_badge]][ruff_url]

## Installation

### External tools

Most of the tools described here are optional, feel free to change them
if this suits your needs better.

From external services running, {{cookiecutter.project_name}} requires a
reverse proxy to be running, like nginx, and postgresql to be up and
running.

Because the server requires a specific python, that might not be the one
that the operating system uses, we recommend [pyenv] to be installed.
From python packages outside the virtualenv, the project also requires
[poetry] and [yamk] to be installed. There is the possibility to add them
in the virtualenv, but this may create conflicts with their dependencies.

The external tools that are assumed to be installed are:

-   [nginx]
-   [postgres]
-   [npm]
-   [yamk]
-   [pyenv]
-   [poetry]

We also assume that the postgres user has admin capabilities, and the
user can use them non-interactively.

To install the project you need to create and activate a virtual
environment, which can be done by:

### Create the certificate

As the site is HTTPS-only, there must be a certificate for it. There are
two good ways to do it:

-   Use [ngrok]
-   Use [easyCA]

Ngrok will use ngrok's certificate, and easyCA will create a root
certificate that you'll need to install, and then change your `nginx`
and `/etc/hosts` to use it. Both projects have good documentation that
you can follow.

### Creating the virtualenv

Although poetry does create a virtual env, all the commands assume the
existence of one, so it's better to actually create one. Assuming that
you're already in the cloned directory:

```console
$ pyenv install 3.12
$ pyenv shell 3.12
$ python -m venv ~/.local/share/venv/{{cookiecutter.project_name}}
$ . ~/.local/share/venv/{{cookiecutter.project_name}}
```

If everything is present, the only thing that needs to be done is to use
yam to install the project:

```console
$ yam install
```

## Usage

### Running the server

After a successful installation, try getting the server up by:

```console
$ yam runserver
```

trying to visit <http://localhost:8000> at this point should give an
error about "Invalid HTTP_HOST header". You should ask to be added in
the ngrok project, and there you can create your domain, to access the
project.

After the first installation, you can start the server by visiting the
cloned repo, and doing the following:

```console
$ . ~/.local/share/venvs/{{cookiecutter.project_name}}/bin/activate  # or the name of the virtualenv
$ yam runserver
```

There is hot reloading, and yam takes care of all the dependencies
issues. If there are unapplied migrations, you can apply them by:

```console
$ . ~/.local/share/venvs/{{cookiecutter.project_name}}/bin/activate  # or the name of the virtualenv
$ yam migrations
```

### Running the django shell

To run the local django shell, if you're inside the virtual environment,
you can just run:

```console
$ . ~/.local/share/venvs/{{cookiecutter.project_name}}/bin/activate  # or the name of the virtualenv
$ yam shell
```

### Formatting

To fix some simple linting errors, run:

```console
$ . ~/.local/share/venvs/{{cookiecutter.project_name}}/bin/activate  # or the name of the virtualenv
$ yam format
```

### Testing

To run the linting and the tests, run:

```console
$ . ~/.local/share/venvs/{{cookiecutter.project_name}}/bin/activate  # or the name of the virtualenv
$ yam lint
$ yam tests
```

### Updating

Updating the project can be done by yam:

```console
$ . ~/.local/share/venvs/{{cookiecutter.project_name}}/bin/activate  # or the name of the virtualenv
$ yam update
```

[black_badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black_url]: https://github.com/psf/black
[yam_badge]: https://img.shields.io/badge/build%20automation-yamk-success
[yam_url]: https://github.com/spapanik/yamk
[ruff_badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json
[ruff_url]: https://github.com/charliermarsh/ruff
[nginx]: https://www.nginx.com/resources/wiki/start/topics/tutorials/install/
[postgres]: https://www.postgresql.org/download/
[npm]: https://docs.npmjs.com/cli/
[yamk]: https://yamk.readthedocs.io/en/stable/installation.html
[pyenv]: https://github.com/pyenv/pyenv#installation
[poetry]: https://python-poetry.org/docs/
[ngrok]: https://ngrok.com/
[easyCA]: https://github.com/onepesu/easyCA
