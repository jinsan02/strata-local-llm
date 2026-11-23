수정 완료. `src/packaging/version.py`의 `_cmpkey` 함수에서 `pre is None and dev is not None` 조건에 `and post is None`을 추가했다.

**원인:** `1.0.post1.dev2` 같은 버전에서 `pre=None`, `dev=('dev', 2)`, `post=('post', 1)`일 때, 기존 조건 `pre is None and dev is not None`이 True가 되어 "dev-only" 케이스로 처리되었다. 이로 인해 `pre_rank = -1` (모든 pre-release보다 앞)이 되어 정렬이 엉키고, `1.0`보다 작은 버전으로 간주되어 `SpecifierSet`의 `contains`도 False를 반환했다.

**수정:** `and post is None`을 추가해 post-release가 있는 버전은 "dev-only"가 아닌 "stable" (`pre_rank=3`)로 처리하게 했다. 이제 `1.0 < 1.0.post1.dev2 < 1.0.post1`로 올바르게 정렬된다.