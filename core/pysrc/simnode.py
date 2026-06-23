#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
from .toponode import Component, ProductionAddress, SatelliteHostUplink, SatellitePortTemplate

ENUM_SIMNODEOPERATINGSYSTEM_SRL = 'srl'
ENUM_SIMNODEOPERATINGSYSTEM_SROS = 'sros'
ENUM_SIMNODEOPERATINGSYSTEM_EOS = 'eos'
ENUM_SIMNODEOPERATINGSYSTEM_SONIC = 'sonic'
ENUM_SIMNODEOPERATINGSYSTEM_IOS_XR = 'ios-xr'
ENUM_SIMNODEOPERATINGSYSTEM_NXOS = 'nxos'
ENUM_SIMNODEOPERATINGSYSTEM_TESTMAN = 'testman'
ENUM_SIMNODEOPERATINGSYSTEM_SIREN = 'siren'
ENUM_SIMNODEOPERATINGSYSTEM_LINUX = 'linux'
ENUM_SIMNODEOPERATINGSYSTEM_SRLTEST = 'srltest'

ENUM_SIMNODEDHCPPREFERREDADDRESSFAMILY_IPV4 = 'IPv4'
ENUM_SIMNODEDHCPPREFERREDADDRESSFAMILY_IPV6 = 'IPv6'
Y_PREFERREDADDRESSFAMILY = 'preferredAddressFamily'
Y_ID = 'id'
Y_TYPE = 'type'
Y_MACADDRESS = 'macAddress'
Y_SATELLITEPROFILE = 'satelliteProfile'
Y_PORTTEMPLATE = 'portTemplate'
Y_OPERATINGSYSTEM = 'operatingSystem'
Y_VERSION = 'version'
Y_LICENSE = 'license'
Y_PLATFORM = 'platform'
Y_COMPONENTS = 'components'
Y_UPLINKINTERFACES = 'uplinkInterfaces'
Y_CONTAINERIMAGE = 'containerImage'
Y_IMAGEPULLSECRET = 'imagePullSecret'
Y_SERIALNUMBERPATH = 'serialNumberPath'
Y_VERSIONPATH = 'versionPath'
Y_VERSIONMATCH = 'versionMatch'
Y_PLATFORMPATH = 'platformPath'
Y_PORT = 'port'
Y_DHCP = 'dhcp'
Y_PRODUCTIONADDRESS = 'productionAddress'
Y_GATEWAYADDRESS = 'gatewayAddress'
Y_COMPONENT = 'component'
Y_SATELLITENODES = 'satelliteNodes'
Y_IPADDRESS = 'ipAddress'
# Package objects (GVK Schemas)
SIMNODE_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='SimNode')


class SimNodeDhcp:
    def __init__(
        self,
        preferredAddressFamily: str | None = None,
    ):
        self.preferredAddressFamily = preferredAddressFamily

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.preferredAddressFamily is not None:
            _rval[Y_PREFERREDADDRESSFAMILY] = self.preferredAddressFamily
        return _rval

    @staticmethod
    def from_input(obj) -> 'SimNodeDhcp | None':
        if obj:
            _preferredAddressFamily = obj.get(Y_PREFERREDADDRESSFAMILY)
            return SimNodeDhcp(
                preferredAddressFamily=_preferredAddressFamily,
            )
        return None  # pragma: no cover


class SimSatelliteNode:
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
        containerImage: str | None = None,
        imagePullSecret: str | None = None,
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
        self.containerImage = containerImage
        self.imagePullSecret = imagePullSecret

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
        if self.containerImage is not None:
            _rval[Y_CONTAINERIMAGE] = self.containerImage
        if self.imagePullSecret is not None:
            _rval[Y_IMAGEPULLSECRET] = self.imagePullSecret
        return _rval

    @staticmethod
    def from_input(obj) -> 'SimSatelliteNode | None':
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
            _containerImage = obj.get(Y_CONTAINERIMAGE)
            _imagePullSecret = obj.get(Y_IMAGEPULLSECRET)
            return SimSatelliteNode(
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
                containerImage=_containerImage,
                imagePullSecret=_imagePullSecret,
            )
        return None  # pragma: no cover


