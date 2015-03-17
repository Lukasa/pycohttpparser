import picohttpparser.api as p

class Test(object):
    def test_basic_parsing(self):
        data = (
            b"POST /post HTTP/1.1\r\n"
            b"User-Agent: hyper\r\n"
            b"content-length: 2\r\n"
            b"host: http2bin.org\r\n"
            b"\r\n"
            b"hi"
        )
        m = memoryview(data)

        c = p.Parser()
        r = c.parse_request(m)

        assert r
        assert r.method.tobytes() == b'POST'
        assert r.path.tobytes() == b'/post'
        assert r.minor_version == 1

        expected_headers = [
            (b'User-Agent', b'hyper'),
            (b'content-length', b'2'),
            (b'host', b'http2bin.org'),
        ]

        assert len(expected_headers) == len(r.headers)

        for (n1, v1), (n2, v2) in zip(r.headers, expected_headers):
            assert n1.tobytes() == n2
            assert v1.tobytes() == v2

        assert r.consumed == len(data) - 2

    def test_basic_response_parsing(self):
        data = (
            b"HTTP/1.1 200 OK\r\n"
            b"Server: h2o\r\n"
            b"content-length: 2\r\n"
            b"Vary: accept-encoding\r\n"
            b"\r\n"
            b"hi"
        )
        m = memoryview(data)

        c = p.Parser()
        r = c.parse_response(m)

        assert r
        assert r.status == 200
        assert r.msg.tobytes() == b'OK'
        assert r.minor_version == 1

        expected_headers = [
            (b'Server', b'h2o'),
            (b'content-length', b'2'),
            (b'Vary', b'accept-encoding'),
        ]

        assert len(expected_headers) == len(r.headers)

        for (n1, v1), (n2, v2) in zip(r.headers, expected_headers):
            assert n1.tobytes() == n2
            assert v1.tobytes() == v2

        assert r.consumed == len(data) - 2
