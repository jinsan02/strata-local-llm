수정 완료. 변경 사항을 요약하면:

1. **`src/flask/app.py`**: `Flask.default_config`에 `"SESSION_COOKIE_MAX_AGE": None` 추가
2. **`src/flask/sessions.py`**: 
   - `SessionInterface`에 `get_cookie_max_age(self, app) -> int | None` 메서드 추가 (`None` → `None`, `timedelta` → 초 단위 정수, 음수 → `ValueError`, 그 밖의 형 → `TypeError`)
   - `SecureCookieSessionInterface.save_session()`에서 `max_age = self.get_cookie_max_age(app)`를 호출하고 `response.set_cookie()`의 `max_age` 인자로 전달. 쿠키 삭제 경로(`delete_cookie`)는 변경하지 않음