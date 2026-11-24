수정을 마쳤습니다. `src/packaging/specifiers.py` 파일의 `SpecifierSet` 클래스에 `bounds()` 메서드를 추가했습니다.

**변경 내용 요약:**
- `SpecifierSet.bounds()` 메서드 추가 (도큐스트링 포함)
- `===` specifier 가 있으면 `ValueError` 던짐
- 각 연산자별 경계 계산: `>=`, `>`, `<=`, `<`, `==`, `==.*`, `~=`, `!=`
- 와일드카드(`.*`) 와 `~=` 의 upper 는 epoch 유지, release 숫자만으로 계산
- 여러 specifier 의 경계는 합침: lower 는 가장 큰 것, upper 는 가장 작은 것
- 같은 버전일 때 `inclusive=False` 쪽이 우선