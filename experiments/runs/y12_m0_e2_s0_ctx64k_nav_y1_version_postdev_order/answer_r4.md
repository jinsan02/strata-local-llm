수정 내용을 요약하면:

**원인:** `_cmpkey` 함수에서 `pre`가 없고 `dev`만 있을 때를 "dev-only" 버전으로 처리하는 조건(`if pre is None and dev is not None`)이 `post`가 있는 경우(`1.0.post1.dev2` 등)까지 포함하고 있었다. PEP 440에 따르면 dev-only(예: `1.0.dev1`)만 pre-release보다 앞에 와야 하며, post-release와 함께 있는 dev segment는 해당 post release의 일부로 처리되어야 한다.

**수정:** 조건에 `and post is None`을 추가하여 `pre`도 없고 `post`도 없으며 `dev`만 있는 경우에만 "dev-only"로 처리되도록 했다.