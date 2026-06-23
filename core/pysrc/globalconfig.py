#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
from .engineconfig import ClusterExternal
Y_DHCP = 'dhcp'
# Package objects (GVK Schemas)
GLOBALCONFIG_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='GlobalConfig')


class GlobalConfigSpec:
    def __init__(
        self,
        dhcp: ClusterExternal | None = None,
    ):
        self.dhcp = dhcp

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.dhcp is not None:
            _rval[Y_DHCP] = self.dhcp.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'GlobalConfigSpec | None':
        if obj:
            _dhcp = ClusterExternal.from_input(obj.get(Y_DHCP))
            return GlobalConfigSpec(
                dhcp=_dhcp,
            )
        return None  # pragma: no cover


class GlobalConfig:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: GlobalConfigSpec | None = None,
        status: GlobalConfigStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = GLOBALCONFIG_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'GlobalConfig | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = GlobalConfigSpec.from_input(obj.get(Y_SPEC, None))
            _status = GlobalConfigStatus.from_input(obj.get(Y_STATUS))
            return GlobalConfig(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class GlobalConfigList:
    def __init__(
        self,
        items: list[GlobalConfig],
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
    def from_input(obj) -> 'GlobalConfigList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return GlobalConfigList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
