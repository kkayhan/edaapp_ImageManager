#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
from .nodeprofile import Dhcp4Options, Dhcp6Options

ENUM_CSRPARAMSCSRSUITE_CSRSUITE_X509_KEY_TYPE_RSA_2048_SIGNATURE_ALGORITHM_SHA_2_256 = 'CSRSUITE_X509_KEY_TYPE_RSA_2048_SIGNATURE_ALGORITHM_SHA_2_256'
ENUM_CSRPARAMSCSRSUITE_ = ''

ENUM_TARGETNODESTATUSDHCPSTATUS_OFFERED = 'Offered'
ENUM_TARGETNODESTATUSDHCPSTATUS_ACKNOWLEDGED = 'Acknowledged'

ENUM_TARGETNODESTATUSBOOTSTRAPSTATUS_INIT = 'Init'
ENUM_TARGETNODESTATUSBOOTSTRAPSTATUS_CERTINSTALL = 'CertInstall'
ENUM_TARGETNODESTATUSBOOTSTRAPSTATUS_TCPWAIT = 'TCPWait'
ENUM_TARGETNODESTATUSBOOTSTRAPSTATUS_CONNECTING = 'Connecting'
ENUM_TARGETNODESTATUSBOOTSTRAPSTATUS_READY = 'Ready'
ENUM_TARGETNODESTATUSBOOTSTRAPSTATUS_FAILED = 'Failed'
Y_ADDRESS = 'address'
Y_PORT = 'port'
Y_MACADDRESS = 'macAddress'
Y_SERIALNUMBER = 'serialNumber'
Y_OPERATINGSYSTEM = 'operatingSystem'
Y_DHCP4 = 'dhcp4'
Y_DHCP6 = 'dhcp6'
Y_SERIALNUMBERPATH = 'serialNumberPath'
Y_VERSIONPATH = 'versionPath'
Y_PLATFORMPATH = 'platformPath'
Y_PLATFORM = 'platform'
Y_VERSIONMATCH = 'versionMatch'
Y_TRUSTBUNDLE = 'trustBundle'
Y_ISSUERREF = 'issuerRef'
Y_CSRPARAMS = 'csrParams'
Y_SKIPVERIFY = 'skipVerify'
Y_NODESECURITYPROFILE = 'nodeSecurityProfile'
Y_TLS = 'tls'
Y_CERTSECRETNAME = 'certSecretName'
Y_CSRSUITE = 'csrSuite'
Y_COMMONNAME = 'commonName'
Y_COUNTRY = 'country'
Y_STATE = 'state'
Y_CITY = 'city'
Y_ORG = 'org'
Y_ORGUNIT = 'orgUnit'
Y_CERTIFICATEVALIDITY = 'certificateValidity'
Y_SAN = 'san'
Y_DNS = 'dns'
Y_EMAILS = 'emails'
Y_IPS = 'ips'
Y_URIS = 'uris'
Y_OPTIONS = 'options'
Y_DHCPSTATUS = 'dhcpStatus'
Y_BOOTSTRAPSTATUS = 'bootstrapStatus'
Y_BOOTSTRAPSTATUSREASON = 'bootstrapStatusReason'
Y_TLSSTATUS = 'tlsStatus'
# Package objects (GVK Schemas)
TARGETNODE_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='TargetNode')


class SAN:
    def __init__(
        self,
        dns: list[str] | None = None,
        emails: list[str] | None = None,
        ips: list[str] | None = None,
        uris: list[str] | None = None,
    ):
        self.dns = dns
        self.emails = emails
        self.ips = ips
        self.uris = uris

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.dns is not None:
            _rval[Y_DNS] = self.dns
        if self.emails is not None:
            _rval[Y_EMAILS] = self.emails
        if self.ips is not None:
            _rval[Y_IPS] = self.ips
        if self.uris is not None:
            _rval[Y_URIS] = self.uris
        return _rval

    @staticmethod
    def from_input(obj) -> 'SAN | None':
        if obj:
            _dns = obj.get(Y_DNS)
            _emails = obj.get(Y_EMAILS)
            _ips = obj.get(Y_IPS)
            _uris = obj.get(Y_URIS)
            return SAN(
                dns=_dns,
                emails=_emails,
                ips=_ips,
                uris=_uris,
            )
        return None  # pragma: no cover


