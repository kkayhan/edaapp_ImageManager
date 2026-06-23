#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *

ENUM_NODETEMPLATEOPERATINGSYSTEM_SRL = 'srl'
ENUM_NODETEMPLATEOPERATINGSYSTEM_SROS = 'sros'
ENUM_NODETEMPLATEOPERATINGSYSTEM_EOS = 'eos'
ENUM_NODETEMPLATEOPERATINGSYSTEM_SONIC = 'sonic'
Y_NODETEMPLATE = 'nodeTemplate'
Y_OPERATINGSYSTEM = 'operatingSystem'
Y_VERSION = 'version'
Y_PLATFORM = 'platform'
Y_INTERFACEGROUP = 'interfaceGroup'
Y_INTERFACETEMPLATE = 'interfaceTemplate'
Y_LABELS = 'labels'
Y_INTERFACES = 'interfaces'
Y_SPEED = 'speed'
Y_NUMBERCHANNEL = 'numberChannel'
Y_FEC = 'fec'
# Package objects (GVK Schemas)
DESIGNER_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='Designer')


class Breakout:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'Breakout | None':
        if obj:
            return Breakout(
            )
        return None  # pragma: no cover


class InterfaceTemplate:
    def __init__(
        self,
        speed: str,
        numberChannel: int,
        fec: str | None = None,
    ):
        self.speed = speed
        self.numberChannel = numberChannel
        self.fec = fec

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.speed is not None:
            _rval[Y_SPEED] = self.speed
        if self.numberChannel is not None:
            _rval[Y_NUMBERCHANNEL] = self.numberChannel
        if self.fec is not None:
            _rval[Y_FEC] = self.fec
        return _rval

    @staticmethod
    def from_input(obj) -> 'InterfaceTemplate | None':
        if obj:
            _speed = obj.get(Y_SPEED)
            _numberChannel = obj.get(Y_NUMBERCHANNEL)
            _fec = obj.get(Y_FEC)
            return InterfaceTemplate(
                speed=_speed,
                numberChannel=_numberChannel,
                fec=_fec,
            )
        return None  # pragma: no cover


class InterfaceGroup:
    def __init__(
        self,
        interfaceTemplate: InterfaceTemplate,
        interfaces: list[str],
        labels: list[str] | None = None,
    ):
        self.interfaceTemplate = interfaceTemplate
        self.interfaces = interfaces
        self.labels = labels

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.interfaceTemplate is not None:
            _rval[Y_INTERFACETEMPLATE] = self.interfaceTemplate.to_input()
        if self.interfaces is not None:
            _rval[Y_INTERFACES] = self.interfaces
        if self.labels is not None:
            _rval[Y_LABELS] = self.labels
        return _rval

    @staticmethod
    def from_input(obj) -> 'InterfaceGroup | None':
        if obj:
            _interfaceTemplate = InterfaceTemplate.from_input(obj.get(Y_INTERFACETEMPLATE))
            _interfaces = obj.get(Y_INTERFACES)
            _labels = obj.get(Y_LABELS)
            return InterfaceGroup(
                interfaceTemplate=_interfaceTemplate,
                interfaces=_interfaces,
                labels=_labels,
            )
        return None  # pragma: no cover


class NodeTemplate:
    def __init__(
        self,
        name: str,
        operatingSystem: str,
        version: str,
        platform: str,
        interfaceGroup: list[InterfaceGroup] | None = None,
    ):
        self.name = name
        self.operatingSystem = operatingSystem
        self.version = version
        self.platform = platform
        self.interfaceGroup = interfaceGroup

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.name is not None:
            _rval[Y_NAME] = self.name
        if self.operatingSystem is not None:
            _rval[Y_OPERATINGSYSTEM] = self.operatingSystem
        if self.version is not None:
            _rval[Y_VERSION] = self.version
        if self.platform is not None:
            _rval[Y_PLATFORM] = self.platform
        if self.interfaceGroup is not None:
            _rval[Y_INTERFACEGROUP] = [x.to_input() for x in self.interfaceGroup]
        return _rval

    @staticmethod
    def from_input(obj) -> 'NodeTemplate | None':
        if obj:
            _name = obj.get(Y_NAME)
            _operatingSystem = obj.get(Y_OPERATINGSYSTEM)
            _version = obj.get(Y_VERSION)
            _platform = obj.get(Y_PLATFORM)
            _interfaceGroup = []
            if obj.get(Y_INTERFACEGROUP) is not None:
                for x in obj.get(Y_INTERFACEGROUP):
                    _interfaceGroup.append(InterfaceGroup.from_input(x))
            return NodeTemplate(
                name=_name,
                operatingSystem=_operatingSystem,
                version=_version,
                platform=_platform,
                interfaceGroup=_interfaceGroup,
            )
        return None  # pragma: no cover


class DesignerSpec:
    def __init__(
        self,
        nodeTemplate: list[NodeTemplate],
    ):
        self.nodeTemplate = nodeTemplate

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.nodeTemplate is not None:
            _rval[Y_NODETEMPLATE] = [x.to_input() for x in self.nodeTemplate]
        return _rval

    @staticmethod
    def from_input(obj) -> 'DesignerSpec | None':
        if obj:
            _nodeTemplate = []
            if obj.get(Y_NODETEMPLATE) is not None:
                for x in obj.get(Y_NODETEMPLATE):
                    _nodeTemplate.append(NodeTemplate.from_input(x))
            return DesignerSpec(
                nodeTemplate=_nodeTemplate,
            )
        return None  # pragma: no cover


class DesignerStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'DesignerStatus | None':
        if obj:
            return DesignerStatus(
            )
        return None  # pragma: no cover


class Designer:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: DesignerSpec | None = None,
        status: DesignerStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = DESIGNER_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'Designer | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = DesignerSpec.from_input(obj.get(Y_SPEC, None))
            _status = DesignerStatus.from_input(obj.get(Y_STATUS))
            return Designer(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class DesignerList:
    def __init__(
        self,
        items: list[Designer],
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
    def from_input(obj) -> 'DesignerList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return DesignerList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
