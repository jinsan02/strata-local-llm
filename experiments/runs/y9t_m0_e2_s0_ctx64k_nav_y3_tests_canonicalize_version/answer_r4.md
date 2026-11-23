새 파일 `tests/test_y_canonicalize_version.py`를 만들었습니다. 기존 테스트 파일은 수정하지 않았습니다.

**테스트 커버리지 요약 (103개 테스트, 모두 통과):**

| 카테고리 | 내용 |
|---|---|
| **기본 동작** | `1.0.0` → `"1"`, `1.4.0` → `"1.4"`, `0.0.0` → `"0"` 등 trailing zero 제거 |
| **`strip_trailing_zero=False`** | `1.0.0` → `"1.0.0"` (전체 release 유지) |
| **잘못된 버전** | `"lolwat"`, `"foo bar baz"`, `""` 등 원문 그대로 반환 |
| **`Version` 객체 입력** | `Version("1.4.0")` 객체 전달 시 동일 결과 |
| **Epoch** | `"1!1.0.0"` → `"1!1"`, epoch 0은 생략 |
| **Pre-release** | `"1.0a0"` → `"1a0"`, `"1.0alpha1"` → `"1a1"` 등 정규화 |
| **Post-release** | `"1.0.post0"` → `"1.post0"`, `"1.0-1"` → `"1.post1"` |
| **Dev-release** | `"1.0.dev0"` → `"1.dev0"` |
| **Local version** | `"1.0+abc"` → `"1+abc"` |
| **복합 세그먼트** | epoch+pre+post+dev+local 조합 |
| **`_trim_release` 동작** | trailing zero가 모두 0이어도 최소 1개는 남김 (`"0.0.0"` → `"0"`) |
| **중복 제거** | 이미 canonicalized 버전에서 다시 호출해도 동일 결과 |