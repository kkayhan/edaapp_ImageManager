#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
Y_ID = 'id'
Y_PROMPT = 'prompt'
# Package objects (GVK Schemas)
WAITFORINPUT_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='WaitForInput')


class WaitForInputSpec:
    def __init__(
        self,
        id: int | None = None,
        prompt: str | None = None,
    ):
        self.id = id
        self.prompt = prompt

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.id is not None:
            _rval[Y_ID] = self.id
        if self.prompt is not None:
            _rval[Y_PROMPT] = self.prompt
        return _rval

    @staticmethod
    def from_input(obj) -> 'WaitForInputSpec | None':
        if obj:
            _id = obj.get(Y_ID)
            _prompt = obj.get(Y_PROMPT)
            return WaitForInputSpec(
                id=_id,
                prompt=_prompt,
            )
        return None  # pragma: no cover


class WaitForInputStatus:
    def __init__(
        self,
        prompt: bool | None = None,
    ):
        self.prompt = prompt

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.prompt is not None:
            _rval[Y_PROMPT] = self.prompt
        return _rval

    @staticmethod
    def from_input(obj) -> 'WaitForInputStatus | None':
        if obj:
            _prompt = obj.get(Y_PROMPT)
            return WaitForInputStatus(
                prompt=_prompt,
            )
        return None  # pragma: no cover


class WaitForInput:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: WaitForInputSpec | None = None,
        status: WaitForInputStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = WAITFORINPUT_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'WaitForInput | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = WaitForInputSpec.from_input(obj.get(Y_SPEC, None))
            _status = WaitForInputStatus.from_input(obj.get(Y_STATUS))
            return WaitForInput(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class WaitForInputList:
    def __init__(
        self,
        items: list[WaitForInput],
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
    def from_input(obj) -> 'WaitForInputList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return WaitForInputList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
