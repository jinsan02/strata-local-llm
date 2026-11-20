기존 테스트 전체(51,524개)가 통과했습니다.

`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

- `"major"` → release[0] += 1, 이후 모두 0
- `"minor"` → release[1] += 1, 이후 모두 0  
- `"micro"` → release[2] += 1, 이후 모두 0
- 유효하지 않은 `part`는 `ValueError` 던짐
- epoch 유지, pre/post/dev/local 버림
-release 길이 유지(올릴 자리 없으면 0 채워 확장)