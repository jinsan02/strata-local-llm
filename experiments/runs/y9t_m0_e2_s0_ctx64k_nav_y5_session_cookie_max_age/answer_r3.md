All tests pass. Here's a summary of the changes made:

1. **`src/flask/app.py`** — Added `"SESSION_COOKIE_MAX_AGE": None` to `default_config` (after `SESSION_COOKIE_SAMESITE`).

2. **`src/flask/sessions.py`** — Added `get_cookie_max_age(self, app) -> t.Optional[int]` method to `SessionInterface` that:
   - Returns `None` if the config value is `None`
   - Returns the `int` value as-is if it's a non-negative integer
   - Converts `datetime.timedelta` to `int(td.total_seconds())`
   - Raises `ValueError` for negative integers or timedeltas
   - Raises `TypeError` for `bool`, strings, floats, and other types

3. **`src/flask/sessions.py`** — Updated `SecureCookieSessionInterface.save_session()` to call `self.get_cookie_max_age(app)` and pass the result as `max_age` to `response.set_cookie()`. The `delete_cookie()` call is unchanged (no `max_age`).