class CSRParams:
    def __init__(
        self,
        csrSuite: str | None = None,
        commonName: str | None = None,
        country: str | None = None,
        state: str | None = None,
        city: str | None = None,
        org: str | None = None,
        orgUnit: str | None = None,
        certificateValidity: object | None = None,
        san: SAN | None = None,
    ):
        self.csrSuite = csrSuite
        self.commonName = commonName
        self.country = country
        self.state = state
        self.city = city
        self.org = org
        self.orgUnit = orgUnit
        self.certificateValidity = certificateValidity
        self.san = san

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.csrSuite is not None:
            _rval[Y_CSRSUITE] = self.csrSuite
        if self.commonName is not None:
            _rval[Y_COMMONNAME] = self.commonName
        if self.country is not None:
            _rval[Y_COUNTRY] = self.country
        if self.state is not None:
            _rval[Y_STATE] = self.state
        if self.city is not None:
            _rval[Y_CITY] = self.city
        if self.org is not None:
            _rval[Y_ORG] = self.org
        if self.orgUnit is not None:
            _rval[Y_ORGUNIT] = self.orgUnit
        if self.certificateValidity is not None:
            _rval[Y_CERTIFICATEVALIDITY] = self.certificateValidity
        if self.san is not None:
            _rval[Y_SAN] = self.san.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'CSRParams | None':
        if obj:
            _csrSuite = obj.get(Y_CSRSUITE, "CSRSUITE_X509_KEY_TYPE_RSA_2048_SIGNATURE_ALGORITHM_SHA_2_256")
            _commonName = obj.get(Y_COMMONNAME)
            _country = obj.get(Y_COUNTRY)
            _state = obj.get(Y_STATE)
            _city = obj.get(Y_CITY)
            _org = obj.get(Y_ORG)
            _orgUnit = obj.get(Y_ORGUNIT)
            _certificateValidity = obj.get(Y_CERTIFICATEVALIDITY, "2160h")
            _san = SAN.from_input(obj.get(Y_SAN))
            return CSRParams(
                csrSuite=_csrSuite,
                commonName=_commonName,
                country=_country,
                state=_state,
                city=_city,
                org=_org,
                orgUnit=_orgUnit,
                certificateValidity=_certificateValidity,
                san=_san,
            )
        return None  # pragma: no cover


class Dhcp4Spec:
    def __init__(
        self,
        address: str,
        options: list[Dhcp4Options],
    ):
        self.address = address
        self.options = options

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.address is not None:
            _rval[Y_ADDRESS] = self.address
        if self.options is not None:
            _rval[Y_OPTIONS] = [x.to_input() for x in self.options]
        return _rval

    @staticmethod
    def from_input(obj) -> 'Dhcp4Spec | None':
        if obj:
            _address = obj.get(Y_ADDRESS)
            _options = []
            if obj.get(Y_OPTIONS) is not None:
                for x in obj.get(Y_OPTIONS):
                    _options.append(Dhcp4Options.from_input(x))
            return Dhcp4Spec(
                address=_address,
                options=_options,
            )
        return None  # pragma: no cover


class Dhcp6Spec:
    def __init__(
        self,
        address: str,
        options: list[Dhcp6Options],
    ):
        self.address = address
        self.options = options

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.address is not None:
            _rval[Y_ADDRESS] = self.address
        if self.options is not None:
            _rval[Y_OPTIONS] = [x.to_input() for x in self.options]
        return _rval

    @staticmethod
    def from_input(obj) -> 'Dhcp6Spec | None':
        if obj:
            _address = obj.get(Y_ADDRESS)
            _options = []
            if obj.get(Y_OPTIONS) is not None:
                for x in obj.get(Y_OPTIONS):
                    _options.append(Dhcp6Options.from_input(x))
            return Dhcp6Spec(
                address=_address,
                options=_options,
            )
        return None  # pragma: no cover


