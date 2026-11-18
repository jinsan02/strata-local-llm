The issue is that generated unittest fixtures (like `setUpClass`) are being exposed in `pytest --fixtures` output without the `-v` flag. In pytest, fixtures whose names start with an underscore (`_`) are considered private/hidden and won't appear in the default fixtures listing.

I need to prefix the fixture name with an underscore to make it hidden:

<tool_call>
<function=SEARCH_PART>
</function>
</tool_call>