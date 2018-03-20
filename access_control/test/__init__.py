import os

if __name__ != "__main__":
    orig_environ = dict(os.environ)
    orig_environ["ALLOWED_API_KEYS"] = "test-api-key"
    os.environ.update(orig_environ)