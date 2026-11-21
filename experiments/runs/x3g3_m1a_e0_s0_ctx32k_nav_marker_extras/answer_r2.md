### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
        try:
            tmp = Requirement(requirement_string)
        except InvalidRequirement as exc:
            raise TypeError(f"Cannot restore Requirement from {state!r}") from exc
=======
        try:
            tmp = Requirement(requirement_string)
        except InvalidRequirement as exc:
            raise TypeError(f"Cannot restore Requirement from {state!r}") from exc

    @property
    def marker_extras(self) -> frozenset["utils.NormalizedName"]:
        """Return all extra names referenced in the requirement's marker.

        Returns an empty frozenset if the requirement has no marker.
        """
        return self.marker.referenced_extras() if self.marker is not None else frozenset()
>>>>>>> REPLACE