#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
Y_FROMNAMESPACE = 'fromNamespace'
Y_DESCRIPTION = 'description'
Y_BOOTSTRAP = 'bootstrap'
# Package objects (GVK Schemas)
NAMESPACE_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='Namespace')


class NamespaceBootstrap:
    def __init__(
        self,
        fromNamespace: str | None = None,
    ):
        self.fromNamespace = fromNamespace

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.fromNamespace is not None:
            _rval[Y_FROMNAMESPACE] = self.fromNamespace
        return _rval

    @staticmethod
    def from_input(obj) -> 'NamespaceBootstrap | None':
        if obj:
            _fromNamespace = obj.get(Y_FROMNAMESPACE)
            return NamespaceBootstrap(
                fromNamespace=_fromNamespace,
            )
        return None  # pragma: no cover


class NamespaceSpec:
    def __init__(
        self,
        description: str | None = None,
        bootstrap: NamespaceBootstrap | None = None,
    ):
        self.description = description
        self.bootstrap = bootstrap

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.description is not None:
            _rval[Y_DESCRIPTION] = self.description
        if self.bootstrap is not None:
            _rval[Y_BOOTSTRAP] = self.bootstrap.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'NamespaceSpec | None':
        if obj:
            _description = obj.get(Y_DESCRIPTION)
            _bootstrap = NamespaceBootstrap.from_input(obj.get(Y_BOOTSTRAP))
            return NamespaceSpec(
                description=_description,
                bootstrap=_bootstrap,
            )
        return None  # pragma: no cover


class NamespaceStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'NamespaceStatus | None':
        if obj:
            return NamespaceStatus(
            )
        return None  # pragma: no cover


class Namespace:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: NamespaceSpec | None = None,
        status: NamespaceStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = NAMESPACE_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'Namespace | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = NamespaceSpec.from_input(obj.get(Y_SPEC, None))
            _status = NamespaceStatus.from_input(obj.get(Y_STATUS))
            return Namespace(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class NamespaceList:
    def __init__(
        self,
        items: list[Namespace],
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
    def from_input(obj) -> 'NamespaceList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return NamespaceList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
