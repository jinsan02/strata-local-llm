The previous `edit_file` attempts failed due to exact string matching issues (likely invisible whitespace or encoding differences). I will use the tools again to get the exact content of the target lines and apply the edit correctly.

<tool_call>
<function=read_file>
<parameter=end_line>
310
</parameter>
<parameter=path>
src/packaging/utils.py
</parameter>
<parameter=start_line>
295
</parameter>
</function>
</tool_call>