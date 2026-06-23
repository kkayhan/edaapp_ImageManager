#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
from .allocation_common import PoolAllocationString, ReservationRangeString
Y_SUBNET = 'subnet'
Y_SUBNETLENGTH = 'subnetLength'
Y_ALLOCATIONS = 'allocations'
Y_RESERVATIONS = 'reservations'
Y_SEGMENTS = 'segments'
Y_PUBLISHALLOCATIONS = 'publishAllocations'
# Package objects (GVK Schemas)
SUBNETALLOCATIONPOOL_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='SubnetAllocationPool')


class SubnetSegment:
    def __init__(
        self,
        subnet: str,
        subnetLength: int,
        allocations: list[PoolAllocationString] | None = None,
        reservations: list[ReservationRangeString] | None = None,
    ):
        self.subnet = subnet
        self.subnetLength = subnetLength
        self.allocations = allocations
        self.reservations = reservations

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.subnet is not None:
            _rval[Y_SUBNET] = self.subnet
        if self.subnetLength is not None:
            _rval[Y_SUBNETLENGTH] = self.subnetLength
        if self.allocations is not None:
            _rval[Y_ALLOCATIONS] = [x.to_input() for x in self.allocations]
        if self.reservations is not None:
            _rval[Y_RESERVATIONS] = [x.to_input() for x in self.reservations]
        return _rval

    @staticmethod
    def from_input(obj) -> 'SubnetSegment | None':
        if obj:
            _subnet = obj.get(Y_SUBNET)
            _subnetLength = obj.get(Y_SUBNETLENGTH)
            _allocations = []
            if obj.get(Y_ALLOCATIONS) is not None:
                for x in obj.get(Y_ALLOCATIONS):
                    _allocations.append(PoolAllocationString.from_input(x))
            _reservations = []
            if obj.get(Y_RESERVATIONS) is not None:
                for x in obj.get(Y_RESERVATIONS):
                    _reservations.append(ReservationRangeString.from_input(x))
            return SubnetSegment(
                subnet=_subnet,
                subnetLength=_subnetLength,
                allocations=_allocations,
                reservations=_reservations,
            )
        return None  # pragma: no cover


class SubnetAllocationPoolSpec:
    def __init__(
        self,
        segments: list[SubnetSegment] | None = None,
        publishAllocations: bool | None = None,
    ):
        self.segments = segments
        self.publishAllocations = publishAllocations

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.segments is not None:
            _rval[Y_SEGMENTS] = [x.to_input() for x in self.segments]
        if self.publishAllocations is not None:
            _rval[Y_PUBLISHALLOCATIONS] = self.publishAllocations
        return _rval

    @staticmethod
    def from_input(obj) -> 'SubnetAllocationPoolSpec | None':
        if obj:
            _segments = []
            if obj.get(Y_SEGMENTS) is not None:
                for x in obj.get(Y_SEGMENTS):
                    _segments.append(SubnetSegment.from_input(x))
            _publishAllocations = obj.get(Y_PUBLISHALLOCATIONS)
            return SubnetAllocationPoolSpec(
                segments=_segments,
                publishAllocations=_publishAllocations,
            )
        return None  # pragma: no cover


class SubnetAllocationPoolStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'SubnetAllocationPoolStatus | None':
        if obj:
            return SubnetAllocationPoolStatus(
            )
        return None  # pragma: no cover


class SubnetAllocationPool:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: SubnetAllocationPoolSpec | None = None,
        status: SubnetAllocationPoolStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = SUBNETALLOCATIONPOOL_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'SubnetAllocationPool | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = SubnetAllocationPoolSpec.from_input(obj.get(Y_SPEC, None))
            _status = SubnetAllocationPoolStatus.from_input(obj.get(Y_STATUS))
            return SubnetAllocationPool(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class SubnetAllocationPoolList:
    def __init__(
        self,
        items: list[SubnetAllocationPool],
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
    def from_input(obj) -> 'SubnetAllocationPoolList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return SubnetAllocationPoolList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
