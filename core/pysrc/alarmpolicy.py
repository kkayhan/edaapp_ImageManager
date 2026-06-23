#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *

ENUM_ACTIONACTION_SUPPRESS = 'Suppress'
ENUM_ACTIONACTION_ACKNOWLEDGE = 'Acknowledge'
ENUM_ACTIONACTION_CHANGESEVERITY = 'ChangeSeverity'

ENUM_ACTIONOVERRIDESEVERITY_WARNING = 'warning'
ENUM_ACTIONOVERRIDESEVERITY_MINOR = 'minor'
ENUM_ACTIONOVERRIDESEVERITY_MAJOR = 'major'
ENUM_ACTIONOVERRIDESEVERITY_CRITICAL = 'critical'
Y_SOURCEGROUP = 'sourceGroup'
Y_TYPE = 'type'
Y_GROUP = 'group'
Y_KIND = 'kind'
Y_NAMES = 'names'
Y_NODES = 'nodes'
Y_NAMESPACE = 'namespace'
Y_ALARMTYPE = 'alarmType'
Y_ALARMRESOURCE = 'alarmResource'
Y_TARGETSAFFECTED = 'targetsAffected'
Y_ACTION = 'action'
Y_OVERRIDESEVERITY = 'overrideSeverity'
Y_MATCH = 'match'
# Package objects (GVK Schemas)
ALARMPOLICY_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='AlarmPolicy')


class Action:
    def __init__(
        self,
        action: str,
        overrideSeverity: str | None = None,
    ):
        self.action = action
        self.overrideSeverity = overrideSeverity

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.action is not None:
            _rval[Y_ACTION] = self.action
        if self.overrideSeverity is not None:
            _rval[Y_OVERRIDESEVERITY] = self.overrideSeverity
        return _rval

    @staticmethod
    def from_input(obj) -> 'Action | None':
        if obj:
            _action = obj.get(Y_ACTION)
            _overrideSeverity = obj.get(Y_OVERRIDESEVERITY)
            return Action(
                action=_action,
                overrideSeverity=_overrideSeverity,
            )
        return None  # pragma: no cover


class AlarmResource:
    def __init__(
        self,
        group: str,
        kind: str,
        names: list[str] | None = None,
    ):
        self.group = group
        self.kind = kind
        self.names = names

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.group is not None:
            _rval[Y_GROUP] = self.group
        if self.kind is not None:
            _rval[Y_KIND] = self.kind
        if self.names is not None:
            _rval[Y_NAMES] = self.names
        return _rval

    @staticmethod
    def from_input(obj) -> 'AlarmResource | None':
        if obj:
            _group = obj.get(Y_GROUP)
            _kind = obj.get(Y_KIND)
            _names = obj.get(Y_NAMES)
            return AlarmResource(
                group=_group,
                kind=_kind,
                names=_names,
            )
        return None  # pragma: no cover


class AlarmType:
    def __init__(
        self,
        sourceGroup: str,
        type: str,
    ):
        self.sourceGroup = sourceGroup
        self.type = type

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.sourceGroup is not None:
            _rval[Y_SOURCEGROUP] = self.sourceGroup
        if self.type is not None:
            _rval[Y_TYPE] = self.type
        return _rval

    @staticmethod
    def from_input(obj) -> 'AlarmType | None':
        if obj:
            _sourceGroup = obj.get(Y_SOURCEGROUP)
            _type = obj.get(Y_TYPE)
            return AlarmType(
                sourceGroup=_sourceGroup,
                type=_type,
            )
        return None  # pragma: no cover


class TargetsAffected:
    def __init__(
        self,
        nodes: list[str],
    ):
        self.nodes = nodes

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.nodes is not None:
            _rval[Y_NODES] = self.nodes
        return _rval

    @staticmethod
    def from_input(obj) -> 'TargetsAffected | None':
        if obj:
            _nodes = obj.get(Y_NODES)
            return TargetsAffected(
                nodes=_nodes,
            )
        return None  # pragma: no cover


class MatchCriteria:
    def __init__(
        self,
        namespace: str | None = None,
        alarmType: AlarmType | None = None,
        alarmResource: AlarmResource | None = None,
        targetsAffected: TargetsAffected | None = None,
    ):
        self.namespace = namespace
        self.alarmType = alarmType
        self.alarmResource = alarmResource
        self.targetsAffected = targetsAffected

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.namespace is not None:
            _rval[Y_NAMESPACE] = self.namespace
        if self.alarmType is not None:
            _rval[Y_ALARMTYPE] = self.alarmType.to_input()
        if self.alarmResource is not None:
            _rval[Y_ALARMRESOURCE] = self.alarmResource.to_input()
        if self.targetsAffected is not None:
            _rval[Y_TARGETSAFFECTED] = self.targetsAffected.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'MatchCriteria | None':
        if obj:
            _namespace = obj.get(Y_NAMESPACE)
            _alarmType = AlarmType.from_input(obj.get(Y_ALARMTYPE))
            _alarmResource = AlarmResource.from_input(obj.get(Y_ALARMRESOURCE))
            _targetsAffected = TargetsAffected.from_input(obj.get(Y_TARGETSAFFECTED))
            return MatchCriteria(
                namespace=_namespace,
                alarmType=_alarmType,
                alarmResource=_alarmResource,
                targetsAffected=_targetsAffected,
            )
        return None  # pragma: no cover


class AlarmPolicySpec:
    def __init__(
        self,
        match: MatchCriteria,
        action: Action,
    ):
        self.match = match
        self.action = action

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.match is not None:
            _rval[Y_MATCH] = self.match.to_input()
        if self.action is not None:
            _rval[Y_ACTION] = self.action.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'AlarmPolicySpec | None':
        if obj:
            _match = MatchCriteria.from_input(obj.get(Y_MATCH))
            _action = Action.from_input(obj.get(Y_ACTION))
            return AlarmPolicySpec(
                match=_match,
                action=_action,
            )
        return None  # pragma: no cover


class AlarmPolicyStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'AlarmPolicyStatus | None':
        if obj:
            return AlarmPolicyStatus(
            )
        return None  # pragma: no cover


class AlarmPolicy:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: AlarmPolicySpec | None = None,
        status: AlarmPolicyStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = ALARMPOLICY_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'AlarmPolicy | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = AlarmPolicySpec.from_input(obj.get(Y_SPEC, None))
            _status = AlarmPolicyStatus.from_input(obj.get(Y_STATUS))
            return AlarmPolicy(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class AlarmPolicyList:
    def __init__(
        self,
        items: list[AlarmPolicy],
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
    def from_input(obj) -> 'AlarmPolicyList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return AlarmPolicyList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
