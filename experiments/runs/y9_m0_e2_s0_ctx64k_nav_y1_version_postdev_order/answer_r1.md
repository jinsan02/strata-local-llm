수정 완료. `_cmpkey` 함수의 1247번 줄에서 `dev-only` 판정 조건이 `pre is None and dev is not None`였는데, 이는 post-release가 있는 경우까지 dev-only로 잘못 분류하는 버그였다. `1.0.post1.dev2` 같은 버전은 post-release가 있으므로 dev-only가 아니어야 하지만, 기존 코드는 post를 무시하고 dev만 보고 dev-only로 판단해 `pre_rank = -1` (dev-only rank)를 부여했다.

수정: `if pre is None and dev is not None:` → `if pre is None and post is None and dev is not None:`

이로써:
- `1.0.post1.dev2`는 이제 `pre_rank=3` (stable)로 처리되어 `1.0` < `1.0.post1.dev2` < `1.0.post1` 순서가 올바름
- `1.0.dev1`은 여전히 `pre_rank=-1` (dev-only)로 `1.0a1`보다 앞
- `SpecifierSet(">=1.0").contains("1.0.post1.dev2")`도 `_cmpkey`가 올바르게 동작하므로 `True` 반환