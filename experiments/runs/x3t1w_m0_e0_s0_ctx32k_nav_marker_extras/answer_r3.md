<tool_call>
<function=edit_file>
<parameter=path>
src/packaging/markers.py
</parameter>
<parameter=old_string>
        return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(python_full_version: str) -> str:
</parameter>
<parameter=new_string>
        return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset[NormalizedName]:
        """Return all extra names referenced in this marker.

        Collects every normalized extra name used in ``extra`` comparisons
        (e.g., ``extra == "foo"``, ``"bar" in extras``) anywhere inside the
        marker expression, regardless of whether it ends up being evaluated
        after short-circuiting.  Returns a :class:`frozenset`; empty if no
        extra references exist.

        .. versionadded:: 26.4
        """
        return _extract_referenced_extras(self._markers)


def _pep440_python_full_version(python_full_version: str) -> str:
</parameter>
</function>
</tool_call>