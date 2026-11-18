문제를 해결하기 위해 `referenced_extras` 메서드를 정확히 수정하고, `prepare_environment` 함수에서 `context="lock_file"`일 때 `extra`를 빈 문자열이 아닌 빈 집합으로 설정하도록 고칩니다. 또한 `_evaluate_markers` 함수의 로직을 수정하여 `extra`가 집합일 때 비교 연산자가 `==`나 `!=`인 경우에만 `_eval_extra_set`를 호출하도록 합니다.

<<<<<<< SEARCH
def _evaluate_markers(
    markers: MarkerList, environment: Mapping[str, str | AbstractSet[str]]
) -> bool:
    groups: list[list[bool]] = [[]]

    for marker in markers:
        if isinstance(marker, list):
            groups[-1].append(_evaluate_markers(marker, environment))
        elif isinstance(marker, tuple):
            lhs, op, rhs = marker

            rhs_value: str | AbstractSet[str]
            if isinstance(lhs, Variable):
                environment_key = lhs.value
                lhs_value = _lookup_environment(environment, environment_key)
                rhs_value = rhs.value
            else:
                lhs_value = lhs.value
                environment_key = rhs.value
                rhs_value = _lookup_environment(environment, environment_key)
                if environment_key == "extra" and isinstance(rhs_value, AbstractSet):
                    groups[-1].append(_eval_extra_set(rhs_value, op, lhs.value))
                    continue

            # Checks for ``extra`` stay off the common string path.
            if not isinstance(lhs_value, str):
                if environment_key == "extra":
                    if isinstance(lhs_value, AbstractSet):
                        groups[-1].append(_eval_extra_set(lhs_value, op, rhs.value))
                        continue
                    raise UndefinedComparison(
                        f"Marker 'extra' must be a string, not {lhs_value!r}."
                    )
                raise UndefinedComparison(
                    f"Set-valued marker {environment_key!r} can only be used "
                    f'with the membership form (e.g. "<name>" in '
                    f"{environment_key}); it cannot appear on the left-hand "
                    f"side of {op.serialize()!r}."
                )
            lhs_value, rhs_value = _normalize(lhs_value, rhs_value, key=environment_key)
            groups[-1].append(_eval_op(lhs_value, op, rhs_value, key=environment_key))
        elif marker == "or":
            groups.append([])
        elif marker == "and":
            pass
        else:  # pragma: nocover
            raise TypeError(f"Unexpected marker {marker!r}")

    return any(all(item) for item in groups)
=======
def _evaluate_markers(
    markers: MarkerList, environment: Mapping[str, str | AbstractSet[str]]
) -> bool:
    groups: list[list[bool]] = [[]]

    for marker in markers:
        if isinstance(marker, list):
            groups[-1].append(_evaluate_markers(marker, environment))
        elif isinstance(marker, tuple):
            lhs, op, rhs = marker

            rhs_value: str | AbstractSet[str]
            if isinstance(lhs, Variable):
                environment_key = lhs.value
                lhs_value = _lookup_environment(environment, environment_key)
                rhs_value = rhs.value
            else:
                lhs_value = lhs.value
                environment_key = rhs.value
                rhs_value = _lookup_environment(environment, environment_key)
                if (
                    environment_key == "extra"
                    and isinstance(rhs_value, AbstractSet)
                    and op.serialize() in ("==", "!=")
                ):
                    groups[-1].append(_eval_extra_set(rhs_value, op, lhs.value))
                    continue

            # Checks for ``extra`` stay off the common string path.
            if not isinstance(lhs_value, str):
                if environment_key == "extra":
                    if isinstance(lhs_value, AbstractSet):
                        if op.serialize() in ("==", "!="):
                            groups[-1].append(_eval_extra_set(lhs_value, op, rhs.value))
                        else:
                            raise UndefinedComparison(
                                f"Undefined {op!r} on {lhs_value!r} and {rhs.value!r}."
                            )
                        continue
                    raise UndefinedComparison(
                        f"Marker 'extra' must be a string, not {lhs_value!r}."
                    )
                raise UndefinedComparison(
                    f"Set-valued marker {environment_key!r} can only be used "
                    f'with the membership form (e.g. "<name>" in '
                    f"{environment_key}); it cannot appear on the left-hand "
                    f"side of {op.serialize()!r}."
                )
            lhs_value, rhs_value = _normalize(lhs_value, rhs_value, key=environment_key)
            groups[-1].append(_eval_op(lhs_value, op, rhs_value, key=environment_key))
        elif marker == "or":
            groups.append([])
        elif marker == "and":
            pass
        else:  # pragma: nocover
            raise TypeError(f"Unexpected marker {marker!r}")

    return any(all(item) for item in groups)
>>>>>>> REPLACE

<<<<<<< SEARCH
    if context == "lock_file":
        current_environment |= {
            "extras": frozenset(),
            "dependency_groups": frozenset(),
        }
    elif context == "metadata":
        current_environment["extra"] = ""
=======
    if context == "lock_file":
        current_environment |= {
            "extra": frozenset(),
            "extras": frozenset(),
            "dependency_groups": frozenset(),
        }
    elif context == "metadata":
        current_environment["extra"] = ""
>>>>>>> REPLACE