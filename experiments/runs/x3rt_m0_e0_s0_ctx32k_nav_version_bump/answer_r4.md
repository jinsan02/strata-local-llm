`src/packaging/version.py` 파일의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

메서드는 `micro` 프로퍼티 뒤에 삽입되었습니다. 주요 동작:
- `part` 가 `"major"`, `"minor"`, `"micro"` 중 하나가 아니면 `ValueError` 던짐
- 지정된 release 인덱스를 1 증가시키고, 그 뒤의 모든 인덱스를 0 으로 설정
- release 길이를 유지 (요청 인덱스가 없으면 0 으로 패딩)
- epoch 유지, pre/post/dev/local 제거
- `__replace__` 를 사용해 불변 객체로 새 `Version` 반환

기존 테스트 51,524개 모두 통과 확인.