모든 테스트가 통과했습니다.

**원인:** `_cmpkey` 함수의 `if pre is None and dev is not None:` 조건이 `post`가 있는 경우까지 "dev-only"로 잘못 분류했습니다. `1.0.post1.dev2` 같은 버전은 pre=None, dev=('dev', 2)이지만 post도 있으므로 dev-only가 아닙니다. PEP 440에서 dev-only는 pre와 post가 **모두** 없는 경우를 의미합니다.

**수정:** 조건을 `if pre is None and post is None and dev is not None:`으로 변경하여 post가 없는 경우에만 dev-only로 분류하도록 했습니다.