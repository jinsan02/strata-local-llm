수정 완료. 변경 내용 요약:

1. **`src/flask/app.py`**: `Flask.default_config`에 `"SESSION_COOKIE_MAX_AGE": None` 추가
2. **`src/flask/sessions.py`**:
   - `timedelta` import 추가
   - `SessionInterface`에 `get_cookie_max_age(self, app) -> t.Optional[int]` 메서드 추가 (값 검증: `None`→`None`, `int`→그대로, `timedelta`→초 단위 정수, 음수→`ValueError`, 기타 형→`TypeError`)
   - `SecureCookieSessionInterface.save_session`에서 `max_age = self.get_cookie_max_age(app)` 호출 후 `response.set_cookie()`에 `max_age` 파라미터 전달 (세션 비우기 시 `delete_cookie`는 변경 안 함)