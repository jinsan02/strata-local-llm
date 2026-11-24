수정 완료. 변경 내용 요약:

1. **`src/flask/app.py`**: `Flask.default_config`에 `"SESSION_COOKIE_MAX_AGE": None` 추가.

2. **`src/flask/sessions.py`**:
   - `SessionInterface`에 `get_cookie_max_age(self, app) -> int | None` 메서드 추가. 설정값을 읽고 `timedelta` → 초 단위 정수로 변환, `None` → `None`, 음수 → `ValueError`, bool/문자열/실수 등 → `TypeError` 처리.
   - `SecureCookieSessionInterface.save_session()`에서 `response.set_cookie()` 호출 시 `max_age=self.get_cookie_max_age(app)` 파라미터를 추가. 빈 세션 처리(`delete_cookie`)와 기존 동작은 그대로 유지.

기본값 `None`이므로 기존 동작(쿠키에 Max-Age 없음)이 그대로 유지됨.