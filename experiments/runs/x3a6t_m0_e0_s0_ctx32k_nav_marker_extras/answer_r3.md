<tool_call>
<function=edit_file>
<parameter=new_string>
              self.marker._serialized = None

    @property
    def marker_extras(self) -> frozenset[str]:
        """Return a frozenset of extra names referenced in the marker.

        If there is no marker, returns an empty frozenset. Otherwise, returns
        the result of :meth:`~packaging.markers.Marker.referenced_extras`.

        .. versionadded:: 26.5
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()

    def __replace__(
</parameter>
<parameter=old_string>
              self.marker._serialized = None

    def __replace__(
</parameter>
<parameter=path>
src/packaging/requirements.py
</parameter>
</function>
</tool_call>