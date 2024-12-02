from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SuccessorRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: bytes
    def __init__(self, id: _Optional[bytes] = ...) -> None: ...

class OptionalNode(_message.Message):
    __slots__ = ("exists", "node")
    EXISTS_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    exists: bool
    node: Node
    def __init__(self, exists: bool = ..., node: _Optional[_Union[Node, _Mapping]] = ...) -> None: ...

class Node(_message.Message):
    __slots__ = ("id", "ip", "port")
    ID_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    id: bytes
    ip: str
    port: int
    def __init__(self, id: _Optional[bytes] = ..., ip: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
