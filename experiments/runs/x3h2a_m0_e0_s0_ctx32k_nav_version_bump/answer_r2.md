수정 내용: `packaging.version.Version` 클래스에 `bump(part)` 메서드를 추가했습니다. 이 메서드는 지정한 부분(`major`, `minor`, `micro`)의 숫자를 1 증가시키고, 뒤따르는 숫자들을 0으로 만듭니다. 해당 자리가 없으면 0을 채워 길이를 늘리며, pre/post/dev/local 정보는 제거됩니다.

### EDIT: src/packaging/version.py
<<<<<<< SEARCH
        new_version._hash_cache = self._hash_cache
        return new_version


def _parse_letter_version(
=======
        new_version._hash_cache = self._hash_cache
        return new_version

    def bump(self, part: str) -> Version:
        """
        Increment the specified release component.

        >>> Version("1.2.3").bump("major")
        <Version('2.0.0')>
        >>> Version("1.2.3").bump("minor")
        <Version('1.3.0')>
        >>> Version("1.2.3").bump("micro")
        <Version('1.2.4')>
        >>> Version("1.2.3rc1").bump("micro")
        <Version('1.2.4')>

        If the component is beyond the current length, it will be extended with zeros:

        >>> Version("1").bump("micro")
        <Version('1.0.1')>

        :param part: One of "major", "minor", or "micro".
        :raises ValueError: If ``part`` is not valid.
        """
        if part == "major":
            index = 0
        elif part == "minor":
            index = 1
        elif part == "micro":
            index = 2
        else:
            raise ValueError(f"Invalid bump part: {part!r}")

        new_release = list(self._release)
        
        if len(new_release) <= index:
            new_release.extend([0] * (index + 1 - len(new_release)))
            
        new_release[index] += 1
        for i in range(index + 1, len(new_release)):
            new_release[i] = 0

        return self.from_parts(
            epoch=self._epoch,
            release=tuple(new_release),
            pre=None,
            post=None,
            dev=None,
            local=None,
        )


def _parse_letter_version(
>>>>>>> REPLACE