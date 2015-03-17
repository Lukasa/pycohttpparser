# -*- coding: utf-8 -*-
"""
picohttpparser/backend
~~~~~~~~~~~~~~~~~~~~~~

The CFFI layer in picohttpparser.
"""
import os

from cffi import FFI

# FIXME: This all needs cleaning up.
ffi = FFI()

ffi.cdef(
    """
    struct phr_header {
      const char* name;
      size_t name_len;
      const char* value;
      size_t value_len;
    };

    int phr_parse_request(const char* buf, size_t len, const char** method,
                          size_t* method_len, const char** path,
                          size_t* path_len, int* minor_version,
                          struct phr_header* headers, size_t* num_headers,
                          size_t last_len);

    int phr_parse_response(const char* _buf, size_t len, int *minor_version,
                  int *status, const char **msg, size_t *msg_len,
                  struct phr_header* headers, size_t* num_headers,
                  size_t last_len);

    int phr_parse_headers(const char* buf, size_t len, struct phr_header* headers,
                          size_t* num_headers, size_t last_len);

    struct phr_chunked_decoder {
      size_t bytes_left_in_chunk; /* number of bytes left in current chunk */
      char consume_trailer; /* if trailing headers should be consumed */
      char _hex_count;
      char _state;
    };

    ssize_t phr_decode_chunked(struct phr_chunked_decoder *decoder, char *buf,
                               size_t *bufsz);

    """
)
path = os.path.join(os.path.dirname(__file__), 'picohttpparser.c')
with open(path, 'r') as f:
    data = f.read()

lib = ffi.verify(
    """
    #include <sys/types.h>
    """ + data,
    include_dirs = [os.path.dirname(__file__)],
)
