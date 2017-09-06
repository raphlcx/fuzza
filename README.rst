=====
Fuzza
=====

.. image:: https://img.shields.io/travis/Raphx/fuzza/master.svg?style=flat-square
    :target: https://travis-ci.org/Raphx/fuzza

.. image:: https://img.shields.io/codecov/c/github/Raphx/fuzza/master.svg?style=flat-square
  :target: https://codecov.io/gh/Raphx/fuzza

.. image:: https://img.shields.io/github/license/Raphx/fuzza.svg?style=flat-square
  :target: LICENSE

A generic template-based fuzzer.

.. contents:: :local:

Why another fuzzer
==================

Fuzza attempts to make fuzzing as simple and configurable as possible. It is:

* Data independent. Fuzza does not generate its own data. It is responsible for only carrying out fuzzing sessions.
* Platform agnostic. It aims to be used to fuzz all kind of protocols, and not constrained to fuzz only a certain few.
* Template based. Fuzzing grammar is defined in a plain text template file, without requiring any application-specific template construction grammar.
* Configuration driven. Fuzz parameters are specified in a configuration file, allowing more fine-grained controls without touching the source.

How it works
============

Fuzza carries out fuzzing based on the configurations specified in its YAML configuration file, named ``fuzza.cfg.yml``. It works sequentially as follows:

1. Read data from data files
2. Read templates from template files
3. Apply necessary transformations to data
4. For each of the template found, render each with all the data available, resulting in a payload individually
5. Dispatch the payload to the fuzz target

Installing
==========

Installation can be done on the machine locally via Python package installation, or skipped entirely through the use of Docker image.

Local setup
-----------

Ensure Python >= 3.6 is installed, then execute the following commands::

    git clone https://github.com/Raphx/fuzza.git

    cd fuzza

    python setup.py install

Note: For installation on Windows, ensure that VC++ build tools (or Visual Studio) is installed. You can get it `here <http://landinghub.visualstudio.com/visual-cpp-build-tools>`_.

If installation is successfull, the program name and version should be printed out on the following command::

    fuzza --version

Using Docker
------------

Ensure Docker is installed.

Build the image::

    docker build . -t fuzza

Now run it::

    docker run --rm -v $(pwd):/app fuzza

Arguments can be supplied by appending them to the execution command::

    docker run --rm -v $(pwd):/app fuzza --version

Commands
========

Fuzza is a CLI application. It has a number of subcommands, as documented below.

``init``
--------

The ``init`` subcommand generates a configuration file to be consumed by the ``fuzz`` command. It takes a number of options,

::

    Usage: fuzza init [OPTIONS]

      Create a fuzzer configuration file.

    Options:

      --host <host>                   The hostname or IP address of target to fuzz.

      --port <port>                   The port of target to fuzz.

      --data-path <path>              Path containing fuzz data. Support glob
                                      patterns.

      -c, --data-chunk                Read each fuzz data file in chunk, instead
                                      of line-by-line. [False]

      --template-path [path]          Path containing template files. Support glob
                                      patterns. []

      --dispatcher [dispatcher]       Type of dispatcher to use. [tcp]

      -r, --dispatcher-reuse          Enable dispatcher connection reuse. [False]

      --transformer [transformer[, ...]]
                                      List of transformations to be sequentially
                                      applied to fuzz data. []

      --protocol [protocol]           Type of communication protocol. [textual]

      --help                          Show this message and exit.

For a minimal configuration, Fuzza requires only host, port and data path for it to work. By not specifying any template, fuzz data is directly dispatched to the target, without being rendered in a template.

If multiple templates are found, each template will be iterated through to individually render all the fuzz data.

In the case of unspecified configuration:

* Data chunk mode reading defaults to ``False``
* Template defaults to ``None``, meaning no templates are to be used
* Dispatcher defaults to using TCP dispatcher
* Dispatcher connection reuse defaults to ``False``
* Transformer defaults to an empty list
* Protocol defaults to textual

``fuzz``
--------

The fuzz command does not have any options available. It takes the configuration file, either generated from the ``init`` subcommand, or manually hand crafted, and start a fuzz session based on the configurations.

::

    Usage: fuzza fuzz [OPTIONS]

      Execute the fuzzer.

    Options:

      --help  Show this message and exit.

Architecture
============

