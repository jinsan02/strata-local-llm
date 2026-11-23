수정 완료. `src/packaging/version.py`의 `_cmpkey` 함수에서 두 가지 변경을 했다:

1. **dev-only 판정 조건 수정** (1247줄): `pre is None and dev is not None` → `pre is None and dev is not None and post is None`. `post`가 있는 경우(dev-after-post)를 dev-only로 잘못 분류하는 버그를 고쳤다.

2. **`dev_rank` 로직 수정** (1262-1268줄): 기존 `dev_rank = 1 if dev is None else 0`을 PEP 440에 맞게 수정:
   - dev-only (pre=None, post=None): `dev_rank=-1` (모든 pre-release보다 앞)
   - pre 또는 post가 있고 dev가 있음: `dev_rank=0` (해당 pre/post 뒤에 옴)
   - dev 없음: `dev_rank=1` (dev가 있는 버전보다 뒤)

이로써 `1.0.post1.dev2`가 `1.0.post1`보다 앞에, `1.0`보다 뒤에 정렬되고, `SpecifierSet(">=1.0").contains("1.0.post1.dev2")`가 `True`가 된다.