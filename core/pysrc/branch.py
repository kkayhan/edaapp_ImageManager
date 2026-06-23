#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
Y_CLUSTERPROVIDER = 'clusterProvider'
Y_PHASE = 'phase'
Y_ADDRESS = 'address'
Y_PORT = 'port'
Y_GRPCPORT = 'gRPCPort'
Y_KUBECONFIGSECRET = 'kubeconfigSecret'
Y_PROXYADDRESS = 'proxyAddress'
Y_PROXYPORT = 'proxyPort'
# Package objects (GVK Schemas)
BRANCH_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='Branch')


class BranchSpec:
    def __init__(
        self,
        clusterProvider: str | None = None,
    ):
        self.clusterProvider = clusterProvider

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.clusterProvider is not None:
            _rval[Y_CLUSTERPROVIDER] = self.clusterProvider
        return _rval

    @staticmethod
    def from_input(obj) -> 'BranchSpec | None':
        if obj:
            _clusterProvider = obj.get(Y_CLUSTERPROVIDER)
            return BranchSpec(
                clusterProvider=_clusterProvider,
            )
        return None  # pragma: no cover


class BranchStatus:
    def __init__(
        self,
        phase: str | None = None,
        address: str | None = None,
        port: int | None = None,
        gRPCPort: int | None = None,
        kubeconfigSecret: str | None = None,
        proxyAddress: str | None = None,
        proxyPort: int | None = None,
    ):
        self.phase = phase
        self.address = address
        self.port = port
        self.gRPCPort = gRPCPort
        self.kubeconfigSecret = kubeconfigSecret
        self.proxyAddress = proxyAddress
        self.proxyPort = proxyPort

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.phase is not None:
            _rval[Y_PHASE] = self.phase
        if self.address is not None:
            _rval[Y_ADDRESS] = self.address
        if self.port is not None:
            _rval[Y_PORT] = self.port
        if self.gRPCPort is not None:
            _rval[Y_GRPCPORT] = self.gRPCPort
        if self.kubeconfigSecret is not None:
            _rval[Y_KUBECONFIGSECRET] = self.kubeconfigSecret
        if self.proxyAddress is not None:
            _rval[Y_PROXYADDRESS] = self.proxyAddress
        if self.proxyPort is not None:
            _rval[Y_PROXYPORT] = self.proxyPort
        return _rval

    @staticmethod
    def from_input(obj) -> 'BranchStatus | None':
        if obj:
            _phase = obj.get(Y_PHASE)
            _address = obj.get(Y_ADDRESS)
            _port = obj.get(Y_PORT)
            _gRPCPort = obj.get(Y_GRPCPORT)
            _kubeconfigSecret = obj.get(Y_KUBECONFIGSECRET)
            _proxyAddress = obj.get(Y_PROXYADDRESS)
            _proxyPort = obj.get(Y_PROXYPORT)
            return BranchStatus(
                phase=_phase,
                address=_address,
                port=_port,
                gRPCPort=_gRPCPort,
                kubeconfigSecret=_kubeconfigSecret,
                proxyAddress=_proxyAddress,
                proxyPort=_proxyPort,
            )
        return None  # pragma: no cover


class Branch:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: BranchSpec | None = None,
        status: BranchStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = BRANCH_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'Branch | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = BranchSpec.from_input(obj.get(Y_SPEC, None))
            _status = BranchStatus.from_input(obj.get(Y_STATUS))
            return Branch(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class BranchList:
    def __init__(
        self,
        items: list[Branch],
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
    def from_input(obj) -> 'BranchList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return BranchList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
