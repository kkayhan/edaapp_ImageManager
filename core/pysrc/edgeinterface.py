#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *

ENUM_EDGEINTERFACESPECENCAPTYPE_NULL = 'null'
ENUM_EDGEINTERFACESPECENCAPTYPE_DOT1Q = 'dot1q'
Y_IPPREFIX = 'ipPrefix'
Y_PRIMARY = 'primary'
Y_INTERFACERESOURCE = 'interfaceResource'
Y_ROUTER = 'router'
Y_BRIDGEDOMAIN = 'bridgeDomain'
Y_ENCAPTYPE = 'encapType'
Y_VLANID = 'vlanID'
Y_GATEWAYIPV4ADDRESSES = 'gatewayIPV4Addresses'
Y_GATEWAYIPV6ADDRESSES = 'gatewayIPV6Addresses'
# Package objects (GVK Schemas)
EDGEINTERFACE_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='EdgeInterface')


class IPAddress:
    def __init__(
        self,
        ipPrefix: str,
        primary: bool | None = None,
    ):
        self.ipPrefix = ipPrefix
        self.primary = primary

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.ipPrefix is not None:
            _rval[Y_IPPREFIX] = self.ipPrefix
        if self.primary is not None:
            _rval[Y_PRIMARY] = self.primary
        return _rval

    @staticmethod
    def from_input(obj) -> 'IPAddress | None':
        if obj:
            _ipPrefix = obj.get(Y_IPPREFIX)
            _primary = obj.get(Y_PRIMARY)
            return IPAddress(
                ipPrefix=_ipPrefix,
                primary=_primary,
            )
        return None  # pragma: no cover


class EdgeInterfaceSpec:
    def __init__(
        self,
        interfaceResource: str,
        encapType: str,
        router: str | None = None,
        bridgeDomain: str | None = None,
        vlanID: int | None = None,
        gatewayIPV4Addresses: list[IPAddress] | None = None,
        gatewayIPV6Addresses: list[IPAddress] | None = None,
    ):
        self.interfaceResource = interfaceResource
        self.encapType = encapType
        self.router = router
        self.bridgeDomain = bridgeDomain
        self.vlanID = vlanID
        self.gatewayIPV4Addresses = gatewayIPV4Addresses
        self.gatewayIPV6Addresses = gatewayIPV6Addresses

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.interfaceResource is not None:
            _rval[Y_INTERFACERESOURCE] = self.interfaceResource
        if self.encapType is not None:
            _rval[Y_ENCAPTYPE] = self.encapType
        if self.router is not None:
            _rval[Y_ROUTER] = self.router
        if self.bridgeDomain is not None:
            _rval[Y_BRIDGEDOMAIN] = self.bridgeDomain
        if self.vlanID is not None:
            _rval[Y_VLANID] = self.vlanID
        if self.gatewayIPV4Addresses is not None:
            _rval[Y_GATEWAYIPV4ADDRESSES] = [x.to_input() for x in self.gatewayIPV4Addresses]
        if self.gatewayIPV6Addresses is not None:
            _rval[Y_GATEWAYIPV6ADDRESSES] = [x.to_input() for x in self.gatewayIPV6Addresses]
        return _rval

    @staticmethod
    def from_input(obj) -> 'EdgeInterfaceSpec | None':
        if obj:
            _interfaceResource = obj.get(Y_INTERFACERESOURCE)
            _encapType = obj.get(Y_ENCAPTYPE, "null")
            _router = obj.get(Y_ROUTER)
            _bridgeDomain = obj.get(Y_BRIDGEDOMAIN)
            _vlanID = obj.get(Y_VLANID)
            _gatewayIPV4Addresses = []
            if obj.get(Y_GATEWAYIPV4ADDRESSES) is not None:
                for x in obj.get(Y_GATEWAYIPV4ADDRESSES):
                    _gatewayIPV4Addresses.append(IPAddress.from_input(x))
            _gatewayIPV6Addresses = []
            if obj.get(Y_GATEWAYIPV6ADDRESSES) is not None:
                for x in obj.get(Y_GATEWAYIPV6ADDRESSES):
                    _gatewayIPV6Addresses.append(IPAddress.from_input(x))
            return EdgeInterfaceSpec(
                interfaceResource=_interfaceResource,
                encapType=_encapType,
                router=_router,
                bridgeDomain=_bridgeDomain,
                vlanID=_vlanID,
                gatewayIPV4Addresses=_gatewayIPV4Addresses,
                gatewayIPV6Addresses=_gatewayIPV6Addresses,
            )
        return None  # pragma: no cover


class EdgeInterfaceStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'EdgeInterfaceStatus | None':
        if obj:
            return EdgeInterfaceStatus(
            )
        return None  # pragma: no cover


class EdgeInterface:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: EdgeInterfaceSpec | None = None,
        status: EdgeInterfaceStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = EDGEINTERFACE_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'EdgeInterface | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = EdgeInterfaceSpec.from_input(obj.get(Y_SPEC, None))
            _status = EdgeInterfaceStatus.from_input(obj.get(Y_STATUS))
            return EdgeInterface(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class EdgeInterfaceList:
    def __init__(
        self,
        items: list[EdgeInterface],
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
    def from_input(obj) -> 'EdgeInterfaceList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return EdgeInterfaceList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
