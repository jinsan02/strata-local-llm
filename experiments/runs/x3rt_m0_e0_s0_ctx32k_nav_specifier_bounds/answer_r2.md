### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
    def __iter__(self) -> Iterator[Specifier]:
        """
        Returns an iterator over all the underlying :class:`Specifier` instances
        in this specifier set.

        >>> sorted(SpecifierSet(">=1.0.0,!=1.0.1"), key=str)
        [<Specifier('!=1.0.1')>, <Specifier('>=1.0.0')>]
        """
        return iter(self._specs)

    def _get_ranges(self) -> Sequence[Interval]:
=======
    def __iter__(self) -> Iterator[Specifier]:
        """
        Returns an iterator over all the underlying :class:`Specifier` instances
        in this specifier set.

        >>> sorted(SpecifierSet(">=1.0.0,!=1.0.1"), key=str)
        [<Specifier('!=1.0.1')>, <Specifier('>=1.0.0')>]
        """
        return iter(self._specs)

    def bounds(self) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
        """Return the combined lower and upper bounds of this specifier set.
        
        Returns a tuple ``(lower, upper)`` where each is ``None`` or a 
        ``(version, inclusive)`` tuple representing the effective boundaries.
        """
        if self._has_arbitrary:
            raise ValueError("=== is not supported for bounds()")
        
        lower_v: Version | None = None
        lower_inc: bool | None = None
        upper_v: Version | None = None
        upper_inc: bool | None = None
        
        for spec in self._specs:
            op, ver_str = spec._spec
            ver = spec._get_spec_version()
            
            if op == ">=":
                l_v, l_inc = ver, True
                u_v, u_inc = None, None
            elif op == ">":
                l_v, l_inc = ver, False
                u_v, u_inc = None, None
            elif op == "<=":
                l_v, l_inc = None, None
                u_v, u_inc = ver, True
            elif op == "<":
                l_v, l_inc = None, None
                u_v, u_inc = ver, False
            elif op == "==":
                if ver_str.endswith(".*"):
                    l_v, l_inc = ver, True
                    upper_release = (*ver.release[:-1], ver.release[-1] + 1)
                    u_v = Version(epoch=ver.epoch, release=upper_release)
                    u_inc = False
                else:
                    l_v, l_inc = ver, True
                    u_v, u_inc = ver, True
            elif op == "~=":
                l_v, l_inc = ver, True
                release = ver.release
                if len(release) == 1:
                    upper_release = (release[0] + 1,)
                else:
                    upper_release = (*release[:-1], release[-1] + 1)
                u_v = Version(epoch=ver.epoch, release=upper_release)
                u_inc = False
            elif op == "!=":
                l_v, l_inc = None, None
                u_v, u_inc = None, None
            else:
                continue
                
            # Combine lower bound
            if l_v is not None:
                if lower_v is None:
                    lower_v, lower_inc = l_v, l_inc
                else:
                    if l_v > lower_v:
                        lower_v, lower_inc = l_v, l_inc
                    elif l_v == lower_v:
                        lower_inc = lower_inc and l_inc
                        
            # Combine upper bound
            if u_v is not None:
                if upper_v is None:
                    upper_v, upper_inc = u_v, u_inc
                else:
                    if u_v < upper_v:
                        upper_v, upper_inc = u_v, u_inc
                    elif u_v == upper_v:
                        upper_inc = upper_inc and u_inc
                        
        return (
            (lower_v, lower_inc) if lower_v is not None else None,
            (upper_v, upper_inc) if upper_v is not None else None
        )

    def _get_ranges(self) -> Sequence[Interval]:
>>>>>>> REPLACE

`SpecifierSet.bounds()` 메서드를 추가했습니다. `===` 가 있으면 `ValueError` 를 던지며, 각 specifier 의 경계를 계산해 가장 큰 하한과 가장 작은 상한을 결합합니다. 버전이 같을 때는 `inclusive=False` 가 우선하도록 처리했습니다. 와일드카드(`==V.*`) 와 호환 연산자(`~=V`) 의 상한은 PEP 440 규칙에 따라 마지막 release 숫자를 조정하여 생성합니다.