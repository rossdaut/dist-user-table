# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from stubs import chord_pb2 as stubs_dot_chord__pb2

GRPC_GENERATED_VERSION = '1.68.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in stubs/chord_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class ChordStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.FindSuccessor = channel.unary_unary(
                '/Chord/FindSuccessor',
                request_serializer=stubs_dot_chord__pb2.SuccessorRequest.SerializeToString,
                response_deserializer=stubs_dot_chord__pb2.Node.FromString,
                _registered_method=True)
        self.Predecessor = channel.unary_unary(
                '/Chord/Predecessor',
                request_serializer=stubs_dot_chord__pb2.Empty.SerializeToString,
                response_deserializer=stubs_dot_chord__pb2.OptionalNode.FromString,
                _registered_method=True)
        self.Notify = channel.unary_unary(
                '/Chord/Notify',
                request_serializer=stubs_dot_chord__pb2.Node.SerializeToString,
                response_deserializer=stubs_dot_chord__pb2.Empty.FromString,
                _registered_method=True)


class ChordServicer(object):
    """Missing associated documentation comment in .proto file."""

    def FindSuccessor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Predecessor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Notify(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ChordServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'FindSuccessor': grpc.unary_unary_rpc_method_handler(
                    servicer.FindSuccessor,
                    request_deserializer=stubs_dot_chord__pb2.SuccessorRequest.FromString,
                    response_serializer=stubs_dot_chord__pb2.Node.SerializeToString,
            ),
            'Predecessor': grpc.unary_unary_rpc_method_handler(
                    servicer.Predecessor,
                    request_deserializer=stubs_dot_chord__pb2.Empty.FromString,
                    response_serializer=stubs_dot_chord__pb2.OptionalNode.SerializeToString,
            ),
            'Notify': grpc.unary_unary_rpc_method_handler(
                    servicer.Notify,
                    request_deserializer=stubs_dot_chord__pb2.Node.FromString,
                    response_serializer=stubs_dot_chord__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Chord', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('Chord', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Chord(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def FindSuccessor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Chord/FindSuccessor',
            stubs_dot_chord__pb2.SuccessorRequest.SerializeToString,
            stubs_dot_chord__pb2.Node.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Predecessor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Chord/Predecessor',
            stubs_dot_chord__pb2.Empty.SerializeToString,
            stubs_dot_chord__pb2.OptionalNode.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Notify(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Chord/Notify',
            stubs_dot_chord__pb2.Node.SerializeToString,
            stubs_dot_chord__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)