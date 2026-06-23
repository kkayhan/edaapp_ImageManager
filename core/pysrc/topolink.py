#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *

ENUM_TOPOLINKMEMBERTYPE_EDGE = 'edge'
ENUM_TOPOLINKMEMBERTYPE_INTERSWITCH = 'interSwitch'
ENUM_TOPOLINKMEMBERTYPE_LOOPBACK = 'loopback'

ENUM_TOPOLINKMEMBERSPEED_800G = '800G'
ENUM_TOPOLINKMEMBERSPEED_400G = '400G'
ENUM_TOPOLINKMEMBERSPEED_200G = '200G'
ENUM_TOPOLINKMEMBERSPEED_100G = '100G'
ENUM_TOPOLINKMEMBERSPEED_50G = '50G'
ENUM_TOPOLINKMEMBERSPEED_40G = '40G'
ENUM_TOPOLINKMEMBERSPEED_25G = '25G'
ENUM_TOPOLINKMEMBERSPEED_10G = '10G'
ENUM_TOPOLINKMEMBERSPEED_2_5G = '2.5G'
ENUM_TOPOLINKMEMBERSPEED_1G = '1G'
ENUM_TOPOLINKMEMBERSPEED_100M = '100M'
Y_LINKS = 'links'
Y_LOCAL = 'local'
Y_REMOTE = 'remote'
Y_TYPE = 'type'
Y_SPEED = 'speed'
Y_NODE = 'node'
Y_INTERFACERESOURCE = 'interfaceResource'
Y_INTERFACE = 'interface'
Y_OPERATIONALSTATE = 'operationalState'
Y_MEMBERS = 'members'
# Package objects (GVK Schemas)
TOPOLINK_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='TopoLink')


class Endpoint:
    def __init__(
        self,
        node: str,
        interfaceResource: str,
        interface: str | None = None,
    ):
        self.node = node
        self.interfaceResource = interfaceResource
        self.interface = interface

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.node is not None:
            _rval[Y_NODE] = self.node
        if self.interfaceResource is not None:
            _rval[Y_INTERFACERESOURCE] = self.interfaceResource
        if self.interface is not None:
            _rval[Y_INTERFACE] = self.interface
        return _rval

    @staticmethod
    def from_input(obj) -> 'Endpoint | None':
        if obj:
            _node = obj.get(Y_NODE)
            _interfaceResource = obj.get(Y_INTERFACERESOURCE)
            _interface = obj.get(Y_INTERFACE)
            return Endpoint(
                node=_node,
                interfaceResource=_interfaceResource,
                interface=_interface,
            )
        return None  # pragma: no cover


class MemberStatus:
    def __init__(
        self,
        operationalState: str,
        node: str,
        interface: str | None = None,
    ):
        self.operationalState = operationalState
        self.node = node
        self.interface = interface

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.operationalState is not None:
            _rval[Y_OPERATIONALSTATE] = self.operationalState
        if self.node is not None:
            _rval[Y_NODE] = self.node
        if self.interface is not None:
            _rval[Y_INTERFACE] = self.interface
        return _rval

    @staticmethod
    def from_input(obj) -> 'MemberStatus | None':
        if obj:
            _operationalState = obj.get(Y_OPERATIONALSTATE)
            _node = obj.get(Y_NODE)
            _interface = obj.get(Y_INTERFACE)
            return MemberStatus(
                operationalState=_operationalState,
                node=_node,
                interface=_interface,
            )
        return None  # pragma: no cover


class TopoLinkMember:
    def __init__(
        self,
        local: Endpoint,
        type: str,
        remote: Endpoint | None = None,
        speed: str | None = None,
    ):
        self.local = local
        self.type = type
        self.remote = remote
        self.speed = speed

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.local is not None:
            _rval[Y_LOCAL] = self.local.to_input()
        if self.type is not None:
            _rval[Y_TYPE] = self.type
        if self.remote is not None:
            _rval[Y_REMOTE] = self.remote.to_input()
        if self.speed is not None:
            _rval[Y_SPEED] = self.speed
        return _rval

    @staticmethod
    def from_input(obj) -> 'TopoLinkMember | None':
        if obj:
            _local = Endpoint.from_input(obj.get(Y_LOCAL))
            _type = obj.get(Y_TYPE)
            _remote = Endpoint.from_input(obj.get(Y_REMOTE))
            _speed = obj.get(Y_SPEED)
            return TopoLinkMember(
                local=_local,
                type=_type,
                remote=_remote,
                speed=_speed,
            )
        return None  # pragma: no cover


class TopoLinkSpec:
    def __init__(
        self,
        links: list[TopoLinkMember],
    ):
        self.links = links

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.links is not None:
            _rval[Y_LINKS] = [x.to_input() for x in self.links]
        return _rval

    @staticmethod
    def from_input(obj) -> 'TopoLinkSpec | None':
        if obj:
            _links = []
            if obj.get(Y_LINKS) is not None:
                for x in obj.get(Y_LINKS):
                    _links.append(TopoLinkMember.from_input(x))
            return TopoLinkSpec(
                links=_links,
            )
        return None  # pragma: no cover


class TopoLinkStatus:
    def __init__(
        self,
        operationalState: str,
        members: list[MemberStatus] | None = None,
    ):
        self.operationalState = operationalState
        self.members = members

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.operationalState is not None:
            _rval[Y_OPERATIONALSTATE] = self.operationalState
        if self.members is not None:
            _rval[Y_MEMBERS] = [x.to_input() for x in self.members]
        return _rval

    @staticmethod
    def from_input(obj) -> 'TopoLinkStatus | None':
        if obj:
            _operationalState = obj.get(Y_OPERATIONALSTATE)
            _members = []
            if obj.get(Y_MEMBERS) is not None:
                for x in obj.get(Y_MEMBERS):
                    _members.append(MemberStatus.from_input(x))
            return TopoLinkStatus(
                operationalState=_operationalState,
                members=_members,
            )
        return None  # pragma: no cover


class TopoLink:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: TopoLinkSpec | None = None,
        status: TopoLinkStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = TOPOLINK_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'TopoLink | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = TopoLinkSpec.from_input(obj.get(Y_SPEC, None))
            _status = TopoLinkStatus.from_input(obj.get(Y_STATUS))
            return TopoLink(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class TopoLinkList:
    def __init__(
        self,
        items: list[TopoLink],
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
    def from_input(obj) -> 'TopoLinkList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return TopoLinkList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