class TLS:
    def __init__(
        self,
        trustBundle: str | None = None,
        issuerRef: str | None = None,
        csrParams: CSRParams | None = None,
        skipVerify: bool | None = None,
    ):
        self.trustBundle = trustBundle
        self.issuerRef = issuerRef
        self.csrParams = csrParams
        self.skipVerify = skipVerify

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.trustBundle is not None:
            _rval[Y_TRUSTBUNDLE] = self.trustBundle
        if self.issuerRef is not None:
            _rval[Y_ISSUERREF] = self.issuerRef
        if self.csrParams is not None:
            _rval[Y_CSRPARAMS] = self.csrParams.to_input()
        if self.skipVerify is not None:
            _rval[Y_SKIPVERIFY] = self.skipVerify
        return _rval

    @staticmethod
    def from_input(obj) -> 'TLS | None':
        if obj:
            _trustBundle = obj.get(Y_TRUSTBUNDLE)
            _issuerRef = obj.get(Y_ISSUERREF)
            _csrParams = CSRParams.from_input(obj.get(Y_CSRPARAMS))
            _skipVerify = obj.get(Y_SKIPVERIFY)
            return TLS(
                trustBundle=_trustBundle,
                issuerRef=_issuerRef,
                csrParams=_csrParams,
                skipVerify=_skipVerify,
            )
        return None  # pragma: no cover


class TLSStatus:
    def __init__(
        self,
        nodeSecurityProfile: str | None = None,
        tls: TLS | None = None,
        certSecretName: str | None = None,
    ):
        self.nodeSecurityProfile = nodeSecurityProfile
        self.tls = tls
        self.certSecretName = certSecretName

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.nodeSecurityProfile is not None:
            _rval[Y_NODESECURITYPROFILE] = self.nodeSecurityProfile
        if self.tls is not None:
            _rval[Y_TLS] = self.tls.to_input()
        if self.certSecretName is not None:
            _rval[Y_CERTSECRETNAME] = self.certSecretName
        return _rval

    @staticmethod
    def from_input(obj) -> 'TLSStatus | None':
        if obj:
            _nodeSecurityProfile = obj.get(Y_NODESECURITYPROFILE)
            _tls = TLS.from_input(obj.get(Y_TLS))
            _certSecretName = obj.get(Y_CERTSECRETNAME)
            return TLSStatus(
                nodeSecurityProfile=_nodeSecurityProfile,
                tls=_tls,
                certSecretName=_certSecretName,
            )
        return None  # pragma: no cover


