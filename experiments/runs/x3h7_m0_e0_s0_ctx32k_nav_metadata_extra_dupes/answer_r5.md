<tool_call>
<function=edit_file>
<parameter=path>
src/packaging/metadata.py
</parameter>
<parameter=old_string>
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from .errors import ExceptionGroup, _ErrorCollector
</parameter>
<parameter=new_string>
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from ._parser import Variable, Value
from .errors import ExceptionGroup, _ErrorCollector
</parameter>
</function>
</tool_call>