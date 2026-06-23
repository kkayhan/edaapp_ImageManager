#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *

ENUM_DEVIATIONNODEACTIONSPECACTION_SETACCEPT = 'setAccept'
ENUM_DEVIATIONNODEACTIONSPECACTION_CLEARACCEPT = 'clearAccept'
ENUM_DEVIATIONNODEACTIONSPECACTION_REJECT = 'reject'

ENUM_DEVIATIONACTIONSTATUSRESULT_OK = 'OK'
ENUM_DEVIATIONACTIONSTATUSRESULT_FAILED = 'Failed'
Y_PATH = 'path'
Y_ACTION = 'action'
Y_RECURSE = 'recurse'
Y_NODEENDPOINT = 'nodeEndpoint'
Y_ACTIONS = 'actions'
Y_RESULT = 'result'
Y_TRANSACTIONID = 'transactionId'
# Package objects (GVK Schemas)
DEVIATIONACTION_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='DeviationAction')


class DeviationNodeActionSpec:
    def __init__(
        self,
        path: str,
        action: str,
        recurse: bool | None = None,
    ):
        self.path = path
        self.action = action
        self.recurse = recurse

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.path is not None:
            _rval[Y_PATH] = self.path
        if self.action is not None:
            _rval[Y_ACTION] = self.action
        if self.recurse is not None:
            _rval[Y_RECURSE] = self.recurse
        return _rval

    @staticmethod
    def from_input(obj) -> 'DeviationNodeActionSpec | None':
        if obj:
            _path = obj.get(Y_PATH)
            _action = obj.get(Y_ACTION)
            _recurse = obj.get(Y_RECURSE)
            return DeviationNodeActionSpec(
                path=_path,
                action=_action,
                recurse=_recurse,
            )
        return None  # pragma: no cover


class DeviationActionSpec:
    def __init__(
        self,
        nodeEndpoint: str,
        actions: list[DeviationNodeActionSpec],
    ):
        self.nodeEndpoint = nodeEndpoint
        self.actions = actions

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.nodeEndpoint is not None:
            _rval[Y_NODEENDPOINT] = self.nodeEndpoint
        if self.actions is not None:
            _rval[Y_ACTIONS] = [x.to_input() for x in self.actions]
        return _rval

    @staticmethod
    def from_input(obj) -> 'DeviationActionSpec | None':
        if obj:
            _nodeEndpoint = obj.get(Y_NODEENDPOINT)
            _actions = []
            if obj.get(Y_ACTIONS) is not None:
                for x in obj.get(Y_ACTIONS):
                    _actions.append(DeviationNodeActionSpec.from_input(x))
            return DeviationActionSpec(
                nodeEndpoint=_nodeEndpoint,
                actions=_actions,
            )
        return None  # pragma: no cover


class DeviationActionStatus:
    def __init__(
        self,
        result: str | None = None,
        transactionId: int | None = None,
    ):
        self.result = result
        self.transactionId = transactionId

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.result is not None:
            _rval[Y_RESULT] = self.result
        if self.transactionId is not None:
            _rval[Y_TRANSACTIONID] = self.transactionId
        return _rval

    @staticmethod
    def from_input(obj) -> 'DeviationActionStatus | None':
        if obj:
            _result = obj.get(Y_RESULT)
            _transactionId = obj.get(Y_TRANSACTIONID)
            return DeviationActionStatus(
                result=_result,
                transactionId=_transactionId,
            )
        return None  # pragma: no cover


class DeviationAction:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: DeviationActionSpec | None = None,
        status: DeviationActionStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = DEVIATIONACTION_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'DeviationAction | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = DeviationActionSpec.from_input(obj.get(Y_SPEC, None))
            _status = DeviationActionStatus.from_input(obj.get(Y_STATUS))
            return DeviationAction(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class DeviationActionList:
    def __init__(
        self,
        items: list[DeviationAction],
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
    def from_input(obj) -> 'DeviationActionList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return DeviationActionList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
