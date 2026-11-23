수정 완료.

**원인:** `_cmpkey` 함수에서 `pre is None and dev is not None` 조건이 `1.0.post1.dev2` 같은 post+dev 버전에도 적용되어, `pre_rank = -1` (dev-only rank)을 부여했다. 이로 인해 `1.0.post1.dev2`가 `1.0a1` 같은 실제 pre-release보다 앞에 오게 되었다.

**수정:** 조건을 `pre is None and post is None and dev is not None`으로 변경하여, post-release가 있는 버전은 dev-only 분기에 들어가지 않도록 했다.