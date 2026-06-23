#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
Y_PROXYPORT = 'proxyPort'
Y_DESTHOST = 'destHost'
Y_DESTPORT = 'destPort'
Y_IDLETIMEOUT = 'idleTimeout'
Y_BUFFERSIZE = 'bufferSize'
# Package objects (GVK Schemas)
UDPPROXY_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='UdpProxy')


class UdpProxySpec:
    def __init__(
        self,
        proxyPort: int,
        destHost: str,
        destPort: int,
        idleTimeout: int,
        bufferSize: int,
    ):
        self.proxyPort = proxyPort
        self.destHost = destHost
        self.destPort = destPort
        self.idleTimeout = idleTimeout
        self.bufferSize = bufferSize

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.proxyPort is not None:
            _rval[Y_PROXYPORT] = self.proxyPort
        if self.destHost is not None:
            _rval[Y_DESTHOST] = self.destHost
        if self.destPort is not None:
            _rval[Y_DESTPORT] = self.destPort
        if self.idleTimeout is not None:
            _rval[Y_IDLETIMEOUT] = self.idleTimeout
        if self.bufferSize is not None:
            _rval[Y_BUFFERSIZE] = self.bufferSize
        return _rval

    @staticmethod
    def from_input(obj) -> 'UdpProxySpec | None':
        if obj:
            _proxyPort = obj.get(Y_PROXYPORT)
            _destHost = obj.get(Y_DESTHOST)
            _destPort = obj.get(Y_DESTPORT)
            _idleTimeout = obj.get(Y_IDLETIMEOUT)
            _bufferSize = obj.get(Y_BUFFERSIZE)
            return UdpProxySpec(
                proxyPort=_proxyPort,
                destHost=_destHost,
                destPort=_destPort,
                idleTimeout=_idleTimeout,
                bufferSize=_bufferSize,
            )
        return None  # pragma: no cover


class UdpProxyStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'UdpProxyStatus | None':
        if obj:
            return UdpProxyStatus(
            )
        return None  # pragma: no cover


class UdpProxy:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: UdpProxySpec | None = None,
        status: UdpProxyStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = UDPPROXY_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'UdpProxy | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = UdpProxySpec.from_input(obj.get(Y_SPEC, None))
            _status = UdpProxyStatus.from_input(obj.get(Y_STATUS))
            return UdpProxy(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class UdpProxyList:
    def __init__(
        self,
        items: list[UdpProxy],
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
    def from_input(obj) -> 'UdpProxyList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return UdpProxyList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
