pycohttpparser Python API
=========================

.. module:: hyper

This page documents pycohttpparser's Python API.

An important feature to note is that, wherever possible, pycohttpparser uses
`memoryview` objects to avoid copying data. The only objects that are not
returned as `memoryview`s are response status codes and the HTTP minor version
number.

.. autoclass:: pycohttpparser.api.Parser
   :inherited-members:

.. autoclass:: pycohttpparser.api.Request
   :inherited-members:

.. autoclass:: pycohttpparser.api.Response
   :inherited-members:

.. autoclass:: pycohttpparser.api.ParseError
