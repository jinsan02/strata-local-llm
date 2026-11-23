요구사항 확인:

1. **`part`는 `"major"`·`"minor"`·`"micro"` 중 하나** (1143-1152줄): `if/elif/else`로 정확히 3개만 허용, 나머지는 `ValueError` ✅
2. **해당 release 숫자 1 올리고 뒤 0으로** (1154-1163줄): `release[index] += 1` 후 루프로 뒤 0 채움 ✅
3. **release 길이 유지** (1156-1157줄): `while len(release) <= index`로 필요한 경우만 확장 ✅
   - 예: `1`→micro → `(1,)` → `(1,0,0)` → `(1,0,1)` ✅
   - 예: `1.2.3.4`→minor → `(1,3,0,0)` 길이 4 유지 ✅
4. **epoch 그대로, pre/post/dev/local 버림** (1165줄): `__replace__`에 `pre=None, post=None, dev=None, local=None` 명시적 전달 ✅
   - 예: `2!1.2.3rc1.post2.dev3+abc`→micro → `2!1.2.4` ✅
5. **기타 `part` 값은 `ValueError`** (1149-1152줄): `"Major"`, `"MINOR"` 등 대소문자 다른 것도 `ValueError` ✅
6. **원본 불변, 새 `Version` 반환** (1165줄): `__replace__`는 새 인스턴스 반환 ✅
7. **기존 동작 불변**: 새 메서드만 추가, 기존 메서드 변경 없음 ✅

지시문 요구사항 모두 반영 완료.