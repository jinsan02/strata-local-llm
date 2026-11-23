모든 요구사항 반영 완료:

- `src/packaging/utils.py:207` — `platforms: Iterable[str] | None = None` 키워드 전용 인자 추가
- `src/packaging/utils.py:321-336` — `platforms is not None`일 때만 검사, `str` 전달 시 `TypeError`, `_normalize_string` + `.lower()`로 정규화 비교, `any` 태그는 무조건 통과, 실패 시 `InvalidWheelFilename`
- `src/packaging/utils.py:12` — `_normalize_string` import 추가
- 기존 검사(확장자·이름·버전·빌드번호·태그)가 platforms 체크 전에 실행되므로 기존 동작/메시지 유지
- 반환값 `(name, version, build, tags)` 변경 없음, `validate_order`와 호환

기존 테스트 317개 모두 통과.