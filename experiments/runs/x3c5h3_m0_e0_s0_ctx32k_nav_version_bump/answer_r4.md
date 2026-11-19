<tool_call>
<function=run_shell>
<parameter=command>
python -c "from packaging.version import Version; v = Version('1.2.3'); print(v.bump('major'))"
</parameter>
</function>
</tool_call>