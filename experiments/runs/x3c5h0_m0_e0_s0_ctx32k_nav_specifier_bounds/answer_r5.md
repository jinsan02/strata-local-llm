수정 내용을 요약합니다.

1.  `src/packaging/specifiers.py` 파일에 `InvalidVersion` import를 추가했습니다.
2.  `src/packaging/specifiers.py`의 `SpecifierSet` 클래스에 `bounds()` 메서드를 구현했습니다.
    *   `===` 연산자가 있으면 `ValueError`를 발생시킵니다.
    *   각 specifier의 연산자와 버전을 분석하여 `(lower, upper)` 경계를 계산합니다.
    *   와일드카드 (`==V.*`)와 호환성 (`~=V`) 연산자에 대해 요구된 버전 산출 규칙(마지막 숫자 올리기 등)을 적용했습니다.
    *   여러 specifier의 경계를 합칠 때, 하한은 가장 큰 것을, 상한은 가장 작은 것을 선택하며, 동점 시 `inclusive=False`가 승리하도록 처리했습니다.

### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
from .version import Version, _adapt_possessive
=======
from .version import Version, _adapt_possessive, InvalidVersion
>>>>>>> REPLACE

### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
        return self._canonical_specs() == other._canonical_specs()

    def __len__(self) -> int:
=======
        return self._canonical_specs() == other._canonical_specs()

    def bounds(self) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
        """Return the (lower, upper) version bounds.

        :return: A tuple of ``(lower, upper)``, where each item is either
            ``None`` or a ``(version, inclusive)`` tuple.
        :raises ValueError: If the specifier set contains an arbitrary (===) specifier.
        """
        if self._has_arbitrary:
            raise ValueError(
                "Bounds cannot be determined for SpecifierSet containing an "
                "arbitrary (===) specifier."
            )

        lower: tuple[Version, bool] | None = None
        upper: tuple[Version, bool] | None = None

        for spec in self._specs:
            op = spec.operator
            ver_str = spec.version
            
            # Version object base (without wildcard suffix)
            version_base = ver_str.removesuffix(".*")
            
            try:
                version = Version(version_base)
            except InvalidVersion:
                continue

            new_lower: tuple[Version, bool] | None = None
            new_upper: tuple[Version, bool] | None = None

            if op == ">=":
                new_lower = (version, True)
            elif op == ">":
                new_lower = (version, False)
            elif op == "<=":
                new_upper = (version, True)
            elif op == "<":
                new_upper = (version, False)
            elif op == "==":
                if ver_str.endswith(".*"):
                    new_lower = (version, True)
                    rel = version.release
                    # Next prefix: increment last digit of release.
                    # e.g., 1.2 -> 1.3, 1 -> 2
                    if len(rel) > 1:
                        new_rel = (*rel[:-1], rel[-1] + 1)
                    else:
                        new_rel = (rel[0] + 1,)
                    
                    try:
                        upper_version = Version.from_parts(epoch=version.epoch, release=new_rel)
                        new_upper = (upper_version, False)
                    except InvalidVersion:
                        pass
                else:
                    new_lower = (version, True)
                    new_upper = (version, True)
            elif op == "~=":
                new_lower = (version, True)
                rel = version.release
                # Upper bound is the next release after dropping the last component.
                if len(rel) > 1:
                    new_rel = (*rel[:-2], rel[-2] + 1)
                else:
                    new_rel = (rel[0] + 1,)
                
                try:
                    upper_version = Version.from_parts(epoch=version.epoch, release=new_rel)
                    new_upper = (upper_version, False)
                except InvalidVersion:
                    pass

            # Merge lower bound
            if new_lower is not None:
                if lower is None:
                    lower = new_lower
                else:
                    cur_ver, cur_inc = lower
                    new_ver, new_inc = new_lower
                    if new_ver > cur_ver:
                        lower = new_lower
                    elif new_ver == cur_ver and not new_inc and cur_inc:
                        lower = new_lower

            # Merge upper bound
            if new_upper is not None:
                if upper is None:
                    upper = new_upper
                else:
                    cur_ver, cur_inc = upper
                    new_ver, new_inc = new_upper
                    if new_ver < cur_ver:
                        upper = new_upper
                    elif new_ver == cur_ver and not new_inc and cur_inc:
                        upper = new_upper

        return (lower, upper)

    def __len__(self) -> int:
>>>>>>> REPLACE