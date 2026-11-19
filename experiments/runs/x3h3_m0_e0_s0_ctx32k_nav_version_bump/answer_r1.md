`packaging.version.Version` 클래스에 `bump(part)` 메서드를 추가했습니다. 이 메서드는 지정된 부분(`major`, `minor`, `micro`)의 release 숫자를 1 증가시키고, 뒤따르는 숫자들을 0으로 초기화하여 새 버전을 반환합니다. 전사절(e.g., pre, post, dev)과 로컬 버전(local)은 삭제됩니다.

### EDIT: src/packaging/version.py
<<<<<<< SEARCH
          return new_version

      @property
=======
          return new_version
  
      def bump(self, part: str) -> Version:
          """Bump a version component and reset the following components to 0.
  
          :param part: The component to bump. Must be one of ``"major"``,
              ``"minor"``, or ``"micro"``. Case-sensitive.
          :raises ValueError: If ``part`` is not a valid component name.
  
          >>> Version("1.2.3").bump("major")
          <Version('2.0.0')>
          >>> Version("1.2.3").bump("minor")
          <Version('1.3.0')>
          >>> Version("1.2.3").bump("micro")
          <Version('1.2.4')>
          >>> Version("1").bump("micro")
          <Version('1.0.1')>
  
          The pre-release, post-release, dev, and local segments are discarded.
          """
          if part not in ("major", "minor", "micro"):
              raise ValueError(
                  f"Invalid part: {part!r}. Must be one of 'major', 'minor', or 'micro'."
              )
  
          indices = {"major": 0, "minor": 1, "micro": 2}
          idx = indices[part]
  
          release = list(self._release)
  
          # Ensure the release tuple is long enough to contain the target index
          while len(release) <= idx:
              release.append(0)
  
          # Increment the target component
          release[idx] += 1
  
          # Reset all following components to 0
          for i in range(idx + 1, len(release)):
              release[i] = 0
  
          return self.__replace__(
              release=tuple(release), pre=None, post=None, dev=None, local=None
          )
  
      @property
>>>>>>> REPLACE