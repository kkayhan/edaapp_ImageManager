#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
from .engineconfig import EngineIntentGroupVersionKind
Y_DESCRIPTION = 'description'
Y_DRYRUN = 'dryRun'
Y_KEEPDETAILEDLOG = 'keepDetailedLog'
Y_ITEMS = 'items'
Y_REPLACE = 'replace'
Y_DELETE = 'delete'
Y_NAMESPACE = 'namespace'
Y_GVK = 'gvk'
Y_RESULT = 'result'
Y_ERRORS = 'errors'
Y_TRANSACTIONID = 'transactionId'
# Package objects (GVK Schemas)
TRANSACTION_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='Transaction')


class TransactionGvkName:
    def __init__(
        self,
        gvk: EngineIntentGroupVersionKind,
        name: str,
        namespace: str | None = None,
    ):
        self.gvk = gvk
        self.name = name
        self.namespace = namespace

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.gvk is not None:
            _rval[Y_GVK] = self.gvk.to_input()
        if self.name is not None:
            _rval[Y_NAME] = self.name
        if self.namespace is not None:
            _rval[Y_NAMESPACE] = self.namespace
        return _rval

    @staticmethod
    def from_input(obj) -> 'TransactionGvkName | None':
        if obj:
            _gvk = EngineIntentGroupVersionKind.from_input(obj.get(Y_GVK))
            _name = obj.get(Y_NAME)
            _namespace = obj.get(Y_NAMESPACE)
            return TransactionGvkName(
                gvk=_gvk,
                name=_name,
                namespace=_namespace,
            )
        return None  # pragma: no cover


class TransactionItem:
    def __init__(
        self,
        replace: object | None = None,
        delete: TransactionGvkName | None = None,
    ):
        self.replace = replace
        self.delete = delete

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.replace is not None:
            _rval[Y_REPLACE] = self.replace
        if self.delete is not None:
            _rval[Y_DELETE] = self.delete.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'TransactionItem | None':
        if obj:
            _replace = obj.get(Y_REPLACE)
            _delete = TransactionGvkName.from_input(obj.get(Y_DELETE))
            return TransactionItem(
                replace=_replace,
                delete=_delete,
            )
        return None  # pragma: no cover


class TransactionSpec:
    def __init__(
        self,
        items: list[TransactionItem],
        description: str | None = None,
        dryRun: bool | None = None,
        keepDetailedLog: bool | None = None,
    ):
        self.items = items
        self.description = description
        self.dryRun = dryRun
        self.keepDetailedLog = keepDetailedLog

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.items is not None:
            _rval[Y_ITEMS] = [x.to_input() for x in self.items]
        if self.description is not None:
            _rval[Y_DESCRIPTION] = self.description
        if self.dryRun is not None:
            _rval[Y_DRYRUN] = self.dryRun
        if self.keepDetailedLog is not None:
            _rval[Y_KEEPDETAILEDLOG] = self.keepDetailedLog
        return _rval

    @staticmethod
    def from_input(obj) -> 'TransactionSpec | None':
        if obj:
            _items = []
            if obj.get(Y_ITEMS) is not None:
                for x in obj.get(Y_ITEMS):
                    _items.append(TransactionItem.from_input(x))
            _description = obj.get(Y_DESCRIPTION)
            _dryRun = obj.get(Y_DRYRUN)
            _keepDetailedLog = obj.get(Y_KEEPDETAILEDLOG)
            return TransactionSpec(
                items=_items,
                description=_description,
                dryRun=_dryRun,
                keepDetailedLog=_keepDetailedLog,
            )
        return None  # pragma: no cover


class TransactionStatus:
    def __init__(
        self,
        result: str | None = None,
        errors: list[str] | None = None,
        transactionId: int | None = None,
    ):
        self.result = result
        self.errors = errors
        self.transactionId = transactionId

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.result is not None:
            _rval[Y_RESULT] = self.result
        if self.errors is not None:
            _rval[Y_ERRORS] = self.errors
        if self.transactionId is not None:
            _rval[Y_TRANSACTIONID] = self.transactionId
        return _rval

    @staticmethod
    def from_input(obj) -> 'TransactionStatus | None':
        if obj:
            _result = obj.get(Y_RESULT)
            _errors = obj.get(Y_ERRORS)
            _transactionId = obj.get(Y_TRANSACTIONID)
            return TransactionStatus(
                result=_result,
                errors=_errors,
                transactionId=_transactionId,
            )
        return None  # pragma: no cover


class Transaction:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: TransactionSpec | None = None,
        status: TransactionStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = TRANSACTION_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'Transaction | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = TransactionSpec.from_input(obj.get(Y_SPEC, None))
            _status = TransactionStatus.from_input(obj.get(Y_STATUS))
            return Transaction(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class TransactionList:
    def __init__(
        self,
        items: list[Transaction],
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
    def from_input(obj) -> 'TransactionList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return TransactionList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
