<tool_call>
<function=edit_file>
<parameter=new_string>
        self.marker: Marker | None = None
        """A :class:`~.Marker` for the requirement, or ``None``."""
        if parsed.marker is not None:
            self.marker = Marker.__new__(Marker)
            self.marker._markers = _normalize_extra_values(parsed.marker)
            self.marker._serialized = None

    @property
    def marker_extras(self) -> frozenset[str]:
        """Return extra names referenced in the requirement's marker.

        If there is no marker, returns an empty frozenset. Otherwise calls
        :meth:`~packaging.markers.Marker.referenced_extras` on the marker and
        returns the resulting set of normalised extra names.
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()

    def __replace__(
</parameter>
<parameter=old_string>
        self.marker: Marker | None = None
        """A :class:`~.Marker` for the requirement, or ``None``."""
        if parsed.marker is not None:
            self.marker = Marker.__new__(Marker)
            self.marker._markers = _normalize_extra_values(parsed.marker)
            self.marker._serialized = None

    def __replace__(
</parameter>
<parameter=path>
src/packaging/requirements.py
</parameter>
</function>
</tool_call>