수정 내용을 요약하면:

`src/packaging/version.py`의 `_cmpkey` 함수에서 `pre is None and dev is not None` 조건이 `1.0.post1.dev2` 같은 사후 릴리스의 개발판까지 "dev-only"로 잘못 판단하고 있었습니다. PEP 440에서 dev-only(-1 rank)는 pre/post가 없고 dev만 있는 버전(예: `1.0.dev1`)에만 적용되어야 합니다.

**수정:** `pre is None and dev is not None` → `pre is None and post is None and dev is not None`

이로써:
- `1.0.post1.dev2`는 stable pre_rank(3)을 얻어 `1.0` > `1.0a1` 순서대로 올바르게 정렬됩니다.
- `1.0.dev1`은 여전히 dev-only rank(-1)을 얻어 `1.0a1`보다 앞에 머물고, `1.0`보다도 앞에 있습니다.
- `SpecifierSet(">=1.0", prereleases=True).contains("1.0.post1.dev2")`도 `True`를 반환합니다.