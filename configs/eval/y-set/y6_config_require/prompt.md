`flask.Config` 에 메서드 `require(self, *keys: str, allow_none: bool = False) -> dict[str, Any]` 를 더하라. 앱이 시작할 때 꼭 있어야 하는 설정을 한 번에 확인하는 용도다.

- 주어진 키들의 값을 담은 새 `dict` 를 돌려준다. 키 순서는 인자 순서 그대로다. 같은 키를 두 번 주면 한 번만 담는다.
- 없는 키가 있으면 `KeyError` 를 던진다. `allow_none` 이 거짓이면 값이 `None` 인 키도 없는 것으로 본다.
  - 예외 메시지(`exc.args[0]`)는 `"Missing required config keys: "` 뒤에 없는 키들을 **정렬해서** `", "` 로 이은 문자열이다. 예: `"Missing required config keys: A, B"`. 하나만 없어도 같은 형식이다.
  - 없는 키를 모두 모아 한 번에 알린다(첫 번째에서 멈추지 않는다).
- 키를 하나도 주지 않으면 `TypeError`, 문자열이 아닌 키가 있으면 `TypeError` 를 던진다.
- 설정 값은 바꾸지 않는다. 기존 동작은 바뀌면 안 된다. 테스트 파일은 고치지 마라.
