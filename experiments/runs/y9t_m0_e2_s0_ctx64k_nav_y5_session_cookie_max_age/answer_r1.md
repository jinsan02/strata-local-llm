기존 테스트가 모두 통과했습니다. 수정 사항을 요약하면:

1. **`src/flask/app.py`**: `Flask.default_config`에 `"SESSION_COOKIE_MAX_AGE": None` 추가
2. **`src/flask/sessions.py`**: `SessionInterface`에 `get_cookie_max_age(self, app) -> int | None` 메서드 추가 — `None`은 `None` 반환, `int`(0 이상)은 그대로, `timedelta`는 초 단위 정수로 변환, 음수는 `ValueError`, 그 밖의 형(문자열·실수·`bool` 포함)은 `TypeError`
3. **`src/flask/sessions.py`**: `SecureCookieSessionInterface.save_session()`에서 `response.set_cookie()` 호출 시 `max_age=self.get_cookie_max_age(app)` 파라미터를 추가 (세션 비우기 시 `delete_cookie`는 변경 안 함)