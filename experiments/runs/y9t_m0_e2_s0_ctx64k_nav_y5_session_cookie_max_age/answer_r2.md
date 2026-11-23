다음 파일들을 수정했습니다:
- `src/flask/app.py`: `Flask.default_config`에 `"SESSION_COOKIE_MAX_AGE": None` 추가
- `src/flask/sessions.py`: `timedelta` import 추가, `SessionInterface`에 `get_cookie_max_age()` 메서드 구현 (타입 검증 및 `timedelta` → 초 단위 정수 변환), `SecureCookieSessionInterface.save_session()`에서 `max_age` 값을 `response.set_cookie()`에 전달하도록 수정