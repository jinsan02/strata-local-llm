다음 2개 파일을 수정함:

1. **src/flask/app.py**: `Flask.default_config`에 `"SESSION_COOKIE_MAX_AGE": None` 추가
2. **src/flask/sessions.py**: 
   - `SessionInterface.get_cookie_max_age(self, app)` 메서드 추가 (설정값 검증 및 변환)
   - `SecureCookieSessionInterface.save_session()`에서 `response.set_cookie()` 호출 시 `max_age=self.get_cookie_max_age(app)` 파라미터 추가
   - `delete_cookie()`는 수정하지 않음 (기존 동작 유지)