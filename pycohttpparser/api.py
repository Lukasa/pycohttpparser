# -*- coding: utf-8 -*-
"""
pycohttpparser/api
~~~~~~~~~~~~~~~~~~

Defines the public API to pycohttpparser.
"""
from collections import namedtuple

from .backend import lib, ffi


Request = namedtuple(
    'Request', ['method', 'path', 'minor_version', 'headers', 'consumed']
)
Response = namedtuple(
    'Response', ['status', 'msg', 'minor_version', 'headers', 'consumed']
)

class ParseError(Exception):
    """
    An invalid HTTP message was passed to the parser.
    """

class Parser(object):
    """
    A single HTTP parser object. This object can parse HTTP requests and
    responses using picohttpparser.

    This object is not thread-safe, and it does maintain state that is shared
    across parsing requests. For this reason, make sure that access to this
    object is synchronized if you use it across multiple threads.
    """
    def __init__(self):
        # Store some instance variables. This represents essentially static
        # allocations that are used repeatedly in some of the parsing code.
        # This avoids the overhead of repeatedly allocating large chunks of
        # memory each time a parse is called.
        # Allocate all the data that will come out of the method.
        self._method = self._msg = ffi.new("char **")
        self._method_len = self._msg_len = ffi.new("size_t *")
        self._path = ffi.new("char **")
        self._path_len = ffi.new("size_t *")
        self._minor_version = ffi.new("int *")
        self._status = ffi.new("int *")

        # Allow space for 1000 headers. Anything more is clearly nonsense.
        self._header_count = 1000
        self._headers = ffi.new("struct phr_header [1000]")
        self._num_headers = ffi.new("size_t *", self._header_count)

    def parse_request(self, buffer):
        """
        Parses a single HTTP request from a buffer.

        :param buffer: A ``memoryview`` object wrapping a buffer containing a
            HTTP request.
        :returns: A :class:`Request <pycohttpparser.api.Request>` object, or
            ``None`` if there is not enough data in the buffer.
        """
        # Allocate function inputs
        buffer_size = ffi.cast("size_t", len(buffer))
        phr_buffer = ffi.new("char []", buffer.tobytes())
        last_len = ffi.cast("size_t", 0)

        # Reset the header count.
        self._num_headers[0] = self._header_count

        # Do the parse.
        pret = lib.phr_parse_request(
            phr_buffer,
            buffer_size,
            self._method,
            self._method_len,
            self._path,
            self._path_len,
            self._minor_version,
            self._headers,
            self._num_headers,
            last_len
        )

        # Check for insufficient data or parse errors.
        if pret == -2:
            return None
        elif pret == -1:
            raise ParseError("Invalid message")

        # If we got here we have a full request. We need to return useful
        # data. A useful trick here: all the returned char pointers are
        # pointers into buffer. This means we can use them as offsets and
        # return memoryviews to their data. Snazzy, right?
        method = b''
        path = b''
        minor_version = -1

        offset = self._method[0] - phr_buffer
        element_len = self._method_len[0]
        method = buffer[offset:offset+element_len]

        offset = self._path[0] - phr_buffer
        element_len = self._path_len[0]
        path = buffer[offset:offset+element_len]

        minor_version = self._minor_version[0]

        # We can create the Request object now, because all the scalar fields
        # are ready. We can put the headers into a list already hung from it.
        req = Request(method, path, minor_version, [], pret)

        for header in self._build_headers(phr_buffer, buffer):
            req.headers.append(header)

        return req

    def parse_response(self, buffer):
        """
        Parses a single HTTP response from a buffer.

        :param buffer: A ``memoryview`` object wrapping a buffer containing a
            HTTP response.
        :returns: A :class:`Response <pycohttpparser.api.Response>` object, or
            ``None`` if there is not enough data in the buffer.
        """
        # Allocate function inputs
        buffer_size = ffi.cast("size_t", len(buffer))
        phr_buffer = ffi.new("char []", buffer.tobytes())
        last_len = ffi.cast("size_t", 0)

        # Reset the header count.
        self._num_headers[0] = self._header_count

        # Do the parse.
        pret = lib.phr_parse_response(
            phr_buffer,
            buffer_size,
            self._minor_version,
            self._status,
            self._msg,
            self._msg_len,
            self._headers,
            self._num_headers,
            last_len
        )

        # Check for insufficient data or parse errors.
        if pret == -2:
            return None
        elif pret == -1:
            raise ParseError("Invalid message")

        # If we got here we have a full request. We need to return useful
        # data. A useful trick here: all the returned char pointers are
        # pointers into buffer. This means we can use them as offsets and
        # return memoryviews to their data. Snazzy, right?
        msg = b''
        status = 0
        minor_version = -1

        status = self._status[0]

        offset = self._msg[0] - phr_buffer
        element_len = self._msg_len[0]
        msg = buffer[offset:offset+element_len]

        minor_version = self._minor_version[0]

        # We can create the Request object now, because all the scalar fields
        # are ready. We can put the headers into a list already hung from it.
        req = Response(status, msg, minor_version, [], pret)

        for header in self._build_headers(phr_buffer, buffer):
            req.headers.append(header)

        return req

    def _build_headers(self, phr_buffer, orig_buffer):
        """
        Called by a parsing routine to build a collection of header names and
        values.
        """
        for index in range(self._num_headers[0]):
            header_struct = self._headers[index]
            name_index = header_struct.name - phr_buffer
            value_index = header_struct.value - phr_buffer
            name_len = header_struct.name_len
            value_len = header_struct.value_len

            name = orig_buffer[name_index:name_index+name_len]

            value = orig_buffer[value_index:value_index+value_len]

            yield (name, value)
