<tool_call>
<function=edit_file>
<parameter=path>
src/packaging/markers.py
</parameter>
<parameter=old_string>
        .. versionadded:: 26.4
        """
        return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(python_full_version: str) -> str:
</parameter>
<parameter=new_string>
        .. versionadded:: 26.4
        """
        return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset[str]:
        """Return the set of extra names referenced in this marker.

        This includes extras used in comparisons (e.g. ``extra == "x"``,
        ``"x" == extra``, ``extra != "x"``) and membership checks
        (e.g. ``"x" in extras``).  Names are returned in their canonical form.
        """
        return _extract_extras_from_markers(self._markers)


def _pep440_python_full_version(python_full_version: str) -> str:
</parameter>
</function>
</tool_call>