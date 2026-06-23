#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
Y_TYPE = 'type'
Y_INPUT = 'input'
Y_OUTPUT = 'output'
# Package objects (GVK Schemas)
WORKFLOW_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='Workflow')


class WorkflowSpec:
    def __init__(
        self,
        type: str,
        input: object | None = None,
    ):
        self.type = type
        self.input = input

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.type is not None:
            _rval[Y_TYPE] = self.type
        if self.input is not None:
            _rval[Y_INPUT] = self.input
        return _rval

    @staticmethod
    def from_input(obj) -> 'WorkflowSpec | None':
        if obj:
            _type = obj.get(Y_TYPE)
            _input = obj.get(Y_INPUT)
            return WorkflowSpec(
                type=_type,
                input=_input,
            )
        return None  # pragma: no cover


class WorkflowStatus:
    def __init__(
        self,
        output: object | None = None,
    ):
        self.output = output

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.output is not None:
            _rval[Y_OUTPUT] = self.output
        return _rval

    @staticmethod
    def from_input(obj) -> 'WorkflowStatus | None':
        if obj:
            _output = obj.get(Y_OUTPUT)
            return WorkflowStatus(
                output=_output,
            )
        return None  # pragma: no cover


class Workflow:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: WorkflowSpec | None = None,
        status: WorkflowStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = WORKFLOW_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'Workflow | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = WorkflowSpec.from_input(obj.get(Y_SPEC, None))
            _status = WorkflowStatus.from_input(obj.get(Y_STATUS))
            return Workflow(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class WorkflowList:
    def __init__(
        self,
        items: list[Workflow],
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
    def from_input(obj) -> 'WorkflowList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return WorkflowList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
