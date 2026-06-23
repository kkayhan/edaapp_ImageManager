#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *

ENUM_OPERATINGSYSTEM_SRL = 'srl'
ENUM_OPERATINGSYSTEM_SROS = 'sros'
ENUM_OPERATINGSYSTEM_EOS = 'eos'
ENUM_OPERATINGSYSTEM_SONIC = 'sonic'
ENUM_OPERATINGSYSTEM_IOS_XR = 'ios-xr'
ENUM_OPERATINGSYSTEM_NXOS = 'nxos'

ENUM_NPPSPECMODE_NORMAL = 'normal'
ENUM_NPPSPECMODE_MAINTENANCE = 'maintenance'
ENUM_NPPSPECMODE_NULL = 'null'
ENUM_NPPSPECMODE_EMULATE = 'emulate'
ENUM_NPPSPECMODE_MONITOR = 'monitor'

ENUM_COMPONENTKIND_CONTROLCARD = 'controlCard'
ENUM_COMPONENTKIND_LINECARD = 'lineCard'
ENUM_COMPONENTKIND_FABRIC = 'fabric'
ENUM_COMPONENTKIND_MDA = 'mda'
ENUM_COMPONENTKIND_CONNECTOR = 'connector'
ENUM_COMPONENTKIND_XIOM = 'xiom'
ENUM_COMPONENTKIND_POWERSHELF = 'powerShelf'
ENUM_COMPONENTKIND_POWERMODULE = 'powerModule'
Y_MODE = 'mode'
Y_PLATFORM = 'platform'
Y_VERSION = 'version'
Y_OPERATINGSYSTEM = 'operatingSystem'
Y_ONBOARDED = 'onBoarded'
Y_NODEPROFILE = 'nodeProfile'
Y_MACADDRESS = 'macAddress'
Y_SERIALNUMBER = 'serialNumber'
Y_SYSTEMINTERFACE = 'systemInterface'
Y_PRODUCTIONADDRESS = 'productionAddress'
Y_LICENSE = 'license'
Y_NPP = 'npp'
Y_COMPONENT = 'component'
Y_SATELLITENODES = 'satelliteNodes'
Y_IPV4 = 'ipv4'
Y_IPV6 = 'ipv6'
Y_KIND = 'kind'
Y_TYPE = 'type'
Y_SLOT = 'slot'
Y_HOSTPORT = 'hostPort'
Y_SATELLITE = 'satellite'
Y_ID = 'id'
Y_SATELLITEPROFILE = 'satelliteProfile'
Y_PORTTEMPLATE = 'portTemplate'
Y_COMPONENTS = 'components'
Y_UPLINKINTERFACES = 'uplinkInterfaces'
Y_DOWNLINKS = 'downlinks'
Y_UPLINKS = 'uplinks'
Y_CONNECTORS = 'connectors'
Y_NPP_STATE = 'npp-state'
Y_NPP_POD = 'npp-pod'
Y_NPP_DETAILS = 'npp-details'
Y_NODE_STATE = 'node-state'
Y_NODE_DETAILS = 'node-details'
Y_SIMULATE = 'simulate'
# Package objects (GVK Schemas)
TOPONODE_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='TopoNode')


class Component:
    def __init__(
        self,
        kind: str,
        type: str,
        slot: str | None = None,
    ):
        self.kind = kind
        self.type = type
        self.slot = slot

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.kind is not None:
            _rval[Y_KIND] = self.kind
        if self.type is not None:
            _rval[Y_TYPE] = self.type
        if self.slot is not None:
            _rval[Y_SLOT] = self.slot
        return _rval

    @staticmethod
    def from_input(obj) -> 'Component | None':
        if obj:
            _kind = obj.get(Y_KIND)
            _type = obj.get(Y_TYPE)
            _slot = obj.get(Y_SLOT)
            return Component(
                kind=_kind,
                type=_type,
                slot=_slot,
            )
        return None  # pragma: no cover


class NPPSpec:
    def __init__(
        self,
        mode: str | None = None,
    ):
        self.mode = mode

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.mode is not None:
            _rval[Y_MODE] = self.mode
        return _rval

    @staticmethod
    def from_input(obj) -> 'NPPSpec | None':
        if obj:
            _mode = obj.get(Y_MODE, "normal")
            return NPPSpec(
                mode=_mode,
            )
        return None  # pragma: no cover


