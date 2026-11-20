`packaging.specifiers.SpecifierSet` 클래스에 `bounds()` 메서드를 추가합니다. 이 메서드는 주어진 스펙집합의 하한과 상한 경계를 `(Version, bool)` 형태의 튜플로 계산하여 반환합니다. 와일드카드(`.*`)와 호환 연산자(`~=`)의 상한 버전은 release 숫자를 기반으로 계산됩니다.

### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
    def __eq__(self, other: object) -> bool:
        """Return whether or not the two Specifier-like objects are equal.
=======
    def bounds(self) -> tuple[Version | None, Version | None]:
        """Return the bounding range for this specifier set.

        Returns a tuple of ``(lower, upper)``, where each is ``None`` or
        a ``(Version, inclusive)`` tuple.  ``inclusive=False`` means open
        parenthesis, ``True`` means square bracket.
        """
        lower: Version | None = None
        upper: Version | None = None

        def _pick_lower(current, candidate):
            if current is None:
                return candidate
            c_v, c_i = candidate
            cur_v, cur_i = current
            if c_v != cur_v:
                return max(current, candidate, key=lambda x: x[0])
            return candidate  # version equal; prefer inclusive=False (tighter)

        def _pick_upper(current, candidate):
            if current is None:
                return candidate
            c_v, c_i = candidate
            cur_v, cur_i = current
            if c_v != cur_v:
                return min(current, candidate, key=lambda x: x[0])
            return candidate  # version equal; prefer inclusive=False (tighter)

        for spec in self._specs:
            op = spec.operator
            ver_str = spec.version
            v = spec._get_spec_version()
            if v is None:
                continue

            if op == "==":
                if ver_str.endswith(".*"):
                    # Wildcard: [V, next_release)
                    r_list = list(v.release)
                    r_list[-1] += 1
                    release_str = ".".join(str(x) for x in r_list)
                    upper_ver = Version(
                        f"{v.epoch}!{release_str}" if v.epoch else release_str
                    )
                    new_lower: tuple[Version, bool] | None = (v, True)
                    new_upper: tuple[Version, bool] | None = (upper_ver, False)
                else:
                    # Exact match: [V, V]
                    new_lower = (v, True)
                    new_upper = (v, True)

            elif op == "~=":
                # Compatible: [V, next_last_digit_increased)
                r_list = list(v.release[:-1])
                if not r_list:
                    raise ValueError(
                        f"Compatible release {ver_str!r} requires at least two digits."
                    )
                r_list[-1] += 1
                release_str = ".".join(str(x) for x in r_list)
                upper_ver = Version(
                    f"{v.epoch}!{release_str}" if v.epoch else release_str
                )
                new_lower = (v, True)
                new_upper = (upper_ver, False)

            elif op == ">=":
                new_lower = (v, True)
                new_upper = None
            elif op == ">":
                new_lower = (v, False)
                new_upper = None
            elif op == "<=":
                new_lower = None
                new_upper = (v, True)
            elif op == "<":
                new_lower = None
                new_upper = (v, False)
            elif op == "!=":
                # != does not constrain the numeric bounds for this purpose.
                new_lower = None
                new_upper = None
            else:
                continue

            lower = _pick_lower(lower, new_lower)
            upper = _pick_upper(upper, new_upper)

        return (lower, upper)

    def __eq__(self, other: object) -> bool:
        """Return whether or not the two Specifier-like objects are equal.
>>>>>>> REPLACE