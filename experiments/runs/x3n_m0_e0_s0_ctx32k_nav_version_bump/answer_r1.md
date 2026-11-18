수정을 마쳤습니다. `src/packaging/version.py` 파일의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

구현 내용:
- `part` 가 `"major"`(인덱스 0), `"minor"`(인덱스 1), `"micro"`(인덱스 2) 중 하나인 경우 해당 인덱스의 release 요소를 +1 하고, 그 뒤의 모든 요소를 0 으로 설정
- 목표 인덱스가 release 길이보다 긴 경우 0 을 채워 확장
- epoch 는 `__replace__` 를 통해 유지, pre/post/dev/local 은 모두 None 으로 삭제 (버림)
- 그 밖의 `part` 값은 `ValueError` 발생
- 기존 객체는 불변이며 새 `Version` 인스턴스 반환