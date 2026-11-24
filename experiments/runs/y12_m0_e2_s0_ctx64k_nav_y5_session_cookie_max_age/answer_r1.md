다음과 같이 수정했습니다.

1. **`src/flask/app.py`**: `Flask.default_config`에 `"SESSION_COOKIE_MAX_AGE": None` 추가.
2. **`src/flask/sessions.py`**:
   - `timedelta` import 추가.
   - `SessionInterface`에 `get_cookie_max_age` 메서드 추가 (값 검증 및 변환 처리).
   - `SecureCookieSessionInterface.save_session`에서 `response.set_cookie` 호출 시 `max_age=self.get_cookie_max_age(app)` 파라미터 전달.