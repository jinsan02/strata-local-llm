과제 요구사항을 하나씩 확인합니다.

**1. `bounds()` 메서드 추가** — `src/packaging/specifiers.py:1255-1349` ✓
**2. 반환값 `(lower, upper)` 튜플, 각각 `None` 또는 `(Version, bool)`** — 타입 힌트 및 반환문 확인 ✓
**3. 각 연산자별 경계** — `>=V, >V, <=V, <V, ==V, ==V.*, ~=V, !=V` 모두 구현 ✓
**4. 와일드카드/`~=` upper: epoch 유지, release 숫자만, pre/post/dev/local 없음** — `_next_prefix_dev0` 후 `__replace__(dev=None)` 적용 ✓
   - `==1.2.*` → `(1.2, True), (1.3, False)` ✓
   - `==1!2.*` → epoch 1 유지, upper `1!3` ✓
   - `~=1.4.5` → upper `1.5` ✓
   - `~=2.2` → upper `3` ✓
   - `~=1.4.5rc1` → lower `1.4.5rc1`, upper `1.5` ✓
**5. 여러 specifier 합치기: lower 최대, upper 최소, 동점 시 exclusive 승리** — merge 로직 확인 ✓
**6. 빈 SpecifierSet → `(None, None)`** — `if not self._specs` 확인 ✓
**7. `===` 있으면 `ValueError`** — `if self._has_arbitrary` 확인 ✓
**8. prerelease 설정 영향 없음** — `prereleases` 관련 코드 없음 ✓
**9. 기존 테스트 2108개 모두 통과** ✓

모든 요구사항을 반영했습니다.

---

**수정 내용 요약:**

- `src/packaging/specifiers.py`:
  - `._ranges` 모듈에서 `_next_prefix_dev0` 추가 import
  - `SpecifierSet.bounds()` 메서드 추가 (~100줄): `===` 체크, 빈 세트 처리, 각 specifier 연산자별 경계 추출, 경계 병합(최대 lower/최소 upper, 동점 시 exclusive 우선), 와일드카드/`~=` 의 upper 에서 dev 제거