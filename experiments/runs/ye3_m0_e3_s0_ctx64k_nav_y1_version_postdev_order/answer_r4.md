수정 완료.

**원인**: `_cmpkey` 함수에서 "dev-only" 판정 조건이 `pre is None and dev is not None`로, post-release가 있는 버전(`1.0.post1.dev2`)까지 dev-only로 잘못 분류하고 있었다. 이로 인해 `pre_rank=-1`이 부여되어 모든 pre-release보다 앞에 오게 되었다.

**수정**: 조건을 `pre is None and post is None and dev is not None`로 변경하여, post-release가 있는 버전은 dev-only가 아닌 stable(post-release)로 분류되도록 했다.

- `1.0.dev1`: pre=None, post=None, dev 있음 → dev-only (pre_rank=-1) → `1.0a1`보다 앞 ✓
- `1.0.post1.dev2`: pre=None, post 있음, dev 있음 → stable (pre_rank=3) → `1.0`보다 뒤, `1.0.post1`보다 앞 ✓
- `SpecifierSet(">=1.0").contains("1.0.post1.dev2")`: `1.0.post1.dev2 >= 1.0`이 True이므로 `True` 반환 ✓