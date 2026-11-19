`packaging.metadata.Metadata` 의 extra 검사를 두 가지 늘려라.

1. **Provides-Extra 중복**: `provides_extra` 값을 처리할 때, 이름을 지금처럼 `canonicalize_name` 으로 정규화한 뒤 같은 이름이 두 번 이상 나오면 `InvalidMetadata` 를 던진다(필드 이름 `provides-extra`). 예: `["Foo", "foo"]`, `["foo-bar", "foo_bar"]`. 이 검사는 `validate=False` 로 만든 객체에서 `provides_extra` 속성에 접근할 때도 일어난다. 중복이 없으면 지금처럼 정규화된 이름 리스트를 돌려준다.
2. **선언되지 않은 extra**: `Metadata.from_raw(..., validate=True)` (따라서 `from_email` 도) 검증에서, `requires_dist` 의 요구사항 마커가 변수 `extra` 를 값과 비교하는 부분(`extra == "docs"` · `"docs" == extra` 처럼, 연산자와 좌우 순서 무관, `and` · `or` · 괄호 안 포함)의 값을 정규화한 이름이 정규화된 `provides_extra` 에 없으면 `InvalidMetadata` 를 낸다(필드 이름 `requires-dist`). 다른 검증 오류와 함께 `ExceptionGroup` 으로 모인다.
   - `provides_extra` 필드가 아예 없으면(값이 `None`) 이 검사는 하지 않는다. `provides_extra` 나 `requires_dist` 자체가 잘못돼 오류가 난 경우에도 이 검사는 건너뛴다.
   - `"docs" in extras` 같은 `extras` 집합 비교는 이 검사 대상이 아니다.
   - `validate=False` 일 때는 이 검사를 하지 않는다.
3. 기존 동작은 바뀌면 안 된다.

마커의 구조는 `packaging.markers` · `packaging._parser` 에 있다.