class ProductionAddress:
    def __init__(
        self,
        ipv4: str | None = None,
        ipv6: str | None = None,
    ):
        self.ipv4 = ipv4
        self.ipv6 = ipv6

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.ipv4 is not None:
            _rval[Y_IPV4] = self.ipv4
        if self.ipv6 is not None:
            _rval[Y_IPV6] = self.ipv6
        return _rval

    @staticmethod
    def from_input(obj) -> 'ProductionAddress | None':
        if obj:
            _ipv4 = obj.get(Y_IPV4)
            _ipv6 = obj.get(Y_IPV6)
            return ProductionAddress(
                ipv4=_ipv4,
                ipv6=_ipv6,
            )
        return None  # pragma: no cover


class SatelliteHostUplink:
    def __init__(
        self,
        hostPort: str,
        satellite: str,
    ):
        self.hostPort = hostPort
        self.satellite = satellite

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.hostPort is not None:
            _rval[Y_HOSTPORT] = self.hostPort
        if self.satellite is not None:
            _rval[Y_SATELLITE] = self.satellite
        return _rval

    @staticmethod
    def from_input(obj) -> 'SatelliteHostUplink | None':
        if obj:
            _hostPort = obj.get(Y_HOSTPORT)
            _satellite = obj.get(Y_SATELLITE)
            return SatelliteHostUplink(
                hostPort=_hostPort,
                satellite=_satellite,
            )
        return None  # pragma: no cover


class SatelliteUplink:
    def __init__(
        self,
        name: str,
        downlinks: list[str] | None = None,
    ):
        self.name = name
        self.downlinks = downlinks

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.name is not None:
            _rval[Y_NAME] = self.name
        if self.downlinks is not None:
            _rval[Y_DOWNLINKS] = self.downlinks
        return _rval

    @staticmethod
    def from_input(obj) -> 'SatelliteUplink | None':
        if obj:
            _name = obj.get(Y_NAME)
            _downlinks = obj.get(Y_DOWNLINKS)
            return SatelliteUplink(
                name=_name,
                downlinks=_downlinks,
            )
        return None  # pragma: no cover


class SatellitePortTemplate:
    def __init__(
        self,
        name: str,
        uplinks: list[SatelliteUplink] | None = None,
        connectors: list[Component] | None = None,
    ):
        self.name = name
        self.uplinks = uplinks
        self.connectors = connectors

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.name is not None:
            _rval[Y_NAME] = self.name
        if self.uplinks is not None:
            _rval[Y_UPLINKS] = [x.to_input() for x in self.uplinks]
        if self.connectors is not None:
            _rval[Y_CONNECTORS] = [x.to_input() for x in self.connectors]
        return _rval

    @staticmethod
    def from_input(obj) -> 'SatellitePortTemplate | None':
        if obj:
            _name = obj.get(Y_NAME)
            _uplinks = []
            if obj.get(Y_UPLINKS) is not None:
                for x in obj.get(Y_UPLINKS):
                    _uplinks.append(SatelliteUplink.from_input(x))
            _connectors = []
            if obj.get(Y_CONNECTORS) is not None:
                for x in obj.get(Y_CONNECTORS):
                    _connectors.append(Component.from_input(x))
            return SatellitePortTemplate(
                name=_name,
                uplinks=_uplinks,
                connectors=_connectors,
            )
        return None  # pragma: no cover


