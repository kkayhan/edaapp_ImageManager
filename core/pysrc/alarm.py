#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *

ENUM_ALARMSPECSEVERITY_WARNING = 'warning'
ENUM_ALARMSPECSEVERITY_MINOR = 'minor'
ENUM_ALARMSPECSEVERITY_MAJOR = 'major'
ENUM_ALARMSPECSEVERITY_CRITICAL = 'critical'
ENUM_ALARMSPECSEVERITY_ = ''
Y_TYPE = 'type'
Y_SEVERITY = 'severity'
Y_RESOURCE = 'resource'
Y_KIND = 'kind'
Y_GROUP = 'group'
Y_SOURCERESOURCE = 'sourceResource'
Y_SOURCEKIND = 'sourceKind'
Y_SOURCEGROUP = 'sourceGroup'
Y_DESCRIPTION = 'description'
Y_PROBABLECAUSE = 'probableCause'
Y_REMEDIALACTION = 'remedialAction'
Y_ADDITIONALTEXT = 'additionalText'
Y_JSPATH = 'jsPath'
Y_PARENTALARM = 'parentAlarm'
Y_CLUSTERSPECIFIC = 'clusterSpecific'
Y_TARGETSAFFECTED = 'targetsAffected'
# Package objects (GVK Schemas)
ALARM_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='Alarm')


class AlarmDataTargetsAffected:
    def __init__(
        self,
        name: str | None = None,
    ):
        self.name = name

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.name is not None:
            _rval[Y_NAME] = self.name
        return _rval

    @staticmethod
    def from_input(obj) -> 'AlarmDataTargetsAffected | None':
        if obj:
            _name = obj.get(Y_NAME)
            return AlarmDataTargetsAffected(
                name=_name,
            )
        return None  # pragma: no cover


class AlarmSpec:
    def __init__(
        self,
        name: str,
        type: str,
        severity: str,
        resource: str,
        kind: str,
        group: str,
        sourceResource: str,
        sourceKind: str,
        sourceGroup: str,
        description: str,
        probableCause: str | None = None,
        remedialAction: str | None = None,
        additionalText: str | None = None,
        jsPath: list[str] | None = None,
        parentAlarm: list[str] | None = None,
        clusterSpecific: bool | None = None,
        targetsAffected: list[AlarmDataTargetsAffected] | None = None,
    ):
        self.name = name
        self.type = type
        self.severity = severity
        self.resource = resource
        self.kind = kind
        self.group = group
        self.sourceResource = sourceResource
        self.sourceKind = sourceKind
        self.sourceGroup = sourceGroup
        self.description = description
        self.probableCause = probableCause
        self.remedialAction = remedialAction
        self.additionalText = additionalText
        self.jsPath = jsPath
        self.parentAlarm = parentAlarm
        self.clusterSpecific = clusterSpecific
        self.targetsAffected = targetsAffected

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.name is not None:
            _rval[Y_NAME] = self.name
        if self.type is not None:
            _rval[Y_TYPE] = self.type
        if self.severity is not None:
            _rval[Y_SEVERITY] = self.severity
        if self.resource is not None:
            _rval[Y_RESOURCE] = self.resource
        if self.kind is not None:
            _rval[Y_KIND] = self.kind
        if self.group is not None:
            _rval[Y_GROUP] = self.group
        if self.sourceResource is not None:
            _rval[Y_SOURCERESOURCE] = self.sourceResource
        if self.sourceKind is not None:
            _rval[Y_SOURCEKIND] = self.sourceKind
        if self.sourceGroup is not None:
            _rval[Y_SOURCEGROUP] = self.sourceGroup
        if self.description is not None:
            _rval[Y_DESCRIPTION] = self.description
        if self.probableCause is not None:
            _rval[Y_PROBABLECAUSE] = self.probableCause
        if self.remedialAction is not None:
            _rval[Y_REMEDIALACTION] = self.remedialAction
        if self.additionalText is not None:
            _rval[Y_ADDITIONALTEXT] = self.additionalText
        if self.jsPath is not None:
            _rval[Y_JSPATH] = self.jsPath
        if self.parentAlarm is not None:
            _rval[Y_PARENTALARM] = self.parentAlarm
        if self.clusterSpecific is not None:
            _rval[Y_CLUSTERSPECIFIC] = self.clusterSpecific
        if self.targetsAffected is not None:
            _rval[Y_TARGETSAFFECTED] = [x.to_input() for x in self.targetsAffected]
        return _rval

    @staticmethod
    def from_input(obj) -> 'AlarmSpec | None':
        if obj:
            _name = obj.get(Y_NAME)
            _type = obj.get(Y_TYPE)
            _severity = obj.get(Y_SEVERITY)
            _resource = obj.get(Y_RESOURCE)
            _kind = obj.get(Y_KIND)
            _group = obj.get(Y_GROUP)
            _sourceResource = obj.get(Y_SOURCERESOURCE)
            _sourceKind = obj.get(Y_SOURCEKIND)
            _sourceGroup = obj.get(Y_SOURCEGROUP)
            _description = obj.get(Y_DESCRIPTION)
            _probableCause = obj.get(Y_PROBABLECAUSE)
            _remedialAction = obj.get(Y_REMEDIALACTION)
            _additionalText = obj.get(Y_ADDITIONALTEXT)
            _jsPath = obj.get(Y_JSPATH)
            _parentAlarm = obj.get(Y_PARENTALARM)
            _clusterSpecific = obj.get(Y_CLUSTERSPECIFIC)
            _targetsAffected = []
            if obj.get(Y_TARGETSAFFECTED) is not None:
                for x in obj.get(Y_TARGETSAFFECTED):
                    _targetsAffected.append(AlarmDataTargetsAffected.from_input(x))
            return AlarmSpec(
                name=_name,
                type=_type,
                severity=_severity,
                resource=_resource,
                kind=_kind,
                group=_group,
                sourceResource=_sourceResource,
                sourceKind=_sourceKind,
                sourceGroup=_sourceGroup,
                description=_description,
                probableCause=_probableCause,
                remedialAction=_remedialAction,
                additionalText=_additionalText,
                jsPath=_jsPath,
                parentAlarm=_parentAlarm,
                clusterSpecific=_clusterSpecific,
                targetsAffected=_targetsAffected,
            )
        return None  # pragma: no cover


class AlarmStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'AlarmStatus | None':
        if obj:
            return AlarmStatus(
            )
        return None  # pragma: no cover


class Alarm:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: AlarmSpec | None = None,
        status: AlarmStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = ALARM_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'Alarm | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = AlarmSpec.from_input(obj.get(Y_SPEC, None))
            _status = AlarmStatus.from_input(obj.get(Y_STATUS))
            return Alarm(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class AlarmList:
    def __init__(
        self,
        items: list[Alarm],
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
    def from_input(obj) -> 'AlarmList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return AlarmList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
