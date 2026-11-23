다음과 같이 수정했습니다:

1. **`src/flask/app.py`**: `default_config`에 `"SESSION_COOKIE_MAX_AGE": None` 추가
2. **`src/flask/sessions.py`**:
   - `SessionInterface`에 `get_cookie_max_age(self, app)` 메서드 추가 — 설정 값을 읽고 `None`은 그대로, `int`는 그대로, `timedelta`는 초 단위 정수로 변환, 음수는 `ValueError`, 그 밖의 형(문자열·실수·`bool` 포함)은 `TypeError` 발생
   - `SecureCookieSessionInterface.save_session()`에서 `get_cookie_max_age(app)`를 호출해 `max_age` 인자로 `response.set_cookie()`에 전달