# Modif by BE-Team

from io import BytesIO
import os
import ssl
import sys
import warnings
import base64
import time
from six.moves import urllib
import http.client as http_client
from .TTransport import TTransportBase
import six


class THttpClient(TTransportBase):
    """Http implementation of TTransport base."""

    def __init__(self, uri_or_host, port=None, path=None, cafile=None, cert_file=None, key_file=None, ssl_context=None):
        if port is not None:
            warnings.warn(
                "Please use the THttpClient('http{s}://host:port/path') constructor",
                DeprecationWarning,
                stacklevel=2)
            self.host = uri_or_host
            self.port = port
            assert path
            self.path = path
            self.scheme = 'http'
        else:
            parsed = urllib.parse.urlparse(uri_or_host)
            self.scheme = parsed.scheme
            assert self.scheme in ('http', 'https')
            if self.scheme == 'http':
                self.port = parsed.port or http_client.HTTP_PORT
            elif self.scheme == 'https':
                self.port = parsed.port or http_client.HTTPS_PORT
                self.certfile = cert_file
                self.keyfile = key_file
                self.context = ssl.create_default_context(cafile=cafile) if (cafile and not ssl_context) else ssl_context
            self.host = parsed.hostname
            self.path = parsed.path
            if parsed.query:
                self.path += '?%s' % parsed.query
        proxy = None
        self.realhost = self.realport = self.proxy_auth = None
        self.__wbuf = BytesIO()
        self.__rbuf = BytesIO()
        self.__http = None
        self.__http_response = None
        self.__timeout = None
        self.__custom_headers = None
        self.__time = time.time()
        

    def using_proxy(self):
        return self.realhost is not None

    def open(self):
        if self.scheme == 'http':
            self.__http = http_client.HTTPConnection(self.host, self.port,
                                                     timeout=self.__timeout)
        if self.scheme == 'https':
            self.__http = http_client.HTTPSConnection(self.host, self.port,
                                                      key_file=self.keyfile,
                                                      cert_file=self.certfile,
                                                      timeout=self.__timeout,
                                                      context=self.context)
            
    def close(self):
        self.__http.close()
        self.__http = None
        self.__http_response = None

    def isOpen(self):
        return self.__http is not None

    def setTimeout(self, ms):
        if ms is None:
            self.__timeout = None
        else:
            self.__timeout = ms / 1000.0

    def setCustomHeaders(self, headers):
        self.__custom_headers = headers

    def read(self, sz):
        return self.__rbuf.read(sz)

    def write(self, buf):
        self.__wbuf.write(buf)

    def flush(self):
        if not self.isOpen():
            self.open(); self.__time = time.time()
        elif time.time() - self.__time > 90:
            self.close(); self.open(); self.__time = time.time()
        data = self.__wbuf.getvalue()
        self.__wbuf.truncate(0)
        self.__wbuf.seek(0)
        self.__http.putrequest('POST', self.path)
        self.__http.putheader('Content-Type', 'application/x-thrift')
        self.__http.putheader('Content-Length', str(len(data)))
        if self.__custom_headers:
            for key, val in six.iteritems(self.__custom_headers):
                self.__http.putheader(key, val)
        self.__http.endheaders()
        self.__http.send(data)
        self.__rbuf = BytesIO(self.__http.getresponse().read())
