모든 요구사항을 확인함:
1. `part`가 `"major"`/`"minor"`/`"micro"`일 때 해당 인덱스 숫자 1 올리고 뒤의 숫자 0으로 만듦 → `src/packaging/version.py:1112-1157`
2. release 길이 유지, 올릴 자리 없으면 0으로 채워 늘림 → `while len(release) <= index: release.append(0)`
3. epoch 유지, pre/post/dev/local 버림 → `from_parts(epoch=self._epoch, release=tuple(release))`
4. 그 밖의 `part` 값은 `ValueError` → `else: raise ValueError(...)`
5. 원래 객체 불변, 새 `Version` 반환 → `list()` 복사 및 `from_parts()` 새 인스턴스 생성
6. 기존 동작 영향 없음 → 기존 코드 수정 없음

자동 검사(51524 passed) 및 수동 확인 모두 통과. 추가 수정 불필요.