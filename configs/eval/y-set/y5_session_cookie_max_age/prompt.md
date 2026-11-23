Flask 에 새 설정 `SESSION_COOKIE_MAX_AGE` 를 더하라. 세션 쿠키에 `Max-Age` 속성을 붙이는 설정이다.

- 기본값은 `None` 이고, 앱의 기본 설정(`Flask.default_config`)에 들어 있어야 한다. `None` 이면 지금과 똑같이 동작한다(쿠키에 `Max-Age` 없음).
- `SessionInterface` 에 메서드 `get_cookie_max_age(self, app) -> int | None` 를 더한다. 다른 `get_cookie_*` 메서드처럼 설정 값을 읽는다.
  - `None` → `None`
  - `int`(0 이상) → 그대로, `datetime.timedelta` → 초 단위 정수(`int(td.total_seconds())`)
  - 음수(정수 또는 timedelta) → `ValueError`
  - 그 밖의 형(문자열 · 실수 · `bool` 포함) → `TypeError`
- 기본 세션 인터페이스(`SecureCookieSessionInterface`)가 세션 쿠키를 설정할 때 이 값을 `max_age` 로 넘긴다. 영구 세션의 `Expires` 처리는 그대로 둔다(둘 다 붙을 수 있다). 세션을 비워 쿠키를 지울 때는 바꾸지 않는다.
- 기존 동작은 바뀌면 안 된다. 테스트 파일은 고치지 마라.
