What I changed:

In `src/flask/blueprints.py`, I added a check in the `Blueprint.__init__` method to raise a `ValueError` when the `name` parameter is empty (empty string or falsy). The new validation runs before the existing check for a dot character in the name. This ensures that creating a Blueprint with an empty name fails early with a clear error message, addressing issue #4944.