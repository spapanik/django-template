===
bmk
===

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
  :alt: Code style
  :target: https://github.com/psf/black

Installation
------------

External tools
^^^^^^^^^^^^^^

Most of the tools described here are optional, feel free to change them if this suits your needs better.

From external services running, bmk requires a reverse proxy to be running, like nginx, and postgresql to be up and running.

Because the server requires a specific python, that might not be the one that the operating system uses, we recommend `pyenv`_ to be installed.
From python packages outside the virtualenv, the project also requires `poetry`_ and `yamk`_ to be installed. There is the possibility to add them in the virtualenv, but this may create conflicts with their dependencies.

The external tools that are assumed to be installed are:

* `dart-sass`_
* `nginx`_
* `postgres`_
* `yarn`_
* `yamk`_
* `pyenv`_
* `poetry`_


We also assume that the postgres user has admin capabilities, and the user can use them non-interactively.

To install the project you need to create and activate a virtual environment, which can be done by:

Create the certificate
^^^^^^^^^^^^^^^^^^^^^^

As the site is HTTPS-only, there must be a certificate for it. You may use `easyCA`_ to create it.

Creating the virtualenv
^^^^^^^^^^^^^^^^^^^^^^^

Although poetry does create a virtual env, all the commands assume the existence of one, so it's better to actually create one. Assuming that you're already in the cloned directory:

.. code-block:: console

    $ pyenv install 3.10.0
    $ pyenv shell 3.10.0
    $ python -m venv ~/.local/share/venv/bmk
    $ . ~/.local/share/venv/bmk


If everything is present, the only thing that needs to be done is to use yam to install the project:

.. code-block:: console

    $ yam install

Usage
-----

Running the server
^^^^^^^^^^^^^^^^^^

After a successful installation, try getting the server up by:

.. code-block:: console

    $ django-admin runserver_plus

trying to visit http://localhost:8000 at this point should give an error about "Invalid HTTP_HOST header". You should ask to be added in the ngrok project, and there you can create your domain, to access the project.

After the first installation, you can start the server by visiting the cloned repo, and doing the following:

.. code-block:: console

    $ . ~/.local/share/venvs/bmk/bin/activate  # or the name of the virtualenv
    $ django-admin runserver_plus

There is hot reloading, and yam takes care of all the dependencies issues. If there are unapplied migrations, you can apply them by:

.. code-block:: console

    $ yam migrations

Running the django shell
^^^^^^^^^^^^^^^^^^^^^^^^

To run the local django shell, if you're inside the virtual environment, you can just run:

.. code-block:: console

    $ . ~/.local/share/venvs/bmk/bin/activate  # or the name of the virtualenv
    $ django-admin shell_plus

Formatting
^^^^^^^^^^

To fix some simple linting errors, run:

.. code-block:: console

    $ yam format

Testing
^^^^^^^

To run the linting and the tests, run:

.. code-block:: console

    $ yam lint
    $ yam tests

Updating
^^^^^^^^

Updating the project can be done by yam:

.. code-block:: console

    $ yam update


.. _`dart-sass`: https://sass-lang.com/install
.. _`nginx`: https://www.nginx.com/resources/wiki/start/topics/tutorials/install/
.. _`postgres`: https://www.postgresql.org/download/
.. _`yarn`: https://classic.yarnpkg.com/lang/en/docs/install/
.. _`yamk`: https://yamk.readthedocs.io/en/stable/installation.html
.. _`pyenv`: https://github.com/pyenv/pyenv#installation
.. _`poetry`: https://python-poetry.org/docs/
.. _`easyCA`: https://github.com/onepesu/easyCA
