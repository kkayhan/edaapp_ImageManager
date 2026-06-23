#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
Y_KUBECONFIGSECRET = 'kubeconfigSecret'
Y_NOVIRTUALCLUSTER = 'noVirtualCluster'
Y_ADDRESS = 'address'
Y_STARTPORTRANGE = 'startPortRange'
# Package objects (GVK Schemas)
CLUSTERPROVIDER_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='ClusterProvider')


class ClusterProviderSpec:
    def __init__(
        self,
        kubeconfigSecret: str | None = None,
        noVirtualCluster: bool | None = None,
        address: str | None = None,
        startPortRange: int | None = None,
    ):
        self.kubeconfigSecret = kubeconfigSecret
        self.noVirtualCluster = noVirtualCluster
        self.address = address
        self.startPortRange = startPortRange

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.kubeconfigSecret is not None:
            _rval[Y_KUBECONFIGSECRET] = self.kubeconfigSecret
        if self.noVirtualCluster is not None:
            _rval[Y_NOVIRTUALCLUSTER] = self.noVirtualCluster
        if self.address is not None:
            _rval[Y_ADDRESS] = self.address
        if self.startPortRange is not None:
            _rval[Y_STARTPORTRANGE] = self.startPortRange
        return _rval

    @staticmethod
    def from_input(obj) -> 'ClusterProviderSpec | None':
        if obj:
            _kubeconfigSecret = obj.get(Y_KUBECONFIGSECRET)
            _noVirtualCluster = obj.get(Y_NOVIRTUALCLUSTER)
            _address = obj.get(Y_ADDRESS)
            _startPortRange = obj.get(Y_STARTPORTRANGE)
            return ClusterProviderSpec(
                kubeconfigSecret=_kubeconfigSecret,
                noVirtualCluster=_noVirtualCluster,
                address=_address,
                startPortRange=_startPortRange,
            )
        return None  # pragma: no cover


class ClusterProviderStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'ClusterProviderStatus | None':
        if obj:
            return ClusterProviderStatus(
            )
        return None  # pragma: no cover


class ClusterProvider:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: ClusterProviderSpec | None = None,
        status: ClusterProviderStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = CLUSTERPROVIDER_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'ClusterProvider | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = ClusterProviderSpec.from_input(obj.get(Y_SPEC, None))
            _status = ClusterProviderStatus.from_input(obj.get(Y_STATUS))
            return ClusterProvider(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class ClusterProviderList:
    def __init__(
        self,
        items: list[ClusterProvider],
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
    def from_input(obj) -> 'ClusterProviderList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return ClusterProviderList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
