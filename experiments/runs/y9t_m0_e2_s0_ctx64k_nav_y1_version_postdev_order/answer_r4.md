수정 완료했습니다.

**원인:** `_cmpkey` 함수(1247행)에서 `pre is None and dev is not None`일 때 `pre_rank = -1`(dev-only)을 부여했는데, 이 조건은 post-release가 있는 경우(`1.0.post1.dev2`)에도 dev-only로 처리하는 버그였습니다.

**수정:** 조건을 `pre is None and post is None and dev is not None`으로 변경하여, post-release가 있는 경우 dev-only로 분류되지 않도록 했습니다.

이로써:
- `1.0.post1.dev2`는 `pre_rank=3`(stable과 동일), `post_n=1`, `dev_n=2`가 되어 `1.0.post1`보다 앞에, `1.0`보다 뒤에 정렬됩니다.
- `1.0.dev1`은 여전히 `pre_rank=-1`로 `1.0a1`보다 앞에 정렬됩니다.
- 기존 테스트 53,632개 모두 통과합니다.