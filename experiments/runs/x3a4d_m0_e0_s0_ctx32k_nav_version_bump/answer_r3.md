### EDIT: src/packaging/version.py
<<<<<<< SEARCH
        return self.release[2] if len(self.release) >= 3 else 0

    def _trim_release(self) -> Version:
=======
        return self.release[2] if len(self.release) >= 3 else 0

    def bump(self, part: str) -> Version:
        """
        Return a new version with the specified part bumped.

        :param part: One of "major", "minor", or "micro".
        :raises ValueError: If ``part`` is not one of the valid parts.

        >>> Version("1.2.3").bump("major")
        <Version('2.0.0')>
        >>> Version("1.2.3").bump("minor")
        <Version('1.3.0')>
        >>> Version("1.2.3").bump("micro")
        <Version('1.2.4')>
        >>> Version("1").bump("micro")
        <Version('1.0.1')>
        >>> Version("1.2.3rc1").bump("major")
        <Version('2.0.0')>
        """
        if part == "major":
            index = 0
        elif part == "minor":
            index = 1
        elif part == "micro":
            index = 2
        else:
            raise ValueError(
                f"part must be 'major', 'minor', or 'micro', got {part!r}"
            )

        release = list(self._release)
        while len(release) <= index:
            release.append(0)
        
        release[index] += 1
        for i in range(index + 1, len(release)):
            release[i] = 0
            
        return self.__replace__(
            release=tuple(release),
            pre=None,
            post=None,
            dev=None,
            local=None
        )

    def _trim_release(self) -> Version:
>>>>>>> REPLACE

`Version` 클래스에 `bump` 메서드를 추가했습니다. `major`, `minor`, `micro`에 따라 release 숫자를 증가시키고, 뒤의 숫자를 0으로 초기화하며, pre/post/dev/local은 제거합니다. 유효하지 않은 part 값에 대해서는 `ValueError`를 발생시킵니다.