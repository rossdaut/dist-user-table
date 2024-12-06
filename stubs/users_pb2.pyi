from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ONLINE: _ClassVar[Status]
    OFFLINE: _ClassVar[Status]
ONLINE: Status
OFFLINE: Status

class UserId(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    def __init__(self, user_id: _Optional[int] = ...) -> None: ...

class OptionalUserStatus(_message.Message):
    __slots__ = ("status", "exists")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    EXISTS_FIELD_NUMBER: _ClassVar[int]
    status: Status
    exists: bool
    def __init__(self, status: _Optional[_Union[Status, str]] = ..., exists: bool = ...) -> None: ...

class SetStatusRequest(_message.Message):
    __slots__ = ("user_id", "status")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    status: Status
    def __init__(self, user_id: _Optional[int] = ..., status: _Optional[_Union[Status, str]] = ...) -> None: ...

class SetStatusResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
