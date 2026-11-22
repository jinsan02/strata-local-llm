수정 완료. 변경 내용 요약:

1. **`_extract_declared_extras_from_markers` 함수 추가**: `requires_dist` 마커에서 `extra == <값>` 비교를 추출하여 정규화된 extra 이름 집합을 반환.
2. **`_process_provides_extra` 수정**: 정규화 후 이미 등장한 이름이면 `InvalidMetadata` 발생 (중복 검사).
3. **`Metadata.from_raw` 수정**: `validate=True`일 때, `provides_extra`와 `requires_dist`가 모두 유효하면 선언되지 않은 extra를 검사하여 `ExceptionGroup`에 추가. `provides_extra`가 없거나 기존 검증 오류가 있으면 건너뜀.