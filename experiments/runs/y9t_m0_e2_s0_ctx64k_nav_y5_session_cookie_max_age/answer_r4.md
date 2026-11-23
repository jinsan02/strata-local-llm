기존 테스트 146개 모두 통과했습니다.

수정 내용 요약:

1. **`src/flask/app.py`**: `default_config` 딕셔너리에 `"SESSION_COOKIE_MAX_AGE": None` 추가 (기본값 `None`)

2. **`src/flask/sessions.py`** — `SessionInterface` 클래스:
   - `get_cookie_max_age(self, app) -> t.Optional[int]` 메서드 추가
   - `SESSION_COOKIE_MAX_AGE` 설정 값을 검증하여 반환:
     - `None` → `None`
     - `bool` → `TypeError`
     - `int` (음수) → `ValueError`, 그 외 → 그대로 반환
     - `timedelta` → `int(td.total_seconds())`, 음수 → `ValueError`
     - 기타 타입 → `TypeError`

3. **`src/flask/sessions.py`** — `SecureCookieSessionInterface.save_session`:
   - `get_cookie_max_age(app)` 호출 결과를 `max_age` 인자로 `response.set_cookie()`에 전달
   - 세션 삭제(`delete_cookie`) 때는 변경 없음
   - `expires` 처리는 그대로 유지 (둘 다 쿠키에 붙을 수 있음)