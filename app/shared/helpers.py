import glob
import os
from argon2 import PasswordHasher

password_hasher = PasswordHasher()


def hash_password(plain_password: str) -> str:
    return password_hasher.hash(plain_password)


def verify_password(hash: str, plain_password: str) -> bool:
    return password_hasher.verify(hash, plain_password)


def import_models(directory):
    module_paths = glob.glob(os.path.join(directory, "**/models.py"), recursive=True)
    for module_path in module_paths:
        if "venv" in module_path:
            continue  # Skip modules in the venv/ directory
        module_name = os.path.relpath(module_path, directory)[:-3].replace(
            os.path.sep, "."
        )  # Get module name

        module = __import__(module_name, fromlist=[""])  # Import module
        for name in dir(module):
            obj = getattr(module, name)
            if hasattr(
                obj, "__table__"
            ):  # Assuming models have a '__table__' attribute
                globals()[name] = obj
