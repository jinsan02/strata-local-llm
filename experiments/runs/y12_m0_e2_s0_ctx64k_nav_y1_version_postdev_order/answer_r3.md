수정 완료.

**원인**: `_cmpkey` 함수에서 `1.0.post1.dev2` 같은 post+dev 버전이 "dev-only"로 잘못 분류되었다. 조건 `if pre is None and dev is not None:`는 `post`가 있는 경우까지 포함해 `pre_rank = -1` (dev-only)을 할당했다. PEP 440에서는 dev-only(`1.0.dev1`)만 `-1`을 받고, post+dev(`1.0.post1.dev2`)는 stable(`pre_rank=3`)로 처리해야 한다.

**수정**: `if pre is None and dev is not None:` → `if pre is None and post is None and dev is not None:`으로 변경해 post 세그먼트가 없는 경우에만 dev-only로 분류하도록 했다. 이로 인해 `1.0.post1.dev2`는 `1.0.post1`보다 작고 `1.0`보다 큰 올바른 순서로 정렬되며, `SpecifierSet`의 `contains`도 `True`를 반환한다.