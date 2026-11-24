수정 사항을 요약하면:

`_cmpkey` 함수에서 `dev_rank` 계산 로직이 `dev`가 있는지 없는지만 보고 있었으나, PEP 440 에 따르면 **post-release 가 있는 경우 그 뒤의 dev-release(post+dev)는 post-release alone 보다 뒤에 와야 한다**. 기존 코드는 `dev_rank = 1 if dev is None else 0` 으로 post+dev 가 post alone 보다 작게 비교되는 버그가 있었다.

수정 후 `dev_rank`는 4가지 상태로 구분된다:
- `0`: dev-only (dev 있고 post 없음) — pre-release 보다 앞
- `1`: stable (dev 없고 post 없음)
- `2`: post-only (dev 없고 post 있음)
- `3`: post+dev (dev 있고 post 있음) — post 보다 뒤

이로써 `1.0.post1.dev2`가 `1.0.post1` 보다 커지고, `SpecifierSet(">=1.0").contains("1.0.post1.dev2")` 도 `True` 가 된다. 다른 버전들(1.0.dev1 < 1.0a1, 1.0rc1 < 1.0rc1.dev1 등)의 순서는 그대로 유지된다.