Fuzza itself is a fuzzing application, which is broken down into a few components:

* **Data** - Read fuzz data from external sources
* **Transformer** - Apply transformation to fuzz data, e.g. base64 encoding, hex encoding
* **Templater** - Consume template files, render fuzz data to templates
* **Protocol adapter** - Adapt payload to communication protocol type
* **Dispatcher** - Establish connection to fuzz target and dispatch fuzz payload

Templating
==========

Templating is very simple as of current. The string ``replace()`` method is used to render data into a place holder, denoted as ``$fuzzdata`` in the template.

Artifacts
=========

Fuzza produces a single log file in the same directory where the CLI is invoked. The log file produced is named ``fuzza.log``.

Examples
========

Fuzzing HTTP ``Host`` header
----------------------------

Scenario: A simple HTTP server running on localhost at port 8000, with data files located in the ``data`` directory.

Given the template file named ``sample.template``::

    GET / HTTP/1.1

    Host: $fuzzdata

and the configuration file ``fuzza.cfg.yml``::

    host: 127.0.0.1
    port: 8000
    data_path: data/*
    template_path: sample.template

In the directory containing the template, configuration file, and ``data`` directory, run::

    fuzza fuzz

Fuzzing a binary protocol
-------------------------

Scenario: A hex string template is prepared to fuzz a binary protocol, served by a service on port 4343 on localhost, with data files located in the ``data`` directory.

Given the template file named ``sample2.template``::

    31 32 33 $fuzzdata

and the configuration file ``fuzza.cfg.yml``::

    host: 127.0.0.1
    port: 4343
    data_path: data/*
    template_path: sample2.template
    transformation:
     - hex
    protocol: binary

In the containing directory, run::

    fuzza fuzz

Here's what happens sequentially:

1. Data is read from the ``data/*`` directory
2. Hex encoding transformation is applied to all the data. This is required since the template is prepared in hex string format.
3. The transformed data is rendered to the template by replacing the ``$fuzzdata`` place holder, thereby producing the fuzz payload.
4. Since communication protocol type is binary, the protocol adapter kicks in to convert the hex string payload to its binary value representation.
5. The payload is then dispatched.

Built-in modules
================

Fuzza provides some built-in modules for some of its components. Custom modules can also be provided, check `Extensibility`_.

Below are the modules provided for each of the component:

Transformer

* base64
* hex

Dispatcher

* tcp

Protocol adapter:

* textual
* binary

Extensibility
=============

Fuzza is made to support customization. The components which can be customized are:

* Transformer
* Dispatcher
* Protocol adapter

Customization is as simple as creating a Python module, and implementing a specific function in the module.

Transformer
-----------

Transformer module requires one function implementation:

* ``transform(data: List[str]) -> List[str]`` - Transformation to apply on data. Accepts a list of data. Returns a list of transformed data.

Example, a module named ``my_transformer.py``::

    def transform(data):

      transformed_data = copy.deepcopy(data)

      # some transformation to the data
      # ...

      return transformed_data

Now, specify to use the transformer in the configuration file::

    host: 127.0.0.1
    port: 80
    transformer:
     - my_transformer

Dispatcher
----------

Dispatcher requires three function implementations:

* ``connect(target: Tuple[str, int]]) -> Any`` - Specify how connection should be set up. Argument is a tuple containing hostname and port. Returns a connection object.
* ``dispatch(con: Any, payload: str) -> str`` - Specify how payloads should be dispatched. Accepts a connection object and the payload. Returns the received response from after the dispatching.
* ``close(con: Any) -> None`` - Specify how connection should be terminated. Accepts a connection object.

Example, a module named ``my_dispatcher.py``::

    def connect(target):
        con = create_connection(target)
        return con

    def dispatch(con, payload):
        response = con.send(payload)
        return response

    def close(con):
        con.close()

Specify in configuration file::

    host: 127.0.0.1
    port: 80
    dispatcher: my_dispatcher

Protocol adapter
----------------

The protocol adapter require one function implementation:

* ``adapt(payload: str) -> str`` - Adaptation of payload. Accepts a payload string. Returns an adapted payload string.

Example, a module named ``my_protocol.py``::

    def adapt(payload):
        adapted = convert_to_hex(payload)
        return adapted

Specify in configuration file::

    host: 127.0.0.1
    port: 80
    protocol: my_protocol
