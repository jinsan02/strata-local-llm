수정 완료. 변경 사항을 요약하면:

1. **`src/flask/app.py`**: `Flask.default_config`에 `"SESSION_COOKIE_MAX_AGE": None` 추가
2. **`src/flask/sessions.py`**: `SessionInterface`에 `get_cookie_max_age(self, app) -> int | None` 메서드 추가 — 설정값을 검증해 정수 초 단위로 반환하고, `None`/음수/잘못된 형식에 대해 각각 `None`/`ValueError`/`TypeError` 처리
3. **`src/flask/sessions.py`**: `SecureCookieSessionInterface.save_session`에서 `response.set_cookie()` 호출 시 `max_age=self.get_cookie_max_age(app)` 파라미터 추가. 쿠키 삭제(`delete_cookie`)는 변경하지 않음.