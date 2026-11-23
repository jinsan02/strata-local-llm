사용자 버그 보고를 받았다. 원인을 찾아 고쳐라.

> `1.0.post1.dev2` 같은 '사후 릴리스의 개발판' 버전이 이상하게 정렬됩니다.
>
> ```python
> >>> from packaging.version import Version
> >>> sorted(["1.0", "1.0a1", "1.0.post1.dev2", "1.0.post1"], key=Version)
> ['1.0.post1.dev2', '1.0a1', '1.0', '1.0.post1']
> >>> from packaging.specifiers import SpecifierSet
> >>> SpecifierSet(">=1.0", prereleases=True).contains("1.0.post1.dev2")
> False
> ```
>
> PEP 440 대로라면 정렬 결과는 `['1.0a1', '1.0', '1.0.post1.dev2', '1.0.post1']` 이고, 두 번째 결과는 `True` 여야 합니다.

- 보고된 증상을 고치되, 다른 버전들의 순서는 그대로여야 한다(예: 개발판 `1.0.dev1` 은 `1.0a1` 보다 앞, `1.0rc1.dev1` 은 `1.0rc1` 보다 앞, `1.0` 은 `1.0.post1.dev1` 보다 앞).
- 원인이 있는 곳을 고쳐라. 증상이 보이는 함수에 예외 처리를 덧붙이는 식으로 덮지 마라.
- 테스트 파일은 고치지 마라.
