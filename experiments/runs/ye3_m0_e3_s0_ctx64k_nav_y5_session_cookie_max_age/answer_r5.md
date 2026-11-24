수정 사항을 요약하면:

1. **`src/flask/app.py`**: `Flask.default_config`에 `"SESSION_COOKIE_MAX_AGE": None` 추가
2. **`src/flask/sessions.py`**: 
   - `SessionInterface`에 `get_cookie_max_age(self, app) -> int | None` 메서드 추가. 설정 값을 읽고 `None`/`int`/`timedelta`를 처리하며, 음수는 `ValueError`, 그 밖의 형은 `TypeError`를 발생시킴
   - `SecureCookieSessionInterface.save_session`에서 `get_cookie_max_age(app)`를 호출해 `max_age` 값을 구하고 `response.set_cookie()`의 `max_age` 인자에 전달. 세션 비우기(`delete_cookie`)는 변경하지 않음