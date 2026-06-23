#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *

ENUM_DEVIATIONSPECOPERATION_CREATE = 'create'
ENUM_DEVIATIONSPECOPERATION_DELETE = 'delete'
Y_GROUPVERSION = 'groupVersion'
Y_KIND = 'kind'
Y_NODEENDPOINT = 'nodeEndpoint'
Y_ACCEPTED = 'accepted'
Y_PATH = 'path'
Y_INTENDEDVALUES = 'intendedValues'
Y_RUNNINGVALUES = 'runningValues'
Y_OPERATION = 'operation'
Y_ASSOCIATEDCRS = 'associatedCrs'
# Package objects (GVK Schemas)
DEVIATION_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='Deviation')


class AssociatedCr:
    def __init__(
        self,
        groupVersion: str,
        kind: str,
        name: str,
    ):
        self.groupVersion = groupVersion
        self.kind = kind
        self.name = name

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.groupVersion is not None:
            _rval[Y_GROUPVERSION] = self.groupVersion
        if self.kind is not None:
            _rval[Y_KIND] = self.kind
        if self.name is not None:
            _rval[Y_NAME] = self.name
        return _rval

    @staticmethod
    def from_input(obj) -> 'AssociatedCr | None':
        if obj:
            _groupVersion = obj.get(Y_GROUPVERSION)
            _kind = obj.get(Y_KIND)
            _name = obj.get(Y_NAME)
            return AssociatedCr(
                groupVersion=_groupVersion,
                kind=_kind,
                name=_name,
            )
        return None  # pragma: no cover


class DeviationSpec:
    def __init__(
        self,
        nodeEndpoint: str,
        path: str,
        operation: str,
        accepted: bool | None = None,
        intendedValues: str | None = None,
        runningValues: str | None = None,
        associatedCrs: list[AssociatedCr] | None = None,
    ):
        self.nodeEndpoint = nodeEndpoint
        self.path = path
        self.operation = operation
        self.accepted = accepted
        self.intendedValues = intendedValues
        self.runningValues = runningValues
        self.associatedCrs = associatedCrs

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.nodeEndpoint is not None:
            _rval[Y_NODEENDPOINT] = self.nodeEndpoint
        if self.path is not None:
            _rval[Y_PATH] = self.path
        if self.operation is not None:
            _rval[Y_OPERATION] = self.operation
        if self.accepted is not None:
            _rval[Y_ACCEPTED] = self.accepted
        if self.intendedValues is not None:
            _rval[Y_INTENDEDVALUES] = self.intendedValues
        if self.runningValues is not None:
            _rval[Y_RUNNINGVALUES] = self.runningValues
        if self.associatedCrs is not None:
            _rval[Y_ASSOCIATEDCRS] = [x.to_input() for x in self.associatedCrs]
        return _rval

    @staticmethod
    def from_input(obj) -> 'DeviationSpec | None':
        if obj:
            _nodeEndpoint = obj.get(Y_NODEENDPOINT)
            _path = obj.get(Y_PATH)
            _operation = obj.get(Y_OPERATION)
            _accepted = obj.get(Y_ACCEPTED)
            _intendedValues = obj.get(Y_INTENDEDVALUES)
            _runningValues = obj.get(Y_RUNNINGVALUES)
            _associatedCrs = []
            if obj.get(Y_ASSOCIATEDCRS) is not None:
                for x in obj.get(Y_ASSOCIATEDCRS):
                    _associatedCrs.append(AssociatedCr.from_input(x))
            return DeviationSpec(
                nodeEndpoint=_nodeEndpoint,
                path=_path,
                operation=_operation,
                accepted=_accepted,
                intendedValues=_intendedValues,
                runningValues=_runningValues,
                associatedCrs=_associatedCrs,
            )
        return None  # pragma: no cover


class DeviationStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'DeviationStatus | None':
        if obj:
            return DeviationStatus(
            )
        return None  # pragma: no cover


class Deviation:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: DeviationSpec | None = None,
        status: DeviationStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = DEVIATION_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'Deviation | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = DeviationSpec.from_input(obj.get(Y_SPEC, None))
            _status = DeviationStatus.from_input(obj.get(Y_STATUS))
            return Deviation(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class DeviationList:
    def __init__(
        self,
        items: list[Deviation],
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
    def from_input(obj) -> 'DeviationList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return DeviationList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
