수정을 완료했습니다. 변경 사항을 요약하면:

1. **`src/flask/app.py`**: `Flask.default_config`에 `"SESSION_COOKIE_MAX_AGE": None` 추가

2. **`src/flask/sessions.py`**:
   - `SessionInterface`에 `get_cookie_max_age(self, app) -> int | None` 메서드 추가. 설정값의 타입을 검증하고 `timedelta`를 초 단위 정수로 변환. `bool`은 `TypeError`, 음수는 `ValueError`, 다른 형식은 `TypeError` 발생
   - `SecureCookieSessionInterface.save_session`에서 `get_cookie_max_age(app)`를 호출해 `max_age`를 구하고 `response.set_cookie()`에 전달. 쿠키 삭제(`delete_cookie`)는 변경하지 않음