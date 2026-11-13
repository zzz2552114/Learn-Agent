from .registry import ToolManager,ToolSpec
from .Tools import MagicArgs,magic_operation

add_tool = ToolSpec(name="magic_operation",
                    description='a magic python funtion: Input two integers, perform a magic operation, and output one integer.',
                    parameters=MagicArgs,
                    handler=magic_operation,
                    read_only=True)

manager = ToolManager()
manager.register(add_tool)