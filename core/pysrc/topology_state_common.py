#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
Y_ENABLED = 'enabled'
Y_GROUP = 'group'
Y_VERSION = 'version'
Y_TOPOLOGY = 'topology'
Y_UINAME = 'uiName'
Y_UIDESCRIPTION = 'uiDescription'
Y_UINAMEKEY = 'uiNameKey'
Y_UIDESCRIPTIONKEY = 'uiDescriptionKey'
Y_KEY = 'key'
Y_TIER = 'tier'
Y_NODESELECTOR = 'nodeSelector'
Y_GROUPUINAME = 'groupUIName'
Y_TIERSELECTORS = 'tierSelectors'
Y_GROUPSELECTORS = 'groupSelectors'
Y_OVERLAYS = 'overlays'


class TopologyOverlayTopologyRef:
    def __init__(
        self,
        group: str,
        version: str,
        name: str,
    ):
        self.group = group
        self.version = version
        self.name = name

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.group is not None:
            _rval[Y_GROUP] = self.group
        if self.version is not None:
            _rval[Y_VERSION] = self.version
        if self.name is not None:
            _rval[Y_NAME] = self.name
        return _rval

    @staticmethod
    def from_input(obj) -> 'TopologyOverlayTopologyRef | None':
        if obj:
            _group = obj.get(Y_GROUP)
            _version = obj.get(Y_VERSION)
            _name = obj.get(Y_NAME)
            return TopologyOverlayTopologyRef(
                group=_group,
                version=_version,
                name=_name,
            )
        return None  # pragma: no cover


class TopologyOverlayBase:
    def __init__(
        self,
        enabled: bool,
        topology: TopologyOverlayTopologyRef,
        uiName: str | None = None,
        uiDescription: str | None = None,
        uiNameKey: str | None = None,
        uiDescriptionKey: str | None = None,
    ):
        self.enabled = enabled
        self.topology = topology
        self.uiName = uiName
        self.uiDescription = uiDescription
        self.uiNameKey = uiNameKey
        self.uiDescriptionKey = uiDescriptionKey

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.enabled is not None:
            _rval[Y_ENABLED] = self.enabled
        if self.topology is not None:
            _rval[Y_TOPOLOGY] = self.topology.to_input()
        if self.uiName is not None:
            _rval[Y_UINAME] = self.uiName
        if self.uiDescription is not None:
            _rval[Y_UIDESCRIPTION] = self.uiDescription
        if self.uiNameKey is not None:
            _rval[Y_UINAMEKEY] = self.uiNameKey
        if self.uiDescriptionKey is not None:
            _rval[Y_UIDESCRIPTIONKEY] = self.uiDescriptionKey
        return _rval

    @staticmethod
    def from_input(obj) -> 'TopologyOverlayBase | None':
        if obj:
            _enabled = obj.get(Y_ENABLED)
            _topology = TopologyOverlayTopologyRef.from_input(obj.get(Y_TOPOLOGY))
            _uiName = obj.get(Y_UINAME)
            _uiDescription = obj.get(Y_UIDESCRIPTION)
            _uiNameKey = obj.get(Y_UINAMEKEY)
            _uiDescriptionKey = obj.get(Y_UIDESCRIPTIONKEY)
            return TopologyOverlayBase(
                enabled=_enabled,
                topology=_topology,
                uiName=_uiName,
                uiDescription=_uiDescription,
                uiNameKey=_uiNameKey,
                uiDescriptionKey=_uiDescriptionKey,
            )
        return None  # pragma: no cover


class TopologyOverlayCommon:
    def __init__(
        self,
        enabled: bool,
    ):
        self.enabled = enabled

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.enabled is not None:
            _rval[Y_ENABLED] = self.enabled
        return _rval

    @staticmethod
    def from_input(obj) -> 'TopologyOverlayCommon | None':
        if obj:
            _enabled = obj.get(Y_ENABLED)
            return TopologyOverlayCommon(
                enabled=_enabled,
            )
        return None  # pragma: no cover


class TopologyOverlayWithKey:
    def __init__(
        self,
        enabled: bool,
        key: str,
    ):
        self.enabled = enabled
        self.key = key

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.enabled is not None:
            _rval[Y_ENABLED] = self.enabled
        if self.key is not None:
            _rval[Y_KEY] = self.key
        return _rval

    @staticmethod
    def from_input(obj) -> 'TopologyOverlayWithKey | None':
        if obj:
            _enabled = obj.get(Y_ENABLED)
            _key = obj.get(Y_KEY)
            return TopologyOverlayWithKey(
                enabled=_enabled,
                key=_key,
            )
        return None  # pragma: no cover