class SimNodeSpec:
    def __init__(
        self,
        serialNumberPath: str,
        versionPath: str,
        operatingSystem: str | None = None,
        version: str | None = None,
        versionMatch: str | None = None,
        platformPath: str | None = None,
        port: int | None = None,
        containerImage: str | None = None,
        imagePullSecret: str | None = None,
        dhcp: SimNodeDhcp | None = None,
        productionAddress: ProductionAddress | None = None,
        gatewayAddress: ProductionAddress | None = None,
        platform: str | None = None,
        license: str | None = None,
        component: list[Component] | None = None,
        satelliteNodes: list[SimSatelliteNode] | None = None,
    ):
        self.serialNumberPath = serialNumberPath
        self.versionPath = versionPath
        self.operatingSystem = operatingSystem
        self.version = version
        self.versionMatch = versionMatch
        self.platformPath = platformPath
        self.port = port
        self.containerImage = containerImage
        self.imagePullSecret = imagePullSecret
        self.dhcp = dhcp
        self.productionAddress = productionAddress
        self.gatewayAddress = gatewayAddress
        self.platform = platform
        self.license = license
        self.component = component
        self.satelliteNodes = satelliteNodes

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.serialNumberPath is not None:
            _rval[Y_SERIALNUMBERPATH] = self.serialNumberPath
        if self.versionPath is not None:
            _rval[Y_VERSIONPATH] = self.versionPath
        if self.operatingSystem is not None:
            _rval[Y_OPERATINGSYSTEM] = self.operatingSystem
        if self.version is not None:
            _rval[Y_VERSION] = self.version
        if self.versionMatch is not None:
            _rval[Y_VERSIONMATCH] = self.versionMatch
        if self.platformPath is not None:
            _rval[Y_PLATFORMPATH] = self.platformPath
        if self.port is not None:
            _rval[Y_PORT] = self.port
        if self.containerImage is not None:
            _rval[Y_CONTAINERIMAGE] = self.containerImage
        if self.imagePullSecret is not None:
            _rval[Y_IMAGEPULLSECRET] = self.imagePullSecret
        if self.dhcp is not None:
            _rval[Y_DHCP] = self.dhcp.to_input()
        if self.productionAddress is not None:
            _rval[Y_PRODUCTIONADDRESS] = self.productionAddress.to_input()
        if self.gatewayAddress is not None:
            _rval[Y_GATEWAYADDRESS] = self.gatewayAddress.to_input()
        if self.platform is not None:
            _rval[Y_PLATFORM] = self.platform
        if self.license is not None:
            _rval[Y_LICENSE] = self.license
        if self.component is not None:
            _rval[Y_COMPONENT] = [x.to_input() for x in self.component]
        if self.satelliteNodes is not None:
            _rval[Y_SATELLITENODES] = [x.to_input() for x in self.satelliteNodes]
        return _rval

    @staticmethod
    def from_input(obj) -> 'SimNodeSpec | None':
        if obj:
            _serialNumberPath = obj.get(Y_SERIALNUMBERPATH)
            _versionPath = obj.get(Y_VERSIONPATH)
            _operatingSystem = obj.get(Y_OPERATINGSYSTEM)
            _version = obj.get(Y_VERSION)
            _versionMatch = obj.get(Y_VERSIONMATCH)
            _platformPath = obj.get(Y_PLATFORMPATH)
            _port = obj.get(Y_PORT, 57400)
            _containerImage = obj.get(Y_CONTAINERIMAGE)
            _imagePullSecret = obj.get(Y_IMAGEPULLSECRET)
            _dhcp = SimNodeDhcp.from_input(obj.get(Y_DHCP))
            _productionAddress = ProductionAddress.from_input(obj.get(Y_PRODUCTIONADDRESS))
            _gatewayAddress = ProductionAddress.from_input(obj.get(Y_GATEWAYADDRESS))
            _platform = obj.get(Y_PLATFORM)
            _license = obj.get(Y_LICENSE)
            _component = []
            if obj.get(Y_COMPONENT) is not None:
                for x in obj.get(Y_COMPONENT):
                    _component.append(Component.from_input(x))
            _satelliteNodes = []
            if obj.get(Y_SATELLITENODES) is not None:
                for x in obj.get(Y_SATELLITENODES):
                    _satelliteNodes.append(SimSatelliteNode.from_input(x))
            return SimNodeSpec(
                serialNumberPath=_serialNumberPath,
                versionPath=_versionPath,
                operatingSystem=_operatingSystem,
                version=_version,
                versionMatch=_versionMatch,
                platformPath=_platformPath,
                port=_port,
                containerImage=_containerImage,
                imagePullSecret=_imagePullSecret,
                dhcp=_dhcp,
                productionAddress=_productionAddress,
                gatewayAddress=_gatewayAddress,
                platform=_platform,
                license=_license,
                component=_component,
                satelliteNodes=_satelliteNodes,
            )
        return None  # pragma: no cover


class SimNodeStatus:
    def __init__(
        self,
        ipAddress: str,
    ):
        self.ipAddress = ipAddress

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.ipAddress is not None:
            _rval[Y_IPADDRESS] = self.ipAddress
        return _rval

    @staticmethod
    def from_input(obj) -> 'SimNodeStatus | None':
        if obj:
            _ipAddress = obj.get(Y_IPADDRESS)
            return SimNodeStatus(
                ipAddress=_ipAddress,
            )
        return None  # pragma: no cover


class SimNode:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: SimNodeSpec | None = None,
        status: SimNodeStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = SIMNODE_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'SimNode | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = SimNodeSpec.from_input(obj.get(Y_SPEC, None))
            _status = SimNodeStatus.from_input(obj.get(Y_STATUS))
            return SimNode(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class SimNodeList:
    def __init__(
        self,
        items: list[SimNode],
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
    def from_input(obj) -> 'SimNodeList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return SimNodeList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
