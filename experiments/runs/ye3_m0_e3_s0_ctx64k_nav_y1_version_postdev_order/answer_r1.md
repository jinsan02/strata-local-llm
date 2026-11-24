수정을 마쳤습니다.

**원인**: `_cmpkey` 함수의 dev-only 판별 조건이 `pre is None and dev is not None`로, post-release가 있는 버전(`1.0.post1.dev2`)도 dev-only로 잘못 분류했습니다. 이로 인해 `pre_rank=-1`이 적용되어 `1.0a1`보다 먼저 정렬되고, `>=1.0` 스펙이 `1.0.post1.dev2`를 만족하지 않는 것으로 잘못 계산되었습니다.

**수정**: `src/packaging/version.py`의 1247행에서 `pre is None and dev is not None`를 `pre is None and post is None and dev is not None`로 변경했습니다.