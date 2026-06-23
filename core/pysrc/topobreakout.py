#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *

ENUM_TOPOBREAKOUTSPECSPEED_800G = '800G'
ENUM_TOPOBREAKOUTSPECSPEED_400G = '400G'
ENUM_TOPOBREAKOUTSPECSPEED_200G = '200G'
ENUM_TOPOBREAKOUTSPECSPEED_100G = '100G'
ENUM_TOPOBREAKOUTSPECSPEED_50G = '50G'
ENUM_TOPOBREAKOUTSPECSPEED_40G = '40G'
ENUM_TOPOBREAKOUTSPECSPEED_25G = '25G'
ENUM_TOPOBREAKOUTSPECSPEED_10G = '10G'
Y_NODE = 'node'
Y_INTERFACE = 'interface'
Y_CHANNELS = 'channels'
Y_SPEED = 'speed'
# Package objects (GVK Schemas)
TOPOBREAKOUT_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='TopoBreakout')


class TopoBreakoutSpec:
    def __init__(
        self,
        node: list[str],
        channels: int,
        speed: str,
        interface: list[str] | None = None,
    ):
        self.node = node
        self.channels = channels
        self.speed = speed
        self.interface = interface

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.node is not None:
            _rval[Y_NODE] = self.node
        if self.channels is not None:
            _rval[Y_CHANNELS] = self.channels
        if self.speed is not None:
            _rval[Y_SPEED] = self.speed
        if self.interface is not None:
            _rval[Y_INTERFACE] = self.interface
        return _rval

    @staticmethod
    def from_input(obj) -> 'TopoBreakoutSpec | None':
        if obj:
            _node = obj.get(Y_NODE)
            _channels = obj.get(Y_CHANNELS)
            _speed = obj.get(Y_SPEED)
            _interface = obj.get(Y_INTERFACE)
            return TopoBreakoutSpec(
                node=_node,
                channels=_channels,
                speed=_speed,
                interface=_interface,
            )
        return None  # pragma: no cover


class TopoBreakoutStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'TopoBreakoutStatus | None':
        if obj:
            return TopoBreakoutStatus(
            )
        return None  # pragma: no cover


class TopoBreakout:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: TopoBreakoutSpec | None = None,
        status: TopoBreakoutStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = TOPOBREAKOUT_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'TopoBreakout | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = TopoBreakoutSpec.from_input(obj.get(Y_SPEC, None))
            _status = TopoBreakoutStatus.from_input(obj.get(Y_STATUS))
            return TopoBreakout(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class TopoBreakoutList:
    def __init__(
        self,
        items: list[TopoBreakout],
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
    def from_input(obj) -> 'TopoBreakoutList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return TopoBreakoutList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
