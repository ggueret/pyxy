import os
import time
import errno
import fcntl
import falcon
import socket
import hashlib
import logging
import requests
from . import config


__VERSION__ = "0.0.1a0"


logger = logging.getLogger(__name__)


class AcquireTimeoutError(Exception):
    pass


class LockedFile(object):

    def __init__(self, path, *args, **kwargs):
        self._path = path
        self._fd = open(path, *args, **kwargs)

    def acquire(self, timeout=0):
        while True:
            try:
                return fcntl.flock(self._fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

            except IOError as exc:
                if exc.errno is not errno.EAGAIN:
                    raise

            time.sleep(0.1)
            timeout -= 0.1

        raise AcquireTimeoutError("timeout reached")

    def release(self):
        fcntl.flock(self._fd, fcntl.LOCK_UN)

    def read(self, size=0):
        return self._fd.read(size)

    def write(self, content):
        self._fd.write(content)

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, *exception):
        self.close()

    def close(self):
        self.release()
        self._fd.close()
        self._fd = None


class Cache(object):

    def __init__(self):
        self.base_dir = config.CACHE_DIR

    def abspath(self, name):
        return os.path.join(self.base_dir, name)

    def copy_fileobj(self, source, dest, chunk_size=16 * 1024):
        while True:
            chunk = source.read(chunk_size)

            if not chunk:
                break

            dest.write(chunk)

    def set(self, name, fd, chunk_size=16 * 1024):
        tmp_path = self.abspath('.' + name)

        with LockedFile(tmp_path, "wb") as tmp_fd:
            self.copy_fileobj(fd, tmp_fd)

        os.rename(tmp_path, self.abspath(name))

    def get(self, name, default=None):
        value = default
        try:
            value = LockedFile(self.abspath(name), "rb")
        except FileNotFoundError:
            pass

        return value


class PyXy(object):

    def __init__(self):
        self.cache = Cache()
        self.hostname = socket.gethostname()

    def generate_hash(self, uri):
        return hashlib.sha1(uri.encode('utf-8')).hexdigest()

    def on_get(self, request, response, urlpath):
        cache_key = self.generate_hash(request.uri)
        from_cache = self.cache.get(cache_key)

        if not from_cache:
            logger.info("MISS: %s", request.uri)
            with requests.get(request.uri, stream=True) as remote:
                if remote.status_code == requests.codes.ok:
                    remote.raw.decode_content = True
                    self.cache.set(cache_key, remote.raw)
                    response.stream = self.cache.get(cache_key)

                else:
                    response.stream = remote

                response.status = getattr(falcon, f'HTTP_{str(remote.status_code)}')
                response.set_header('X-Cache', "MISS from pyxy")
                response.set_header('X-Cache-Lookup', "MISS from pyxy")
        else:
            logger.info(" HIT: %s", request.uri)
            response.stream = from_cache
            response.status = falcon.HTTP_200
            response.set_header('X-Cache', "HIT from pyxy")
            response.set_header('X-Cache-Lookup', "HIT from pyxy")


logging.config.dictConfig(config.LOGGING)

app = falcon.API()
app.add_route('/{urlpath}', PyXy())
