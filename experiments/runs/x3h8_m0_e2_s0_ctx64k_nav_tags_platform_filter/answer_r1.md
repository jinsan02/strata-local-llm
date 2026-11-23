모든 요구사항을 확인했다:

1. **기본값 `None`, 기존 동작 유지**: `src/packaging/utils.py:215` - `platforms: Iterable[str] | None = None`, `if platforms is not None:` 조건문 ✅
2. **iterable 허용, `str` 전달 시 `TypeError`**: `src/packaging/utils.py:332-335` - `isinstance(platforms, str)` 체크 ✅
3. **정규화 규칙 (`.` `- ` ` ` → `_`, 소문자)**: `src/packaging/utils.py:208` - `_normalize_platform` 함수 ✅
4. **태그 중 하나라도 매칭, `any`는 항상 통과, 빈 iterable 포함**: `src/packaging/utils.py:339-341` - `any(tag.platform == "any" or ...)` ✅
5. **불일치 시 `InvalidWheelFilename`**: `src/packaging/utils.py:343-345` ✅
6. **기존 검사 먼저, 기존 메시지 유지**: `src/packaging/utils.py:282-329` - platforms 검사 전에 기존 검증 ✅
7. **반환값 동일, `validate_order` 호환**: `src/packaging/utils.py:347` - 기존 `(name, version, build, tags)` 그대로 반환 ✅
8. **기존 동작 변경 없음**: `platforms=None` 시 기존 코드 경로 동일 ✅

테스트 317개 모두 통과. 수정 완료.