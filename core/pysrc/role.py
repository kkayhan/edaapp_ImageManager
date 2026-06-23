#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
from .cluster_role import RoleResourceRule, RoleTableRule, RoleUrlRule
Y_DESCRIPTION = 'description'
Y_RESOURCERULES = 'resourceRules'
Y_URLRULES = 'urlRules'
Y_TABLERULES = 'tableRules'
# Package objects (GVK Schemas)
ROLE_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='Role')


class RoleSpec:
    def __init__(
        self,
        description: str | None = None,
        resourceRules: list[RoleResourceRule] | None = None,
        urlRules: list[RoleUrlRule] | None = None,
        tableRules: list[RoleTableRule] | None = None,
    ):
        self.description = description
        self.resourceRules = resourceRules
        self.urlRules = urlRules
        self.tableRules = tableRules

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.description is not None:
            _rval[Y_DESCRIPTION] = self.description
        if self.resourceRules is not None:
            _rval[Y_RESOURCERULES] = [x.to_input() for x in self.resourceRules]
        if self.urlRules is not None:
            _rval[Y_URLRULES] = [x.to_input() for x in self.urlRules]
        if self.tableRules is not None:
            _rval[Y_TABLERULES] = [x.to_input() for x in self.tableRules]
        return _rval

    @staticmethod
    def from_input(obj) -> 'RoleSpec | None':
        if obj:
            _description = obj.get(Y_DESCRIPTION)
            _resourceRules = []
            if obj.get(Y_RESOURCERULES) is not None:
                for x in obj.get(Y_RESOURCERULES):
                    _resourceRules.append(RoleResourceRule.from_input(x))
            _urlRules = []
            if obj.get(Y_URLRULES) is not None:
                for x in obj.get(Y_URLRULES):
                    _urlRules.append(RoleUrlRule.from_input(x))
            _tableRules = []
            if obj.get(Y_TABLERULES) is not None:
                for x in obj.get(Y_TABLERULES):
                    _tableRules.append(RoleTableRule.from_input(x))
            return RoleSpec(
                description=_description,
                resourceRules=_resourceRules,
                urlRules=_urlRules,
                tableRules=_tableRules,
            )
        return None  # pragma: no cover


class RoleStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'RoleStatus | None':
        if obj:
            return RoleStatus(
            )
        return None  # pragma: no cover


class Role:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: RoleSpec | None = None,
        status: RoleStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = ROLE_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'Role | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = RoleSpec.from_input(obj.get(Y_SPEC, None))
            _status = RoleStatus.from_input(obj.get(Y_STATUS))
            return Role(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class RoleList:
    def __init__(
        self,
        items: list[Role],
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
    def from_input(obj) -> 'RoleList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return RoleList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