class SatelliteNode:
    def __init__(
        self,
        id: str,
        type: str,
        macAddress: str | None = None,
        satelliteProfile: str | None = None,
        portTemplate: SatellitePortTemplate | None = None,
        operatingSystem: str | None = None,
        version: str | None = None,
        license: str | None = None,
        platform: str | None = None,
        components: list[Component] | None = None,
        uplinkInterfaces: list[SatelliteHostUplink] | None = None,
    ):
        self.id = id
        self.type = type
        self.macAddress = macAddress
        self.satelliteProfile = satelliteProfile
        self.portTemplate = portTemplate
        self.operatingSystem = operatingSystem
        self.version = version
        self.license = license
        self.platform = platform
        self.components = components
        self.uplinkInterfaces = uplinkInterfaces

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.id is not None:
            _rval[Y_ID] = self.id
        if self.type is not None:
            _rval[Y_TYPE] = self.type
        if self.macAddress is not None:
            _rval[Y_MACADDRESS] = self.macAddress
        if self.satelliteProfile is not None:
            _rval[Y_SATELLITEPROFILE] = self.satelliteProfile
        if self.portTemplate is not None:
            _rval[Y_PORTTEMPLATE] = self.portTemplate.to_input()
        if self.operatingSystem is not None:
            _rval[Y_OPERATINGSYSTEM] = self.operatingSystem
        if self.version is not None:
            _rval[Y_VERSION] = self.version
        if self.license is not None:
            _rval[Y_LICENSE] = self.license
        if self.platform is not None:
            _rval[Y_PLATFORM] = self.platform
        if self.components is not None:
            _rval[Y_COMPONENTS] = [x.to_input() for x in self.components]
        if self.uplinkInterfaces is not None:
            _rval[Y_UPLINKINTERFACES] = [x.to_input() for x in self.uplinkInterfaces]
        return _rval

    @staticmethod
    def from_input(obj) -> 'SatelliteNode | None':
        if obj:
            _id = obj.get(Y_ID)
            _type = obj.get(Y_TYPE)
            _macAddress = obj.get(Y_MACADDRESS)
            _satelliteProfile = obj.get(Y_SATELLITEPROFILE)
            _portTemplate = SatellitePortTemplate.from_input(obj.get(Y_PORTTEMPLATE))
            _operatingSystem = obj.get(Y_OPERATINGSYSTEM)
            _version = obj.get(Y_VERSION)
            _license = obj.get(Y_LICENSE)
            _platform = obj.get(Y_PLATFORM)
            _components = []
            if obj.get(Y_COMPONENTS) is not None:
                for x in obj.get(Y_COMPONENTS):
                    _components.append(Component.from_input(x))
            _uplinkInterfaces = []
            if obj.get(Y_UPLINKINTERFACES) is not None:
                for x in obj.get(Y_UPLINKINTERFACES):
                    _uplinkInterfaces.append(SatelliteHostUplink.from_input(x))
            return SatelliteNode(
                id=_id,
                type=_type,
                macAddress=_macAddress,
                satelliteProfile=_satelliteProfile,
                portTemplate=_portTemplate,
                operatingSystem=_operatingSystem,
                version=_version,
                license=_license,
                platform=_platform,
                components=_components,
                uplinkInterfaces=_uplinkInterfaces,
            )
        return None  # pragma: no cover


class TopoNodeSpec:
    def __init__(
        self,
        platform: str,
        version: str,
        operatingSystem: str,
        nodeProfile: str,
        npp: NPPSpec,
        onBoarded: bool | None = None,
        macAddress: str | None = None,
        serialNumber: str | None = None,
        systemInterface: str | None = None,
        productionAddress: ProductionAddress | None = None,
        license: str | None = None,
        component: list[Component] | None = None,
        satelliteNodes: list[SatelliteNode] | None = None,
    ):
        self.platform = platform
        self.version = version
        self.operatingSystem = operatingSystem
        self.nodeProfile = nodeProfile
        self.npp = npp
        self.onBoarded = onBoarded
        self.macAddress = macAddress
        self.serialNumber = serialNumber
        self.systemInterface = systemInterface
        self.productionAddress = productionAddress
        self.license = license
        self.component = component
        self.satelliteNodes = satelliteNodes

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.platform is not None:
            _rval[Y_PLATFORM] = self.platform
        if self.version is not None:
            _rval[Y_VERSION] = self.version
        if self.operatingSystem is not None:
            _rval[Y_OPERATINGSYSTEM] = self.operatingSystem
        if self.nodeProfile is not None:
            _rval[Y_NODEPROFILE] = self.nodeProfile
        if self.npp is not None:
            _rval[Y_NPP] = self.npp.to_input()
        if self.onBoarded is not None:
            _rval[Y_ONBOARDED] = self.onBoarded
        if self.macAddress is not None:
            _rval[Y_MACADDRESS] = self.macAddress
        if self.serialNumber is not None:
            _rval[Y_SERIALNUMBER] = self.serialNumber
        if self.systemInterface is not None:
            _rval[Y_SYSTEMINTERFACE] = self.systemInterface
        if self.productionAddress is not None:
            _rval[Y_PRODUCTIONADDRESS] = self.productionAddress.to_input()
        if self.license is not None:
            _rval[Y_LICENSE] = self.license
        if self.component is not None:
            _rval[Y_COMPONENT] = [x.to_input() for x in self.component]
        if self.satelliteNodes is not None:
            _rval[Y_SATELLITENODES] = [x.to_input() for x in self.satelliteNodes]
        return _rval

    @staticmethod
    def from_input(obj) -> 'TopoNodeSpec | None':
        if obj:
            _platform = obj.get(Y_PLATFORM)
            _version = obj.get(Y_VERSION)
            _operatingSystem = obj.get(Y_OPERATINGSYSTEM, "srl")
            _nodeProfile = obj.get(Y_NODEPROFILE)
            _npp = NPPSpec.from_input(obj.get(Y_NPP))
            _onBoarded = obj.get(Y_ONBOARDED, False)
            _macAddress = obj.get(Y_MACADDRESS)
            _serialNumber = obj.get(Y_SERIALNUMBER)
            _systemInterface = obj.get(Y_SYSTEMINTERFACE)
            _productionAddress = ProductionAddress.from_input(obj.get(Y_PRODUCTIONADDRESS))
            _license = obj.get(Y_LICENSE)
            _component = []
            if obj.get(Y_COMPONENT) is not None:
                for x in obj.get(Y_COMPONENT):
                    _component.append(Component.from_input(x))
            _satelliteNodes = []
            if obj.get(Y_SATELLITENODES) is not None:
                for x in obj.get(Y_SATELLITENODES):
                    _satelliteNodes.append(SatelliteNode.from_input(x))
            return TopoNodeSpec(
                platform=_platform,
                version=_version,
                operatingSystem=_operatingSystem,
                nodeProfile=_nodeProfile,
                npp=_npp,
                onBoarded=_onBoarded,
                macAddress=_macAddress,
                serialNumber=_serialNumber,
                systemInterface=_systemInterface,
                productionAddress=_productionAddress,
                license=_license,
                component=_component,
                satelliteNodes=_satelliteNodes,
            )
        return None  # pragma: no cover


