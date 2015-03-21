# -*- coding: utf-8 -*-
"""
pycohttpparser/backend
~~~~~~~~~~~~~~~~~~~~~~

The CFFI layer in pycohttpparser.

Much of the code in this module was borrowed from Donald Stufft's excellent
article on distributing modules that use CFFI:
https://caremad.io/2014/11/distributing-a-cffi-project/
"""
import binascii
import os
import sys
import threading

from cffi import FFI
from cffi.verifier import Verifier


# This section is used for packaging up, as per 'Distributing a CFFI Project'.
def _create_modulename(cdef_sources, source, sys_version):
    """
    This is the same as CFFI's create modulename except we don't include the
    CFFI version.
    """
    key = '\x00'.join([sys_version[:3], source, cdef_sources])
    key = key.encode('utf-8')
    k1 = hex(binascii.crc32(key[0::2]) & 0xffffffff)
    k1 = k1.lstrip('0x').rstrip('L')
    k2 = hex(binascii.crc32(key[1::2]) & 0xffffffff)
    k2 = k2.lstrip('0').rstrip('L')
    return '_pycohttpparser_cffi_{0}{1}'.format(k1, k2)


def _compile_module(*args, **kwargs):
    raise RuntimeError(
        "Attempted implicit compile of a cffi module. All cffi modules should "
        "be pre-compiled at installation time."
    )


class LazyLibrary(object):
    def __init__(self, ffi):
        self._ffi = ffi
        self._lib = None
        self._lock = threading.Lock()

    def __getattr__(self, name):
        if self._lib is None:
            with self._lock:
                if self._lib is None:
                    self._lib = self._ffi.verifier.load_library()

        return getattr(self._lib, name)


CDEF = """
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

path = os.path.join(os.path.dirname(__file__), 'picohttpparser.c')
with open(path, 'r') as f:
    data = f.read()

SOURCE = "#include <sys/types.h>\n" + data

# FIXME: This all needs cleaning up.
ffi = FFI()
ffi.cdef(CDEF)
ffi.verifier = Verifier(
    ffi,
    SOURCE,
    include_dirs=[os.path.dirname(__file__)],
    modulename=_create_modulename(CDEF, SOURCE, sys.version)
)

# Patch the Verifier() instance to prevent CFFI from implicitly compiling the
# module
ffi.verifier.compile_module = _compile_module
ffi.verifier._compile_module = _compile_module

lib = LazyLibrary(ffi)
