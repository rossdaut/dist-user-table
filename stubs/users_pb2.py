# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: stubs/users.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'stubs/users.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11stubs/users.proto\x1a\x1bgoogle/protobuf/empty.proto\"\x19\n\x06UserId\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\"=\n\x12OptionalUserStatus\x12\x17\n\x06status\x18\x01 \x01(\x0e\x32\x07.Status\x12\x0e\n\x06\x65xists\x18\x02 \x01(\x08\"<\n\x10SetStatusRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\x12\x17\n\x06status\x18\x02 \x01(\x0e\x32\x07.Status\"\x1b\n\x08Response\x12\x0f\n\x07success\x18\x01 \x01(\x08\"f\n\x08UsersMap\x12#\n\x05users\x18\x01 \x03(\x0b\x32\x14.UsersMap.UsersEntry\x1a\x35\n\nUsersEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\x16\n\x05value\x18\x02 \x01(\x0e\x32\x07.Status:\x02\x38\x01*!\n\x06Status\x12\n\n\x06ONLINE\x10\x00\x12\x0b\n\x07OFFLINE\x10\x01\x32\xc8\x01\n\x05Users\x12/\n\rGetUserStatus\x12\x07.UserId\x1a\x13.OptionalUserStatus\"\x00\x12/\n\rSetUserStatus\x12\x11.SetStatusRequest\x1a\t.Response\"\x00\x12\'\n\rTransferUsers\x12\t.UsersMap\x1a\t.Response\"\x00\x12\x34\n\rRequestBackup\x12\x16.google.protobuf.Empty\x1a\t.UsersMap\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'stubs.users_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_USERSMAP_USERSENTRY']._loaded_options = None
  _globals['_USERSMAP_USERSENTRY']._serialized_options = b'8\001'
  _globals['_STATUS']._serialized_start=335
  _globals['_STATUS']._serialized_end=368
  _globals['_USERID']._serialized_start=50
  _globals['_USERID']._serialized_end=75
  _globals['_OPTIONALUSERSTATUS']._serialized_start=77
  _globals['_OPTIONALUSERSTATUS']._serialized_end=138
  _globals['_SETSTATUSREQUEST']._serialized_start=140
  _globals['_SETSTATUSREQUEST']._serialized_end=200
  _globals['_RESPONSE']._serialized_start=202
  _globals['_RESPONSE']._serialized_end=229
  _globals['_USERSMAP']._serialized_start=231
  _globals['_USERSMAP']._serialized_end=333
  _globals['_USERSMAP_USERSENTRY']._serialized_start=280
  _globals['_USERSMAP_USERSENTRY']._serialized_end=333
  _globals['_USERS']._serialized_start=371
  _globals['_USERS']._serialized_end=571
# @@protoc_insertion_point(module_scope)
