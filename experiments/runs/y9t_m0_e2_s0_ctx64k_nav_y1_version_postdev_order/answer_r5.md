모든 기존 테스트(53,632개)가 통과했습니다.

**수정 내용 요약:**

`src/packaging/version.py`의 `_cmpkey` 함수(약 1247행)에서 버그를 고쳤습니다.

**원인:** `pre is None and dev is not None` 조건이 `post`가 있는 경우(`1.0.post1.dev2`)까지 포함하여 `pre_rank = -1`을 부여하고 있었습니다. 이로 인해 post-release의 development release가 pre-release보다 앞에 정렬되는 문제가 발생했습니다.

**수정:** `pre is None and dev is not None and post is None`으로 조건을 추가하여, dev-only release(`1.0.dev1`)에만 `_PRE_RANK_DEV_ONLY`(-1)를 사용하고, post-release의 development release(`1.0.post1.dev2`)는 `_PRE_RANK_STABLE`(3)을 사용하도록 했습니다.

PEP 440에 따른 올바른 정렬 순서:
`1.0.dev1` < `1.0a1` < `1.0` < `1.0.post1.dev2` < `1.0.post1`