Implementation이 완료되었습니다. 변경 사항을 요약하면:

**수정 파일:** `src/packaging/specifiers.py`

**변경 내용:**
- `SpecifierSet` 클래스에 `bounds()` 메서드 추가 (109줄 추가)
- `===` specifier가 있으면 `ValueError` 던짐
- 빈 `SpecifierSet` 은 `(None, None)` 반환
- 각 연산자(`>=`, `>`, `<=`, `<`, `==`, `==.*`, `~=`, `!=`)에 따른 경계 계산
- `==V.*` 와일드카드: upper는 마지막 release 숫자를 1 올린 버전 (epoch 유지, dev/post/local 없음)
- `~=V`: lower는 V itself, upper는 release[:-1] 후 마지막 숫자 +1 (epoch 유지)
- 여러 specifier 병합: lower는 최대 버전, upper는 최소 버전, 버전 같으면 exclusive(`False`)가 승리