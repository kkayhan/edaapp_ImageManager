#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
Y_POOLINSTANCE = 'poolInstance'
Y_VALUE = 'value'
Y_START = 'start'
Y_END = 'end'


class PoolAllocationIndex:
    def __init__(
        self,
        name: str,
        value: int,
        poolInstance: str | None = None,
    ):
        self.name = name
        self.value = value
        self.poolInstance = poolInstance

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.name is not None:
            _rval[Y_NAME] = self.name
        if self.value is not None:
            _rval[Y_VALUE] = self.value
        if self.poolInstance is not None:
            _rval[Y_POOLINSTANCE] = self.poolInstance
        return _rval

    @staticmethod
    def from_input(obj) -> 'PoolAllocationIndex | None':
        if obj:
            _name = obj.get(Y_NAME)
            _value = obj.get(Y_VALUE)
            _poolInstance = obj.get(Y_POOLINSTANCE)
            return PoolAllocationIndex(
                name=_name,
                value=_value,
                poolInstance=_poolInstance,
            )
        return None  # pragma: no cover


class PoolAllocationString:
    def __init__(
        self,
        name: str,
        value: str,
        poolInstance: str | None = None,
    ):
        self.name = name
        self.value = value
        self.poolInstance = poolInstance

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.name is not None:
            _rval[Y_NAME] = self.name
        if self.value is not None:
            _rval[Y_VALUE] = self.value
        if self.poolInstance is not None:
            _rval[Y_POOLINSTANCE] = self.poolInstance
        return _rval

    @staticmethod
    def from_input(obj) -> 'PoolAllocationString | None':
        if obj:
            _name = obj.get(Y_NAME)
            _value = obj.get(Y_VALUE)
            _poolInstance = obj.get(Y_POOLINSTANCE)
            return PoolAllocationString(
                name=_name,
                value=_value,
                poolInstance=_poolInstance,
            )
        return None  # pragma: no cover


class ReservationRangeIndex:
    def __init__(
        self,
        start: int,
        end: int,
    ):
        self.start = start
        self.end = end

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.start is not None:
            _rval[Y_START] = self.start
        if self.end is not None:
            _rval[Y_END] = self.end
        return _rval

    @staticmethod
    def from_input(obj) -> 'ReservationRangeIndex | None':
        if obj:
            _start = obj.get(Y_START)
            _end = obj.get(Y_END)
            return ReservationRangeIndex(
                start=_start,
                end=_end,
            )
        return None  # pragma: no cover


class ReservationRangeString:
    def __init__(
        self,
        start: str,
        end: str,
    ):
        self.start = start
        self.end = end

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.start is not None:
            _rval[Y_START] = self.start
        if self.end is not None:
            _rval[Y_END] = self.end
        return _rval

    @staticmethod
    def from_input(obj) -> 'ReservationRangeString | None':
        if obj:
            _start = obj.get(Y_START)
            _end = obj.get(Y_END)
            return ReservationRangeString(
                start=_start,
                end=_end,
            )
        return None  # pragma: no cover
