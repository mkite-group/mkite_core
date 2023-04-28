import os
from tempfile import TemporaryDirectory


def run_in_tempdir(fn):
    """Wraps a given function `fn` so it runs inside a temporary directory
    that will be torn down after the function fn ends"""

    def wrapper(*args, **kwargs):
        workdir = os.getcwd()
        try:
            with TemporaryDirectory() as tmp:
                os.chdir(tmp)
                fn(*args, **kwargs)
                os.chdir(workdir)

        except Exception as e:
            os.chdir(workdir)
            raise e

    return wrapper
