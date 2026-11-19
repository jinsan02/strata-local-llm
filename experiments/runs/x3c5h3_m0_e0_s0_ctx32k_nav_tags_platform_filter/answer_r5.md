`src/packaging/utils.py` 파일의 `parse_wheel_filename` 함수에 대해 다음 내용을 수정했습니다:

1.  **시그니처 변경**: `platforms=None` 키워드 전용 인자를 추가했습니다.
2.  **검증 로직 추가**: 반환 전에 플랫폼 검증 로직을 구현했습니다.
    *   `str` 타입 전달 시 `TypeError` 발생 처리.
    *   제공된 `platforms`와 태그의 플랫폼을 정규화(`.`, `-`, 공백 → `_`, 소문자)하여 비교.
    *   `'any'` 플랫폼은 항상 통과하도록 로직 추가.
    *   조건 불일치 시 `InvalidWheelFilename` 예외 발생.

수정된 파일 (`src/packaging/utils.py`) 내용 요약:

```python
def parse_wheel_filename(
    filename: str,
    *,
    validate_order: bool = False,
    platforms=None,  # 추가됨
) -> tuple[NormalizedName, Version, BuildTag, frozenset[Tag]]:
    # ... 기존 유효성 검사 코드 ...

    if platforms is not None:
        if isinstance(platforms, str):
            raise TypeError("platforms must be an iterable of strings, not a string")
        
        allowed = set()
        for p in platforms:
            allowed.add(re.sub(r'[\s.\-]', '_', p).lower())
            
        match_found = False
        for tag in tags:
            norm_p = re.sub(r'[\s.\-]', '_', tag.platform).lower()
            if norm_p == 'any':
                match_found = True
                break
            if norm_p in allowed:
                match_found = True
                break
        
        if not match_found:
            raise InvalidWheelFilename(
                f"Invalid wheel filename (incompatible platform tags): {filename!r}"
            )

    return (name, version, build, tags)
```