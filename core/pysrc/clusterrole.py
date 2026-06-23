#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
from .role import RoleStatus

ENUM_ROLERESOURCERULEPERMISSIONS_NONE = 'none'
ENUM_ROLERESOURCERULEPERMISSIONS_READ = 'read'
ENUM_ROLERESOURCERULEPERMISSIONS_READPROPOSE = 'readPropose'
ENUM_ROLERESOURCERULEPERMISSIONS_READWRITE = 'readWrite'

ENUM_ROLEURLRULEPERMISSIONS_NONE = 'none'
ENUM_ROLEURLRULEPERMISSIONS_READ = 'read'
ENUM_ROLEURLRULEPERMISSIONS_READWRITE = 'readWrite'

ENUM_ROLETABLERULEPERMISSIONS_NONE = 'none'
ENUM_ROLETABLERULEPERMISSIONS_READ = 'read'
Y_APIGROUPS = 'apiGroups'
Y_RESOURCES = 'resources'
Y_PERMISSIONS = 'permissions'
Y_PATH = 'path'
Y_DESCRIPTION = 'description'
Y_RESOURCERULES = 'resourceRules'
Y_URLRULES = 'urlRules'
Y_TABLERULES = 'tableRules'
# Package objects (GVK Schemas)
CLUSTERROLE_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='ClusterRole')


class RoleResourceRule:
    def __init__(
        self,
        apiGroups: list[str],
        resources: list[str],
        permissions: str,
    ):
        self.apiGroups = apiGroups
        self.resources = resources
        self.permissions = permissions

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.apiGroups is not None:
            _rval[Y_APIGROUPS] = self.apiGroups
        if self.resources is not None:
            _rval[Y_RESOURCES] = self.resources
        if self.permissions is not None:
            _rval[Y_PERMISSIONS] = self.permissions
        return _rval

    @staticmethod
    def from_input(obj) -> 'RoleResourceRule | None':
        if obj:
            _apiGroups = obj.get(Y_APIGROUPS)
            _resources = obj.get(Y_RESOURCES)
            _permissions = obj.get(Y_PERMISSIONS)
            return RoleResourceRule(
                apiGroups=_apiGroups,
                resources=_resources,
                permissions=_permissions,
            )
        return None  # pragma: no cover


class RoleTableRule:
    def __init__(
        self,
        path: str,
        permissions: str,
    ):
        self.path = path
        self.permissions = permissions

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.path is not None:
            _rval[Y_PATH] = self.path
        if self.permissions is not None:
            _rval[Y_PERMISSIONS] = self.permissions
        return _rval

    @staticmethod
    def from_input(obj) -> 'RoleTableRule | None':
        if obj:
            _path = obj.get(Y_PATH)
            _permissions = obj.get(Y_PERMISSIONS)
            return RoleTableRule(
                path=_path,
                permissions=_permissions,
            )
        return None  # pragma: no cover


class RoleUrlRule:
    def __init__(
        self,
        path: str,
        permissions: str,
    ):
        self.path = path
        self.permissions = permissions

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.path is not None:
            _rval[Y_PATH] = self.path
        if self.permissions is not None:
            _rval[Y_PERMISSIONS] = self.permissions
        return _rval

    @staticmethod
    def from_input(obj) -> 'RoleUrlRule | None':
        if obj:
            _path = obj.get(Y_PATH)
            _permissions = obj.get(Y_PERMISSIONS)
            return RoleUrlRule(
                path=_path,
                permissions=_permissions,
            )
        return None  # pragma: no cover


class ClusterRoleSpec:
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
    def from_input(obj) -> 'ClusterRoleSpec | None':
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
            return ClusterRoleSpec(
                description=_description,
                resourceRules=_resourceRules,
                urlRules=_urlRules,
                tableRules=_tableRules,
            )
        return None  # pragma: no cover


class ClusterRole:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: ClusterRoleSpec | None = None,
        status: ClusterRoleStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = CLUSTERROLE_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'ClusterRole | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = ClusterRoleSpec.from_input(obj.get(Y_SPEC, None))
            _status = ClusterRoleStatus.from_input(obj.get(Y_STATUS))
            return ClusterRole(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class ClusterRoleList:
    def __init__(
        self,
        items: list[ClusterRole],
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
    def from_input(obj) -> 'ClusterRoleList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return ClusterRoleList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
