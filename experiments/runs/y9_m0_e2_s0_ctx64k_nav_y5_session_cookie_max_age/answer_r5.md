수정 내용을 요약하면:

1. **`src/flask/app.py`**: `Flask.default_config`에 `"SESSION_COOKIE_MAX_AGE": None` 추가

2. **`src/flask/sessions.py`**:
   - `SessionInterface`에 `get_cookie_max_age(self, app) -> t.Optional[int]` 메서드 추가. 설정값을 읽어 `None` → `None`, `timedelta` → 초 단위 정수, 음수 정수 → `ValueError`, 그 밖의 형(문자열·실수·`bool` 포함) → `TypeError` 처리
   - `SecureCookieSessionInterface.save_session()`에서 `response.set_cookie()` 호출 시 `max_age=self.get_cookie_max_age(app)` 파라미터 추가. 세션 삭제(`delete_cookie`)는 수정하지 않음