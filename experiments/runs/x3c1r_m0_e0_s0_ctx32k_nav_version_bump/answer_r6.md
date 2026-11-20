수정 내용을 요약하면 다음과 같다:

**파일:** `src/packaging/version.py`

**변경 내용:** `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다. 
- `part` 가 `"major"`/`"minor"`/`"micro"` 일 때 해당 인덱스의 release 숫자를 1 올리고 이후 숫자를 모두 0 으로 한다.
- 요청한 자리가 현재 release 길이보다 긴 경우(예: `release=(1,)`에 `micro`) 필요한 길이까지 0 을 채워 끝을 1 로 만든다.
- epoch 는 유지되고, pre/post/dev/local 은 모두 버린다. (기존 `__replace__` 재사용)
- 유효하지 않은 `part` 값(대소문자 포함)은 `ValueError` 를 던진다.