#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
from .allocation_common import PoolAllocationIndex, ReservationRangeIndex
Y_START = 'start'
Y_SIZE = 'size'
Y_ALLOCATIONS = 'allocations'
Y_RESERVATIONS = 'reservations'
Y_SEGMENTS = 'segments'
Y_PUBLISHALLOCATIONS = 'publishAllocations'
# Package objects (GVK Schemas)
INDEXALLOCATIONPOOL_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='IndexAllocationPool')


class IndexSegment:
    def __init__(
        self,
        start: int,
        size: int,
        allocations: list[PoolAllocationIndex] | None = None,
        reservations: list[ReservationRangeIndex] | None = None,
    ):
        self.start = start
        self.size = size
        self.allocations = allocations
        self.reservations = reservations

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.start is not None:
            _rval[Y_START] = self.start
        if self.size is not None:
            _rval[Y_SIZE] = self.size
        if self.allocations is not None:
            _rval[Y_ALLOCATIONS] = [x.to_input() for x in self.allocations]
        if self.reservations is not None:
            _rval[Y_RESERVATIONS] = [x.to_input() for x in self.reservations]
        return _rval

    @staticmethod
    def from_input(obj) -> 'IndexSegment | None':
        if obj:
            _start = obj.get(Y_START)
            _size = obj.get(Y_SIZE)
            _allocations = []
            if obj.get(Y_ALLOCATIONS) is not None:
                for x in obj.get(Y_ALLOCATIONS):
                    _allocations.append(PoolAllocationIndex.from_input(x))
            _reservations = []
            if obj.get(Y_RESERVATIONS) is not None:
                for x in obj.get(Y_RESERVATIONS):
                    _reservations.append(ReservationRangeIndex.from_input(x))
            return IndexSegment(
                start=_start,
                size=_size,
                allocations=_allocations,
                reservations=_reservations,
            )
        return None  # pragma: no cover


class IndexAllocationPoolSpec:
    def __init__(
        self,
        segments: list[IndexSegment],
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
    def from_input(obj) -> 'IndexAllocationPoolSpec | None':
        if obj:
            _segments = []
            if obj.get(Y_SEGMENTS) is not None:
                for x in obj.get(Y_SEGMENTS):
                    _segments.append(IndexSegment.from_input(x))
            _publishAllocations = obj.get(Y_PUBLISHALLOCATIONS)
            return IndexAllocationPoolSpec(
                segments=_segments,
                publishAllocations=_publishAllocations,
            )
        return None  # pragma: no cover


class IndexAllocationPoolStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'IndexAllocationPoolStatus | None':
        if obj:
            return IndexAllocationPoolStatus(
            )
        return None  # pragma: no cover


class IndexAllocationPool:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: IndexAllocationPoolSpec | None = None,
        status: IndexAllocationPoolStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = INDEXALLOCATIONPOOL_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'IndexAllocationPool | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = IndexAllocationPoolSpec.from_input(obj.get(Y_SPEC, None))
            _status = IndexAllocationPoolStatus.from_input(obj.get(Y_STATUS))
            return IndexAllocationPool(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class IndexAllocationPoolList:
    def __init__(
        self,
        items: list[IndexAllocationPool],
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
    def from_input(obj) -> 'IndexAllocationPoolList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return IndexAllocationPoolList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
