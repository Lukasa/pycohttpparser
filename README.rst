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

For more information, see `the documentation`_.


.. _picohttpparser: https://github.com/h2o/picohttpparser
.. _hyper: http://hyper.readthedocs.org/
.. _consult CFFI's documentation: https://cffi.readthedocs.org/en/latest/#installation-and-status
.. _the documentation: http://pycohttpparser.readthedocs.org/

License
-------

The Python wrapper library here is licensed under the MIT license. See LICENSE
for more details.

The original picohttpparser C code, which is included in this project in its
entirety, is licensed under the MIT license. See the source files or the
NOTICES file for more details.

Maintainers
-----------

The python wrapper library is maintained by Cory Benfield.

picohttpparser is maintained by the picohttpparser team: see NOTICES for more.
