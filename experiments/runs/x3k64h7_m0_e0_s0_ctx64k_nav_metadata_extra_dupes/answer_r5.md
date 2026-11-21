<tool_call>
<function=edit_file>
<parameter=new_string>
    _extract(marker)
    return extras


_STRING_FIELDS = {
    "author",
    "author_email",
    "description",
    "description_content_type",
    "download_url",
    "home_page",
    "license",
    "license_expression",
    "maintainer",
    "maintainer_email",
    "metadata_version",
    "name",
    "requires_python",
    "summary",
    "version",
}
</parameter>
<parameter=old_string>
    _extract(marker)
    return extras


def _STRING_FIELDS = {
    "author",
    "author_email",
    "description",
    "description_content_type",
    "download_url",
    "home_page",
    "license",
    "license_expression",
    "maintainer",
    "maintainer_email",
    "metadata_version",
    "name",
    "requires_python",
    "summary",
    "version",
}
</parameter>
<parameter=path>
src/packaging/metadata.py
</parameter>
</function>
</tool_call>