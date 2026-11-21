<tool_call>
<function=edit_file>
<parameter=new_string>
from .utils import NormalizedName, canonicalize_name

if TYPE_CHECKING:
    from collections.abc import Mapping
</parameter>
<parameter=old_string>
from .utils import canonicalize_name

if TYPE_CHECKING:
    from collections.abc import Mapping
</parameter>
<parameter=path>
src/packaging/markers.py
</parameter>
</function>
</tool_call>