<tool_call>
<function=edit_file>
<parameter=path>
src/packaging/markers.py
</parameter>
<parameter=search_text>
from .utils import canonicalize_name
</parameter>
<parameter=new_text>
from .utils import NormalizedName, canonicalize_name
</parameter>
</function>
</tool_call>