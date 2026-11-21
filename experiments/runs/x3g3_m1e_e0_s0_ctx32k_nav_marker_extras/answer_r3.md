### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
if TYPE_CHECKING:
    from collections.abc import Iterator

    from typing_extensions import Self
=======
if TYPE_CHECKING:
    from collections.abc import Iterator

    from typing_extensions import Self

    from .utils import NormalizedName
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
          self.marker: Marker | None = None
          """A :class:`~.Marker` for the requirement, or ``None``."""
          if parsed.marker is not None:
              self.marker = Marker.__new__(Marker)
              self.marker._markers = _normalize_extra_values(parsed.marker)
              self.marker._serialized = None

      def __replace__(
=======
          self.marker: Marker | None = None
          """A :class:`~.Marker` for the requirement, or ``None``."""
          if parsed.marker is not None:
              self.marker = Marker.__new__(Marker)
              self.marker._markers = _normalize_extra_values(parsed.marker)
              self.marker._serialized = None

      @property
      def marker_extras(self) -> frozenset["NormalizedName"]:
          """The extra names referenced in this requirement's marker.

          Returns an empty :class:`frozenset` if there is no marker, otherwise
          returns the result of :meth:`~packaging.markers.Marker.referenced_extras`.

          .. versionadded:: 26.5
          """
          if self.marker is None:
              return frozenset()
          return self.marker.referenced_extras()

      def __replace__(
>>>>>>> REPLACE