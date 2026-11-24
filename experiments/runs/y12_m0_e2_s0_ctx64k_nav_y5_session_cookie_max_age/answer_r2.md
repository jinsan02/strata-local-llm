수정 완료. 변경 내용:

1. **`src/flask/app.py`**: `Flask.default_config`에 `"SESSION_COOKIE_MAX_AGE": None` 추가
2. **`src/flask/sessions.py`**: `SessionInterface`에 `get_cookie_max_age(self, app) -> t.Optional[int]` 메서드 추가. 설정값이 `None`이면 `None`, `int`면 그대로 반환, `timedelta`면 초 단위 정수로 변환, 음수면 `ValueError`, 그 밖의 형(문자열·실수·`bool` 포함)이면 `TypeError` 발생. `bool` 체크를 `int` 체크 전에 둠.
3. **`src/flask/sessions.py`**: `SecureCookieSessionInterface.save_session()`에서 `get_cookie_max_age(app)` 호출 결과를 `response.set_cookie()`의 `max_age` 인자로 전달. 쿠키 삭제 시(`delete_cookie`)는 변경하지 않음.