class TopoNodeStatus:
    def __init__(
        self,
        npp_state: str | None = None,
        npp_pod: str | None = None,
        npp_details: str | None = None,
        node_state: str | None = None,
        node_details: str | None = None,
        operatingSystem: str | None = None,
        version: str | None = None,
        platform: str | None = None,
        simulate: bool | None = None,
    ):
        self.npp_state = npp_state
        self.npp_pod = npp_pod
        self.npp_details = npp_details
        self.node_state = node_state
        self.node_details = node_details
        self.operatingSystem = operatingSystem
        self.version = version
        self.platform = platform
        self.simulate = simulate

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.npp_state is not None:
            _rval[Y_NPP_STATE] = self.npp_state
        if self.npp_pod is not None:
            _rval[Y_NPP_POD] = self.npp_pod
        if self.npp_details is not None:
            _rval[Y_NPP_DETAILS] = self.npp_details
        if self.node_state is not None:
            _rval[Y_NODE_STATE] = self.node_state
        if self.node_details is not None:
            _rval[Y_NODE_DETAILS] = self.node_details
        if self.operatingSystem is not None:
            _rval[Y_OPERATINGSYSTEM] = self.operatingSystem
        if self.version is not None:
            _rval[Y_VERSION] = self.version
        if self.platform is not None:
            _rval[Y_PLATFORM] = self.platform
        if self.simulate is not None:
            _rval[Y_SIMULATE] = self.simulate
        return _rval

    @staticmethod
    def from_input(obj) -> 'TopoNodeStatus | None':
        if obj:
            _npp_state = obj.get(Y_NPP_STATE)
            _npp_pod = obj.get(Y_NPP_POD)
            _npp_details = obj.get(Y_NPP_DETAILS)
            _node_state = obj.get(Y_NODE_STATE)
            _node_details = obj.get(Y_NODE_DETAILS)
            _operatingSystem = obj.get(Y_OPERATINGSYSTEM)
            _version = obj.get(Y_VERSION)
            _platform = obj.get(Y_PLATFORM)
            _simulate = obj.get(Y_SIMULATE)
            return TopoNodeStatus(
                npp_state=_npp_state,
                npp_pod=_npp_pod,
                npp_details=_npp_details,
                node_state=_node_state,
                node_details=_node_details,
                operatingSystem=_operatingSystem,
                version=_version,
                platform=_platform,
                simulate=_simulate,
            )
        return None  # pragma: no cover


class TopoNode:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: TopoNodeSpec | None = None,
        status: TopoNodeStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = TOPONODE_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'TopoNode | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = TopoNodeSpec.from_input(obj.get(Y_SPEC, None))
            _status = TopoNodeStatus.from_input(obj.get(Y_STATUS))
            return TopoNode(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class TopoNodeList:
    def __init__(
        self,
        items: list[TopoNode],
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
    def from_input(obj) -> 'TopoNodeList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return TopoNodeList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
