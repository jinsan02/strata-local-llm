수정을 완료했습니다. 무엇을 바꿨는지 요약하면:

**파일:** `src/packaging/specifiers.py`

**변경 내용:** `SpecifierSet` 클래스에 `bounds()` 메서드를 추가했습니다 (약 100줄).

메서드의 동작:
- `===` specifier 가 있으면 `ValueError` 던짐
- 각 specifier 의 연산자/버전에 따라 `(Version, inclusive)` 튜플로 lower/upper 경계 생성
- 여러 specifier 의 경계는 합침: lower 는 max, upper 는 min. 버전이 같으면 `inclusive=False` 쪽이 승리
- 빈 `SpecifierSet` 은 `(None, None)` 반환
- 지원 연산자: `>=`, `>`, `<=`, `<`, `==`, `==V.*` (와일드카드), `~=`, `!=` (경계 없음)
- 와일드카드/`~=` 의 upper 는 epoch 를 유지하고 release 의 마지막 숫자를 버린 후 남은 마지막 숫자를 1 올린 버전으로 생성 (pre/post/dev/local 없음)