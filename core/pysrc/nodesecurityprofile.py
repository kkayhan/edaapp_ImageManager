#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
from .targetnode import TLS
Y_NODESELECTOR = 'nodeSelector'
Y_NODES = 'nodes'
Y_TLS = 'tls'
Y_NAMESPACE = 'namespace'
# Package objects (GVK Schemas)
NODESECURITYPROFILE_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='NodeSecurityProfile')


class NodeSecurityProfileSpec:
    def __init__(
        self,
        nodeSelector: list[str] | None = None,
        nodes: list[str] | None = None,
        tls: TLS | None = None,
        namespace: str | None = None,
    ):
        self.nodeSelector = nodeSelector
        self.nodes = nodes
        self.tls = tls
        self.namespace = namespace

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.nodeSelector is not None:
            _rval[Y_NODESELECTOR] = self.nodeSelector
        if self.nodes is not None:
            _rval[Y_NODES] = self.nodes
        if self.tls is not None:
            _rval[Y_TLS] = self.tls.to_input()
        if self.namespace is not None:
            _rval[Y_NAMESPACE] = self.namespace
        return _rval

    @staticmethod
    def from_input(obj) -> 'NodeSecurityProfileSpec | None':
        if obj:
            _nodeSelector = obj.get(Y_NODESELECTOR)
            _nodes = obj.get(Y_NODES)
            _tls = TLS.from_input(obj.get(Y_TLS))
            _namespace = obj.get(Y_NAMESPACE)
            return NodeSecurityProfileSpec(
                nodeSelector=_nodeSelector,
                nodes=_nodes,
                tls=_tls,
                namespace=_namespace,
            )
        return None  # pragma: no cover


class NodeSecurityProfileStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'NodeSecurityProfileStatus | None':
        if obj:
            return NodeSecurityProfileStatus(
            )
        return None  # pragma: no cover


class NodeSecurityProfile:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: NodeSecurityProfileSpec | None = None,
        status: NodeSecurityProfileStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = NODESECURITYPROFILE_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'NodeSecurityProfile | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = NodeSecurityProfileSpec.from_input(obj.get(Y_SPEC, None))
            _status = NodeSecurityProfileStatus.from_input(obj.get(Y_STATUS))
            return NodeSecurityProfile(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class NodeSecurityProfileList:
    def __init__(
        self,
        items: list[NodeSecurityProfile],
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
    def from_input(obj) -> 'NodeSecurityProfileList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return NodeSecurityProfileList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
