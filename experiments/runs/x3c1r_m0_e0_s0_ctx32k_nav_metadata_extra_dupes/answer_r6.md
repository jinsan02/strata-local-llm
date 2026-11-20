`src/packaging/metadata.py` 파일의 `Metadata` 클래스와 `_Validator` 클래스를 수정하여 두 가지 검증 로직을 추가합니다.

1. **Provides-Extra 중복 검사**: `_process_provides_extra` 메서드에서 정규화된 이름이 이미 등장했는지 확인하여 `InvalidMetadata` 예외를 던집니다.
2. **선언되지 않은 Extra 검사**: `Metadata.from_raw` 메서드의 검증 로직 마지막 단계에, `provides_extra`에 정의된 Extras가 `requires_dist`의 마커에서 참조할 때만 유효하도록 하는 검사를 추가합니다. 이 과정은 다른 검증 오류(ExceptionGroup)와 함께 모이도록 설계되었습니다.

<tool_call>
<function=edit_file>
<parameter=path>
src/packaging/metadata.py
</parameter>
<parameter=search>
    def _process_provides_extra(
        self,
        value: list[str],
    ) -> list[utils.NormalizedName]:
        normalized_names = []
        try:
            for name in value:
                normalized_names.append(utils.canonicalize_name(name, validate=True))
        except utils.InvalidName as exc:
            raise self._invalid_metadata(
                f"{name!r} is invalid for {self.raw_name!r}", cause=exc
            ) from exc
        else:
            return normalized_names
</parameter>
<parameter=replace>
    def _process_provides_extra(
        self,
        value: list[str],
    ) -> list[utils.NormalizedName]:
        normalized_names = []
        seen = set()
        try:
            for name in value:
                canon = utils.canonicalize_name(name, validate=True)
                if canon in seen:
                    raise self._invalid_metadata(
                        f"duplicate {name!r}"
                    )
                seen.add(canon)
                normalized_names.append(canon)
        except utils.InvalidName as exc:
            raise self._invalid_metadata(
                f"{name!r} is invalid for {self.raw_name!r}", cause=exc
            ) from exc
        return normalized_names
</parameter>
</function>
</tool_call>