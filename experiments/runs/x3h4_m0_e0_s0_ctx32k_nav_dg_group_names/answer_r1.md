`src/packaging/dependency_groups.py` 파일에 다음과 같이 수정을 가했습니다.

1. `packaging.utils.canonicalize_name`을 가져와서 패키지의 `Name` 필드 규칙 검증에 재사용합니다.
2. `ValueError`를 상속하는 `InvalidGroupName` 예외 클래스를 추가하고 `__all__`에 등록합니다.
3. `_normalize_group_names` 내부에서 그룹 이름 키를 검사하여 잘못된 형식의 경우 기존 오류 수집기(`_ErrorCollector`)에 모아서 보고합니다. 
4. `lookup()`과 `resolve()` 메서드 시작 부분에서 유효하지 않은 그룹 이름을 즉시 넘겨받으면 `InvalidGroupName`을 단일 예외로 던지도록 합니다.

```python
# src/packaging/dependency_groups.py 내 주요 변경 사항 요약:
# 1. import 구문 추가: from .utils import canonicalize_name
# 2. __all__ 에 "InvalidGroupName" 추가
# 3. InvalidGroupName 클래스 및 _validate_group_name 헬퍼 함수 정의
# 4. _normalize_group_names 순회 시 _validate_group_name(group_name) 호출
# 5. lookup() 과 resolve() 의 첫 줄에 _validate_group_name(group) 호출 추가
```