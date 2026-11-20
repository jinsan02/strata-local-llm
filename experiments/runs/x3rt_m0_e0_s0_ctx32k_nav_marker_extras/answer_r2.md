<tool_call>
<function=edit_file>
<parameter=new_string>
        # Specifiers technically can be mutated, so deep copy needed
        result.specifier = copy.deepcopy(tmp.specifier)
        return result

    @property
    def marker_extras(self) -> frozenset[str]:
        """Return the set of extra names referenced in this requirement's marker.

        If the requirement has no marker, returns an empty :class:`frozenset`.
        Otherwise, returns the result of
        :meth:`~packaging.markers.Marker.referenced_extras`.

        .. versionadded:: 26.5
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()

    def _iter_parts(self, name: str) -> Iterator[str]:
</parameter>
<parameter=old_string>
        # Specifiers technically can be mutated, so deep copy needed
        result.specifier = copy.deepcopy(tmp.specifier)
        return result

    def _iter_parts(self, name: str) -> Iterator[str]:
</parameter>
<parameter=path>
src/packaging/requirements.py
</parameter>
</function>
</tool_call>