`packaging.markers.Marker`에 `referenced_extras()` 메서드를, `packaging.requirements.Requirement`에 `marker_extras` 속성을 추가했습니다. 

`referenced_extras()` 구현 중 PEP 685의 `"x" in extras` 형식을 처리하기 위해 `"extra"`뿐만 아니라 `"extras"` 변수명도 포함하도록 수정이 필요합니다. 아래 편집 블록을 적용하세요.

### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
                # One side must be Variable("extra"), the other must be Value
                if isinstance(lhs, Variable) and lhs.value == "extra":
                    if isinstance(rhs, Value):
                        extras.add(canonicalize_name(rhs.value))
                elif isinstance(rhs, Variable) and rhs.value == "extra":
                    if isinstance(lhs, Value):
                        extras.add(canonicalize_name(lhs.value))
=======
                # One side must be Variable("extra") or Variable("extras"), the other must be Value
                if isinstance(lhs, Variable) and lhs.value in {"extra", "extras"}:
                    if isinstance(rhs, Value):
                        extras.add(canonicalize_name(rhs.value))
                elif isinstance(rhs, Variable) and rhs.value in {"extra", "extras"}:
                    if isinstance(lhs, Value):
                        extras.add(canonicalize_name(lhs.value))
>>>>>>> REPLACE