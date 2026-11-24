수정 완료. 변경 사항을 요약하면:

1. **`src/flask/app.py`**: `Flask.default_config`에 `"SESSION_COOKIE_MAX_AGE": None` 추가.

2. **`src/flask/sessions.py`**:
   - `from datetime import timedelta` import 추가.
   - `SessionInterface`에 `get_cookie_max_age(self, app) -> int | None` 메서드 추가. 설정값을 검증하고 변환(정수 그대로, timedelta→초 정수, bool/기타 형→TypeError, 음수→ValueError, None→None).
   - `SecureCookieSessionInterface.save_session()`에서 `response.set_cookie()` 호출 시 `max_age=self.get_cookie_max_age(app)` 파라미터를 추가. `delete_cookie()`는 변경하지 않음.