class TargetNodeSpec:
    def __init__(
        self,
        address: str,
        operatingSystem: str,
        port: int | None = None,
        macAddress: str | None = None,
        serialNumber: str | None = None,
        dhcp4: Dhcp4Spec | None = None,
        dhcp6: Dhcp6Spec | None = None,
        serialNumberPath: str | None = None,
        versionPath: str | None = None,
        platformPath: str | None = None,
        platform: str | None = None,
        versionMatch: str | None = None,
    ):
        self.address = address
        self.operatingSystem = operatingSystem
        self.port = port
        self.macAddress = macAddress
        self.serialNumber = serialNumber
        self.dhcp4 = dhcp4
        self.dhcp6 = dhcp6
        self.serialNumberPath = serialNumberPath
        self.versionPath = versionPath
        self.platformPath = platformPath
        self.platform = platform
        self.versionMatch = versionMatch

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.address is not None:
            _rval[Y_ADDRESS] = self.address
        if self.operatingSystem is not None:
            _rval[Y_OPERATINGSYSTEM] = self.operatingSystem
        if self.port is not None:
            _rval[Y_PORT] = self.port
        if self.macAddress is not None:
            _rval[Y_MACADDRESS] = self.macAddress
        if self.serialNumber is not None:
            _rval[Y_SERIALNUMBER] = self.serialNumber
        if self.dhcp4 is not None:
            _rval[Y_DHCP4] = self.dhcp4.to_input()
        if self.dhcp6 is not None:
            _rval[Y_DHCP6] = self.dhcp6.to_input()
        if self.serialNumberPath is not None:
            _rval[Y_SERIALNUMBERPATH] = self.serialNumberPath
        if self.versionPath is not None:
            _rval[Y_VERSIONPATH] = self.versionPath
        if self.platformPath is not None:
            _rval[Y_PLATFORMPATH] = self.platformPath
        if self.platform is not None:
            _rval[Y_PLATFORM] = self.platform
        if self.versionMatch is not None:
            _rval[Y_VERSIONMATCH] = self.versionMatch
        return _rval

    @staticmethod
    def from_input(obj) -> 'TargetNodeSpec | None':
        if obj:
            _address = obj.get(Y_ADDRESS)
            _operatingSystem = obj.get(Y_OPERATINGSYSTEM)
            _port = obj.get(Y_PORT)
            _macAddress = obj.get(Y_MACADDRESS)
            _serialNumber = obj.get(Y_SERIALNUMBER)
            _dhcp4 = Dhcp4Spec.from_input(obj.get(Y_DHCP4))
            _dhcp6 = Dhcp6Spec.from_input(obj.get(Y_DHCP6))
            _serialNumberPath = obj.get(Y_SERIALNUMBERPATH)
            _versionPath = obj.get(Y_VERSIONPATH)
            _platformPath = obj.get(Y_PLATFORMPATH)
            _platform = obj.get(Y_PLATFORM)
            _versionMatch = obj.get(Y_VERSIONMATCH)
            return TargetNodeSpec(
                address=_address,
                operatingSystem=_operatingSystem,
                port=_port,
                macAddress=_macAddress,
                serialNumber=_serialNumber,
                dhcp4=_dhcp4,
                dhcp6=_dhcp6,
                serialNumberPath=_serialNumberPath,
                versionPath=_versionPath,
                platformPath=_platformPath,
                platform=_platform,
                versionMatch=_versionMatch,
            )
        return None  # pragma: no cover


class TargetNodeStatus:
    def __init__(
        self,
        dhcpStatus: str | None = None,
        bootstrapStatus: str | None = None,
        bootstrapStatusReason: str | None = None,
        tlsStatus: TLSStatus | None = None,
    ):
        self.dhcpStatus = dhcpStatus
        self.bootstrapStatus = bootstrapStatus
        self.bootstrapStatusReason = bootstrapStatusReason
        self.tlsStatus = tlsStatus

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.dhcpStatus is not None:
            _rval[Y_DHCPSTATUS] = self.dhcpStatus
        if self.bootstrapStatus is not None:
            _rval[Y_BOOTSTRAPSTATUS] = self.bootstrapStatus
        if self.bootstrapStatusReason is not None:
            _rval[Y_BOOTSTRAPSTATUSREASON] = self.bootstrapStatusReason
        if self.tlsStatus is not None:
            _rval[Y_TLSSTATUS] = self.tlsStatus.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'TargetNodeStatus | None':
        if obj:
            _dhcpStatus = obj.get(Y_DHCPSTATUS)
            _bootstrapStatus = obj.get(Y_BOOTSTRAPSTATUS)
            _bootstrapStatusReason = obj.get(Y_BOOTSTRAPSTATUSREASON)
            _tlsStatus = TLSStatus.from_input(obj.get(Y_TLSSTATUS))
            return TargetNodeStatus(
                dhcpStatus=_dhcpStatus,
                bootstrapStatus=_bootstrapStatus,
                bootstrapStatusReason=_bootstrapStatusReason,
                tlsStatus=_tlsStatus,
            )
        return None  # pragma: no cover


class TargetNode:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: TargetNodeSpec | None = None,
        status: TargetNodeStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = TARGETNODE_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'TargetNode | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = TargetNodeSpec.from_input(obj.get(Y_SPEC, None))
            _status = TargetNodeStatus.from_input(obj.get(Y_STATUS))
            return TargetNode(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class TargetNodeList:
    def __init__(
        self,
        items: list[TargetNode],
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
    def from_input(obj) -> 'TargetNodeList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return TargetNodeList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
