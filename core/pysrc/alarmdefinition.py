#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *

ENUM_ALARMDEFINITIONSPECSEVERITY_WARNING = 'warning'
ENUM_ALARMDEFINITIONSPECSEVERITY_MINOR = 'minor'
ENUM_ALARMDEFINITIONSPECSEVERITY_MAJOR = 'major'
ENUM_ALARMDEFINITIONSPECSEVERITY_CRITICAL = 'critical'
Y_SOURCEGROUP = 'sourceGroup'
Y_TYPE = 'type'
Y_DESCRIPTION = 'description'
Y_SEVERITY = 'severity'
Y_KIND = 'kind'
Y_GROUP = 'group'
Y_CLUSTERSPECIFIC = 'clusterSpecific'
# Package objects (GVK Schemas)
ALARMDEFINITION_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='AlarmDefinition')


class AlarmDefinitionSpec:
    def __init__(
        self,
        sourceGroup: str,
        type: str,
        description: str,
        severity: str | None = None,
        kind: str | None = None,
        group: str | None = None,
        clusterSpecific: bool | None = None,
    ):
        self.sourceGroup = sourceGroup
        self.type = type
        self.description = description
        self.severity = severity
        self.kind = kind
        self.group = group
        self.clusterSpecific = clusterSpecific

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.sourceGroup is not None:
            _rval[Y_SOURCEGROUP] = self.sourceGroup
        if self.type is not None:
            _rval[Y_TYPE] = self.type
        if self.description is not None:
            _rval[Y_DESCRIPTION] = self.description
        if self.severity is not None:
            _rval[Y_SEVERITY] = self.severity
        if self.kind is not None:
            _rval[Y_KIND] = self.kind
        if self.group is not None:
            _rval[Y_GROUP] = self.group
        if self.clusterSpecific is not None:
            _rval[Y_CLUSTERSPECIFIC] = self.clusterSpecific
        return _rval

    @staticmethod
    def from_input(obj) -> 'AlarmDefinitionSpec | None':
        if obj:
            _sourceGroup = obj.get(Y_SOURCEGROUP)
            _type = obj.get(Y_TYPE)
            _description = obj.get(Y_DESCRIPTION)
            _severity = obj.get(Y_SEVERITY)
            _kind = obj.get(Y_KIND)
            _group = obj.get(Y_GROUP)
            _clusterSpecific = obj.get(Y_CLUSTERSPECIFIC, False)
            return AlarmDefinitionSpec(
                sourceGroup=_sourceGroup,
                type=_type,
                description=_description,
                severity=_severity,
                kind=_kind,
                group=_group,
                clusterSpecific=_clusterSpecific,
            )
        return None  # pragma: no cover


class AlarmDefinitionStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'AlarmDefinitionStatus | None':
        if obj:
            return AlarmDefinitionStatus(
            )
        return None  # pragma: no cover


class AlarmDefinition:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: AlarmDefinitionSpec | None = None,
        status: AlarmDefinitionStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = ALARMDEFINITION_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'AlarmDefinition | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = AlarmDefinitionSpec.from_input(obj.get(Y_SPEC, None))
            _status = AlarmDefinitionStatus.from_input(obj.get(Y_STATUS))
            return AlarmDefinition(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class AlarmDefinitionList:
    def __init__(
        self,
        items: list[AlarmDefinition],
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
    def from_input(obj) -> 'AlarmDefinitionList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return AlarmDefinitionList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
