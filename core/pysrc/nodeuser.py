#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
Y_NODESELECTOR = 'nodeSelector'
Y_NODES = 'nodes'
Y_GROUPS = 'groups'
Y_USERNAME = 'username'
Y_PASSWORD = 'password'
Y_SSHPUBLICKEYS = 'sshPublicKeys'
Y_GROUPBINDINGS = 'groupBindings'
Y_NODE = 'node'
# Package objects (GVK Schemas)
NODEUSER_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='NodeUser')


class GroupBinding:
    def __init__(
        self,
        groups: list[str],
        nodeSelector: list[str] | None = None,
        nodes: list[str] | None = None,
    ):
        self.groups = groups
        self.nodeSelector = nodeSelector
        self.nodes = nodes

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.groups is not None:
            _rval[Y_GROUPS] = self.groups
        if self.nodeSelector is not None:
            _rval[Y_NODESELECTOR] = self.nodeSelector
        if self.nodes is not None:
            _rval[Y_NODES] = self.nodes
        return _rval

    @staticmethod
    def from_input(obj) -> 'GroupBinding | None':
        if obj:
            _groups = obj.get(Y_GROUPS)
            _nodeSelector = obj.get(Y_NODESELECTOR)
            _nodes = obj.get(Y_NODES)
            return GroupBinding(
                groups=_groups,
                nodeSelector=_nodeSelector,
                nodes=_nodes,
            )
        return None  # pragma: no cover


class NodeUserBindingStatus:
    def __init__(
        self,
        node: str | None = None,
        groups: list[str] | None = None,
    ):
        self.node = node
        self.groups = groups

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.node is not None:
            _rval[Y_NODE] = self.node
        if self.groups is not None:
            _rval[Y_GROUPS] = self.groups
        return _rval

    @staticmethod
    def from_input(obj) -> 'NodeUserBindingStatus | None':
        if obj:
            _node = obj.get(Y_NODE)
            _groups = obj.get(Y_GROUPS)
            return NodeUserBindingStatus(
                node=_node,
                groups=_groups,
            )
        return None  # pragma: no cover


class NodeUserSpec:
    def __init__(
        self,
        password: str,
        groupBindings: list[GroupBinding],
        username: str | None = None,
        sshPublicKeys: list[str] | None = None,
    ):
        self.password = password
        self.groupBindings = groupBindings
        self.username = username
        self.sshPublicKeys = sshPublicKeys

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.password is not None:
            _rval[Y_PASSWORD] = self.password
        if self.groupBindings is not None:
            _rval[Y_GROUPBINDINGS] = [x.to_input() for x in self.groupBindings]
        if self.username is not None:
            _rval[Y_USERNAME] = self.username
        if self.sshPublicKeys is not None:
            _rval[Y_SSHPUBLICKEYS] = self.sshPublicKeys
        return _rval

    @staticmethod
    def from_input(obj) -> 'NodeUserSpec | None':
        if obj:
            _password = obj.get(Y_PASSWORD)
            _groupBindings = []
            if obj.get(Y_GROUPBINDINGS) is not None:
                for x in obj.get(Y_GROUPBINDINGS):
                    _groupBindings.append(GroupBinding.from_input(x))
            _username = obj.get(Y_USERNAME)
            _sshPublicKeys = obj.get(Y_SSHPUBLICKEYS)
            return NodeUserSpec(
                password=_password,
                groupBindings=_groupBindings,
                username=_username,
                sshPublicKeys=_sshPublicKeys,
            )
        return None  # pragma: no cover


class NodeUserStatus:
    def __init__(
        self,
        groupBindings: list[NodeUserBindingStatus] | None = None,
    ):
        self.groupBindings = groupBindings

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.groupBindings is not None:
            _rval[Y_GROUPBINDINGS] = [x.to_input() for x in self.groupBindings]
        return _rval

    @staticmethod
    def from_input(obj) -> 'NodeUserStatus | None':
        if obj:
            _groupBindings = []
            if obj.get(Y_GROUPBINDINGS) is not None:
                for x in obj.get(Y_GROUPBINDINGS):
                    _groupBindings.append(NodeUserBindingStatus.from_input(x))
            return NodeUserStatus(
                groupBindings=_groupBindings,
            )
        return None  # pragma: no cover


class NodeUser:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: NodeUserSpec | None = None,
        status: NodeUserStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = NODEUSER_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'NodeUser | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = NodeUserSpec.from_input(obj.get(Y_SPEC, None))
            _status = NodeUserStatus.from_input(obj.get(Y_STATUS))
            return NodeUser(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class NodeUserList:
    def __init__(
        self,
        items: list[NodeUser],
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
    def from_input(obj) -> 'NodeUserList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return NodeUserList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
