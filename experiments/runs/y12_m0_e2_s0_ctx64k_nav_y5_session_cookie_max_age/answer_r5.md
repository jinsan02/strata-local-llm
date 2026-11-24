수정 완료. 변경 사항을 요약하면:

1. **`src/flask/app.py`**: `Flask.default_config`에 `"SESSION_COOKIE_MAX_AGE": None` 추가
2. **`src/flask/sessions.py`**:
   - `from datetime import timedelta` import 추가
   - `SessionInterface`에 `get_cookie_max_age(self, app) -> t.Optional[int]` 메서드 추가:
     - `None` → `None` 반환
     - `bool` → `TypeError` (int의 서브클래스이므로 먼저 체크)
     - `timedelta` → `int(td.total_seconds())` 반환, 음수면 `ValueError`
     - `int` → 그대로 반환, 음수면 `ValueError`
     - 그 외 형 → `TypeError`
   - `SecureCookieSessionInterface.save_session`에서 `response.set_cookie()` 호출 시 `max_age=self.get_cookie_max_age(app)` 파라미터 추가
   - `delete_cookie`는 수정하지 않음 (기존 동작 유지)