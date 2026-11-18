What I changed:

In `src/flask/blueprints.py`, inside the `Blueprint.__init__` method, I added a check that raises a `ValueError` with the message `"'name' must be a non-empty string."` when the `name` parameter is empty (e.g., an empty string). This prevents blueprints from being created with an invalid empty name, which would cause issues later.