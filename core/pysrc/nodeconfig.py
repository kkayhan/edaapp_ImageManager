#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *

ENUM_NODECONFIGTUPLESPECOPERATION_CREATE = 'Create'
ENUM_NODECONFIGTUPLESPECOPERATION_UPDATE = 'Update'
ENUM_NODECONFIGTUPLESPECOPERATION_DELETE = 'Delete'
Y_PATH = 'path'
Y_CONFIG = 'config'
Y_ENCRYPT = 'encrypt'
Y_OPERATION = 'operation'
Y_NODE_ENDPOINT = 'node-endpoint'
Y_PRIORITY = 'priority'
Y_CONFIGS = 'configs'
# Package objects (GVK Schemas)
NODECONFIG_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='NodeConfig')


class NodeConfigTupleSpec:
    def __init__(
        self,
        path: str,
        operation: str,
        config: str | None = None,
        encrypt: bool | None = None,
    ):
        self.path = path
        self.operation = operation
        self.config = config
        self.encrypt = encrypt

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.path is not None:
            _rval[Y_PATH] = self.path
        if self.operation is not None:
            _rval[Y_OPERATION] = self.operation
        if self.config is not None:
            _rval[Y_CONFIG] = self.config
        if self.encrypt is not None:
            _rval[Y_ENCRYPT] = self.encrypt
        return _rval

    @staticmethod
    def from_input(obj) -> 'NodeConfigTupleSpec | None':
        if obj:
            _path = obj.get(Y_PATH)
            _operation = obj.get(Y_OPERATION)
            _config = obj.get(Y_CONFIG)
            _encrypt = obj.get(Y_ENCRYPT)
            return NodeConfigTupleSpec(
                path=_path,
                operation=_operation,
                config=_config,
                encrypt=_encrypt,
            )
        return None  # pragma: no cover


class NodeConfigSpec:
    def __init__(
        self,
        node_endpoint: str,
        configs: list[NodeConfigTupleSpec],
        priority: int | None = None,
    ):
        self.node_endpoint = node_endpoint
        self.configs = configs
        self.priority = priority

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.node_endpoint is not None:
            _rval[Y_NODE_ENDPOINT] = self.node_endpoint
        if self.configs is not None:
            _rval[Y_CONFIGS] = [x.to_input() for x in self.configs]
        if self.priority is not None:
            _rval[Y_PRIORITY] = self.priority
        return _rval

    @staticmethod
    def from_input(obj) -> 'NodeConfigSpec | None':
        if obj:
            _node_endpoint = obj.get(Y_NODE_ENDPOINT)
            _configs = []
            if obj.get(Y_CONFIGS) is not None:
                for x in obj.get(Y_CONFIGS):
                    _configs.append(NodeConfigTupleSpec.from_input(x))
            _priority = obj.get(Y_PRIORITY, 0)
            return NodeConfigSpec(
                node_endpoint=_node_endpoint,
                configs=_configs,
                priority=_priority,
            )
        return None  # pragma: no cover


class NodeConfigStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'NodeConfigStatus | None':
        if obj:
            return NodeConfigStatus(
            )
        return None  # pragma: no cover


class NodeConfig:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: NodeConfigSpec | None = None,
        status: NodeConfigStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = NODECONFIG_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'NodeConfig | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = NodeConfigSpec.from_input(obj.get(Y_SPEC, None))
            _status = NodeConfigStatus.from_input(obj.get(Y_STATUS))
            return NodeConfig(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class NodeConfigList:
    def __init__(
        self,
        items: list[NodeConfig],
        listMeta: object | None = None
    ):
        self.items = items
        self.listMeta = listMeta

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.items is not None:
            _rval[Y_ITEMS] = self.items
        if self.listMeta is not None:
            _rval[Y_METADATA] = self.listMeta
        return _rval

    @staticmethod
    def from_input(obj) -> 'NodeConfigList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return NodeConfigList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
