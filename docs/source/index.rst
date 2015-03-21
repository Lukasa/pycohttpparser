pycohttpparser
==============

pycohttpparser is a Python wrapper library around the excellent
`picohttpparser`_ C library. It aims to provide a speedy C implementation of
the HTTP/1.1 parsing API used in the `hyper`_ project. Using CFFI, it supports
both CPython 2.7 and 3.4, and PyPy.

To get started with pycohttpparser, simply install it from the cheeseshop:

.. code-block:: bash

    $ pip install pycohttpparser

You'll need to make sure your system is set up for using CFFI. For more
information, `consult CFFI's documentation`_.

Then, you can start parsing your HTTP messages! For example:

.. code-block:: pycon

    >>> import pycohttpparser.api as p
    >>> message = socket.recv()
    >>> m = memoryview(data)
    >>> c = p.Parser()
    >>> r = c.parse_request(m)
    >>> r.method.tobytes()
    b'POST'
    >>> r.path.tobytes()
    b'/post'

Contents
--------

.. toctree::
   :maxdepth: 2

   api


.. _picohttpparser: https://github.com/h2o/picohttpparser
.. _hyper: http://hyper.readthedocs.org/
.. _consult CFFI's documentation: https://cffi.readthedocs.org/en/latest/#installation-and-status
