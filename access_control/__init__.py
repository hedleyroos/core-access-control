import os

orig_environ = dict(os.environ)
orig_environ["ALLOWED_API_KEYS"] = "test-api-key"
os.environ.update(orig_environ)