class TopologyStateBase:
    def __init__(
        self,
        enabled: bool,
        overlays: list[TopologyOverlayWithKey],
        uiName: str | None = None,
        uiDescription: str | None = None,
        uiNameKey: str | None = None,
        uiDescriptionKey: str | None = None,
    ):
        self.enabled = enabled
        self.overlays = overlays
        self.uiName = uiName
        self.uiDescription = uiDescription
        self.uiNameKey = uiNameKey
        self.uiDescriptionKey = uiDescriptionKey

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.enabled is not None:
            _rval[Y_ENABLED] = self.enabled
        if self.overlays is not None:
            _rval[Y_OVERLAYS] = [x.to_input() for x in self.overlays]
        if self.uiName is not None:
            _rval[Y_UINAME] = self.uiName
        if self.uiDescription is not None:
            _rval[Y_UIDESCRIPTION] = self.uiDescription
        if self.uiNameKey is not None:
            _rval[Y_UINAMEKEY] = self.uiNameKey
        if self.uiDescriptionKey is not None:
            _rval[Y_UIDESCRIPTIONKEY] = self.uiDescriptionKey
        return _rval

    @staticmethod
    def from_input(obj) -> 'TopologyStateBase | None':
        if obj:
            _enabled = obj.get(Y_ENABLED)
            _overlays = []
            if obj.get(Y_OVERLAYS) is not None:
                for x in obj.get(Y_OVERLAYS):
                    _overlays.append(TopologyOverlayWithKey.from_input(x))
            _uiName = obj.get(Y_UINAME)
            _uiDescription = obj.get(Y_UIDESCRIPTION)
            _uiNameKey = obj.get(Y_UINAMEKEY)
            _uiDescriptionKey = obj.get(Y_UIDESCRIPTIONKEY)
            return TopologyStateBase(
                enabled=_enabled,
                overlays=_overlays,
                uiName=_uiName,
                uiDescription=_uiDescription,
                uiNameKey=_uiNameKey,
                uiDescriptionKey=_uiDescriptionKey,
            )
        return None  # pragma: no cover


class TopologyStateGroupSelector:
    def __init__(
        self,
        group: str,
        groupUIName: str,
        nodeSelector: list[str] | None = None,
    ):
        self.group = group
        self.groupUIName = groupUIName
        self.nodeSelector = nodeSelector

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.group is not None:
            _rval[Y_GROUP] = self.group
        if self.groupUIName is not None:
            _rval[Y_GROUPUINAME] = self.groupUIName
        if self.nodeSelector is not None:
            _rval[Y_NODESELECTOR] = self.nodeSelector
        return _rval

    @staticmethod
    def from_input(obj) -> 'TopologyStateGroupSelector | None':
        if obj:
            _group = obj.get(Y_GROUP)
            _groupUIName = obj.get(Y_GROUPUINAME)
            _nodeSelector = obj.get(Y_NODESELECTOR)
            return TopologyStateGroupSelector(
                group=_group,
                groupUIName=_groupUIName,
                nodeSelector=_nodeSelector,
            )
        return None  # pragma: no cover


class TopologyStateTierSelector:
    def __init__(
        self,
        tier: int,
        nodeSelector: list[str] | None = None,
    ):
        self.tier = tier
        self.nodeSelector = nodeSelector

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.tier is not None:
            _rval[Y_TIER] = self.tier
        if self.nodeSelector is not None:
            _rval[Y_NODESELECTOR] = self.nodeSelector
        return _rval

    @staticmethod
    def from_input(obj) -> 'TopologyStateTierSelector | None':
        if obj:
            _tier = obj.get(Y_TIER)
            _nodeSelector = obj.get(Y_NODESELECTOR)
            return TopologyStateTierSelector(
                tier=_tier,
                nodeSelector=_nodeSelector,
            )
        return None  # pragma: no cover


class TopologyStateGroupingBase:
    def __init__(
        self,
        uiName: str | None = None,
        uiDescription: str | None = None,
        uiNameKey: str | None = None,
        uiDescriptionKey: str | None = None,
        tierSelectors: list[TopologyStateTierSelector] | None = None,
        groupSelectors: list[TopologyStateGroupSelector] | None = None,
    ):
        self.uiName = uiName
        self.uiDescription = uiDescription
        self.uiNameKey = uiNameKey
        self.uiDescriptionKey = uiDescriptionKey
        self.tierSelectors = tierSelectors
        self.groupSelectors = groupSelectors

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.uiName is not None:
            _rval[Y_UINAME] = self.uiName
        if self.uiDescription is not None:
            _rval[Y_UIDESCRIPTION] = self.uiDescription
        if self.uiNameKey is not None:
            _rval[Y_UINAMEKEY] = self.uiNameKey
        if self.uiDescriptionKey is not None:
            _rval[Y_UIDESCRIPTIONKEY] = self.uiDescriptionKey
        if self.tierSelectors is not None:
            _rval[Y_TIERSELECTORS] = [x.to_input() for x in self.tierSelectors]
        if self.groupSelectors is not None:
            _rval[Y_GROUPSELECTORS] = [x.to_input() for x in self.groupSelectors]
        return _rval

    @staticmethod
    def from_input(obj) -> 'TopologyStateGroupingBase | None':
        if obj:
            _uiName = obj.get(Y_UINAME)
            _uiDescription = obj.get(Y_UIDESCRIPTION)
            _uiNameKey = obj.get(Y_UINAMEKEY)
            _uiDescriptionKey = obj.get(Y_UIDESCRIPTIONKEY)
            _tierSelectors = []
            if obj.get(Y_TIERSELECTORS) is not None:
                for x in obj.get(Y_TIERSELECTORS):
                    _tierSelectors.append(TopologyStateTierSelector.from_input(x))
            _groupSelectors = []
            if obj.get(Y_GROUPSELECTORS) is not None:
                for x in obj.get(Y_GROUPSELECTORS):
                    _groupSelectors.append(TopologyStateGroupSelector.from_input(x))
            return TopologyStateGroupingBase(
                uiName=_uiName,
                uiDescription=_uiDescription,
                uiNameKey=_uiNameKey,
                uiDescriptionKey=_uiDescriptionKey,
                tierSelectors=_tierSelectors,
                groupSelectors=_groupSelectors,
            )
        return None  # pragma: no cover
