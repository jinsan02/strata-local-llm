다음 파일들을 수정했습니다:

1. **`src/flask/app.py`**: `Flask.default_config`에 `"SESSION_COOKIE_MAX_AGE": None`을 추가했습니다.
2. **`src/flask/sessions.py`**:
   - `SessionInterface`에 `get_cookie_max_age(app)` 메서드를 추가했습니다. 설정 값을 읽어 `timedelta`를 초 단위로 변환하거나, 유효하지 않은 타입/음수일 경우 예외를 발생시킵니다.
   - `SecureCookieSessionInterface.save_session`에서 `set_cookie` 호출 시 `max_age` 인자를 추가했습니다.