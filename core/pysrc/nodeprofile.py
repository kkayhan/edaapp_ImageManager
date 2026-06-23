#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *

ENUM_DHCPPREFERREDADDRESSFAMILY_IPV4 = 'IPv4'
ENUM_DHCPPREFERREDADDRESSFAMILY_IPV6 = 'IPv6'

ENUM_DHCP4OPTIONSOPTION_1_SUBNETMASK = '1-SubnetMask'
ENUM_DHCP4OPTIONSOPTION_2_TIMEOFFSET = '2-TimeOffset'
ENUM_DHCP4OPTIONSOPTION_3_ROUTER = '3-Router'
ENUM_DHCP4OPTIONSOPTION_4_TIMESERVER = '4-TimeServer'
ENUM_DHCP4OPTIONSOPTION_5_NAMESERVER = '5-NameServer'
ENUM_DHCP4OPTIONSOPTION_6_DOMAINNAMESERVER = '6-DomainNameServer'
ENUM_DHCP4OPTIONSOPTION_7_LOGSERVER = '7-LogServer'
ENUM_DHCP4OPTIONSOPTION_8_QUOTESERVER = '8-QuoteServer'
ENUM_DHCP4OPTIONSOPTION_9_LPRSERVER = '9-LPRServer'
ENUM_DHCP4OPTIONSOPTION_10_IMPRESSSERVER = '10-ImpressServer'
ENUM_DHCP4OPTIONSOPTION_11_RESOURCELOCATIONSERVER = '11-ResourceLocationServer'
ENUM_DHCP4OPTIONSOPTION_12_HOSTNAME = '12-HostName'
ENUM_DHCP4OPTIONSOPTION_13_BOOTFILESIZE = '13-BootFileSize'
ENUM_DHCP4OPTIONSOPTION_14_MERITDUMPFILE = '14-MeritDumpFile'
ENUM_DHCP4OPTIONSOPTION_15_DOMAINNAME = '15-DomainName'
ENUM_DHCP4OPTIONSOPTION_16_SWAPSERVER = '16-SwapServer'
ENUM_DHCP4OPTIONSOPTION_17_ROOTPATH = '17-RootPath'
ENUM_DHCP4OPTIONSOPTION_18_EXTENSIONSPATH = '18-ExtensionsPath'
ENUM_DHCP4OPTIONSOPTION_19_IPFORWARDING = '19-IPForwarding'
ENUM_DHCP4OPTIONSOPTION_20_NONLOCALSOURCEROUTING = '20-NonLocalSourceRouting'
ENUM_DHCP4OPTIONSOPTION_21_POLICYFILTER = '21-PolicyFilter'
ENUM_DHCP4OPTIONSOPTION_22_MAXIMUMDATAGRAMASSEMBLYSIZE = '22-MaximumDatagramAssemblySize'
ENUM_DHCP4OPTIONSOPTION_23_DEFAULTIPTTL = '23-DefaultIPTTL'
ENUM_DHCP4OPTIONSOPTION_24_PATHMTUAGINGTIMEOUT = '24-PathMTUAgingTimeout'
ENUM_DHCP4OPTIONSOPTION_25_PATHMTUPLATEAUTABLE = '25-PathMTUPlateauTable'
ENUM_DHCP4OPTIONSOPTION_26_INTERFACEMTU = '26-InterfaceMTU'
ENUM_DHCP4OPTIONSOPTION_27_ALLSUBNETSARELOCAL = '27-AllSubnetsAreLocal'
ENUM_DHCP4OPTIONSOPTION_28_BROADCASTADDRESS = '28-BroadcastAddress'
ENUM_DHCP4OPTIONSOPTION_29_PERFORMMASKDISCOVERY = '29-PerformMaskDiscovery'
ENUM_DHCP4OPTIONSOPTION_30_MASKSUPPLIER = '30-MaskSupplier'
ENUM_DHCP4OPTIONSOPTION_31_PERFORMROUTERDISCOVERY = '31-PerformRouterDiscovery'
ENUM_DHCP4OPTIONSOPTION_32_ROUTERSOLICITATIONADDRESS = '32-RouterSolicitationAddress'
ENUM_DHCP4OPTIONSOPTION_33_STATICROUTINGTABLE = '33-StaticRoutingTable'
ENUM_DHCP4OPTIONSOPTION_34_TRAILERENCAPSULATION = '34-TrailerEncapsulation'
ENUM_DHCP4OPTIONSOPTION_35_ARPCACHETIMEOUT = '35-ArpCacheTimeout'
ENUM_DHCP4OPTIONSOPTION_36_ETHERNETENCAPSULATION = '36-EthernetEncapsulation'
ENUM_DHCP4OPTIONSOPTION_37_DEFAULTCPTTL = '37-DefaulTCPTTL'
ENUM_DHCP4OPTIONSOPTION_38_TCPKEEPALIVEINTERVAL = '38-TCPKeepaliveInterval'
ENUM_DHCP4OPTIONSOPTION_39_TCPKEEPALIVEGARBAGE = '39-TCPKeepaliveGarbage'
ENUM_DHCP4OPTIONSOPTION_40_NETWORKINFORMATIONSERVICEDOMAIN = '40-NetworkInformationServiceDomain'
ENUM_DHCP4OPTIONSOPTION_41_NETWORKINFORMATIONSERVERS = '41-NetworkInformationServers'
ENUM_DHCP4OPTIONSOPTION_42_NTPSERVERS = '42-NTPServers'
ENUM_DHCP4OPTIONSOPTION_43_VENDORSPECIFICINFORMATION = '43-VendorSpecificInformation'
ENUM_DHCP4OPTIONSOPTION_44_NETBIOSOVERTCPIPNAMESERVER = '44-NetBIOSOverTCPIPNameServer'
ENUM_DHCP4OPTIONSOPTION_45_NETBIOSOVERTCPIPDATAGRAMDISTRIBUTIONSERVER = '45-NetBIOSOverTCPIPDatagramDistributionServer'
ENUM_DHCP4OPTIONSOPTION_46_NETBIOSOVERTCPIPNODETYPE = '46-NetBIOSOverTCPIPNodeType'
ENUM_DHCP4OPTIONSOPTION_47_NETBIOSOVERTCPIPSCOPE = '47-NetBIOSOverTCPIPScope'
ENUM_DHCP4OPTIONSOPTION_48_XWINDOWSYSTEMFONTSERVER = '48-XWindowSystemFontServer'
ENUM_DHCP4OPTIONSOPTION_49_XWINDOWSYSTEMDISPLAYMANAGER = '49-XWindowSystemDisplayManager'
ENUM_DHCP4OPTIONSOPTION_50_REQUESTEDIPADDRESS = '50-RequestedIPAddress'
ENUM_DHCP4OPTIONSOPTION_51_IPADDRESSLEASETIME = '51-IPAddressLeaseTime'
ENUM_DHCP4OPTIONSOPTION_52_OPTIONOVERLOAD = '52-OptionOverload'
ENUM_DHCP4OPTIONSOPTION_53_DHCPMESSAGETYPE = '53-DHCPMessageType'
ENUM_DHCP4OPTIONSOPTION_54_SERVERIDENTIFIER = '54-ServerIdentifier'
ENUM_DHCP4OPTIONSOPTION_55_PARAMETERREQUESTLIST = '55-ParameterRequestList'
ENUM_DHCP4OPTIONSOPTION_56_MESSAGE = '56-Message'
ENUM_DHCP4OPTIONSOPTION_57_MAXIMUMDHCPMESSAGESIZE = '57-MaximumDHCPMessageSize'
ENUM_DHCP4OPTIONSOPTION_58_RENEWTIMEVALUE = '58-RenewTimeValue'
ENUM_DHCP4OPTIONSOPTION_59_REBINDINGTIMEVALUE = '59-RebindingTimeValue'
ENUM_DHCP4OPTIONSOPTION_60_CLASSIDENTIFIER = '60-ClassIdentifier'
ENUM_DHCP4OPTIONSOPTION_61_CLIENTIDENTIFIER = '61-ClientIdentifier'
ENUM_DHCP4OPTIONSOPTION_62_NETWAREIPDOMAINNAME = '62-NetWareIPDomainName'
ENUM_DHCP4OPTIONSOPTION_63_NETWAREIPINFORMATION = '63-NetWareIPInformation'
ENUM_DHCP4OPTIONSOPTION_64_NETWORKINFORMATIONSERVICEPLUSDOMAIN = '64-NetworkInformationServicePlusDomain'
ENUM_DHCP4OPTIONSOPTION_65_NETWORKINFORMATIONSERVICEPLUSSERVERS = '65-NetworkInformationServicePlusServers'
ENUM_DHCP4OPTIONSOPTION_66_TFTPSERVERNAME = '66-TFTPServerName'
ENUM_DHCP4OPTIONSOPTION_67_BOOTFILENAME = '67-BootfileName'
ENUM_DHCP4OPTIONSOPTION_68_MOBILEIPHOMEAGENT = '68-MobileIPHomeAgent'
ENUM_DHCP4OPTIONSOPTION_69_SIMPLEMAILTRANSPORTPROTOCOLSERVER = '69-SimpleMailTransportProtocolServer'
ENUM_DHCP4OPTIONSOPTION_70_POSTOFFICEPROTOCOLSERVER = '70-PostOfficeProtocolServer'
ENUM_DHCP4OPTIONSOPTION_71_NETWORKNEWSTRANSPORTPROTOCOLSERVER = '71-NetworkNewsTransportProtocolServer'
ENUM_DHCP4OPTIONSOPTION_72_DEFAULTWORLDWIDEWEBSERVER = '72-DefaultWorldWideWebServer'
ENUM_DHCP4OPTIONSOPTION_73_DEFAULTFINGERSERVER = '73-DefaultFingerServer'
ENUM_DHCP4OPTIONSOPTION_74_DEFAULTINTERNETRELAYCHATSERVER = '74-DefaultInternetRelayChatServer'
ENUM_DHCP4OPTIONSOPTION_75_STREETTALKSERVER = '75-StreetTalkServer'
ENUM_DHCP4OPTIONSOPTION_76_STREETTALKDIRECTORYASSISTANCESERVER = '76-StreetTalkDirectoryAssistanceServer'
ENUM_DHCP4OPTIONSOPTION_77_USERCLASSINFORMATION = '77-UserClassInformation'
ENUM_DHCP4OPTIONSOPTION_78_SLPDIRECTORYAGENT = '78-SLPDirectoryAgent'
ENUM_DHCP4OPTIONSOPTION_79_SLPSERVICESCOPE = '79-SLPServiceScope'
ENUM_DHCP4OPTIONSOPTION_80_RAPIDCOMMIT = '80-RapidCommit'
ENUM_DHCP4OPTIONSOPTION_81_FQDN = '81-FQDN'
ENUM_DHCP4OPTIONSOPTION_82_RELAYAGENTINFORMATION = '82-RelayAgentInformation'
ENUM_DHCP4OPTIONSOPTION_83_INTERNETSTORAGENAMESERVICE = '83-InternetStorageNameService'
ENUM_DHCP4OPTIONSOPTION_85_NDSSERVERS = '85-NDSServers'
ENUM_DHCP4OPTIONSOPTION_86_NDSTREENAME = '86-NDSTreeName'
ENUM_DHCP4OPTIONSOPTION_87_NDSCONTEXT = '87-NDSContext'
ENUM_DHCP4OPTIONSOPTION_88_BCMCSCONTROLLERDOMAINNAMELIST = '88-BCMCSControllerDomainNameList'
ENUM_DHCP4OPTIONSOPTION_89_BCMCSCONTROLLERIPV4ADDRESSLIST = '89-BCMCSControllerIPv4AddressList'
ENUM_DHCP4OPTIONSOPTION_90_AUTHENTICATION = '90-Authentication'
ENUM_DHCP4OPTIONSOPTION_91_CLIENTLASTTRANSACTIONTIME = '91-ClientLastTransactionTime'
ENUM_DHCP4OPTIONSOPTION_92_ASSOCIATEDIP = '92-AssociatedIP'
ENUM_DHCP4OPTIONSOPTION_93_CLIENTSYSTEMARCHITECTURETYPE = '93-ClientSystemArchitectureType'
ENUM_DHCP4OPTIONSOPTION_94_CLIENTNETWORKINTERFACEIDENTIFIER = '94-ClientNetworkInterfaceIdentifier'
ENUM_DHCP4OPTIONSOPTION_95_LDAP = '95-LDAP'
ENUM_DHCP4OPTIONSOPTION_97_CLIENTMACHINEIDENTIFIER = '97-ClientMachineIdentifier'
ENUM_DHCP4OPTIONSOPTION_98_OPENGROUPUSERAUTHENTICATION = '98-OpenGroupUserAuthentication'
ENUM_DHCP4OPTIONSOPTION_99_GEOCONFCIVIC = '99-GeoConfCivic'
ENUM_DHCP4OPTIONSOPTION_100_IEEE10031TZSTRING = '100-IEEE10031TZString'
ENUM_DHCP4OPTIONSOPTION_101_REFERENCETOTZDATABASE = '101-ReferenceToTZDatabase'
ENUM_DHCP4OPTIONSOPTION_112_NETINFOPARENTSERVERADDRESS = '112-NetInfoParentServerAddress'
ENUM_DHCP4OPTIONSOPTION_113_NETINFOPARENTSERVERTAG = '113-NetInfoParentServerTag'
ENUM_DHCP4OPTIONSOPTION_114_URL = '114-URL'
ENUM_DHCP4OPTIONSOPTION_116_AUTOCONFIGURE = '116-AutoConfigure'
ENUM_DHCP4OPTIONSOPTION_117_NAMESERVICESEARCH = '117-NameServiceSearch'
ENUM_DHCP4OPTIONSOPTION_118_SUBNETSELECTION = '118-SubnetSelection'
ENUM_DHCP4OPTIONSOPTION_119_DNSDOMAINSEARCHLIST = '119-DNSDomainSearchList'
ENUM_DHCP4OPTIONSOPTION_120_SIPSERVERS = '120-SIPServers'
ENUM_DHCP4OPTIONSOPTION_121_CLASSLESSSTATICROUTE = '121-ClasslessStaticRoute'
ENUM_DHCP4OPTIONSOPTION_122_CCC = '122-CCC'
ENUM_DHCP4OPTIONSOPTION_123_GEOCONF = '123-GeoConf'
ENUM_DHCP4OPTIONSOPTION_124_VENDORIDENTIFYINGVENDORCLASS = '124-VendorIdentifyingVendorClass'
ENUM_DHCP4OPTIONSOPTION_125_VENDORIDENTIFYINGVENDORSPECIFIC = '125-VendorIdentifyingVendorSpecific'
ENUM_DHCP4OPTIONSOPTION_128_TFTPSERVERIPADDRESS = '128-TFTPServerIPAddress'
ENUM_DHCP4OPTIONSOPTION_129_CALLSERVERIPADDRESS = '129-CallServerIPAddress'
ENUM_DHCP4OPTIONSOPTION_130_DISCRIMINATIONSTRING = '130-DiscriminationString'
ENUM_DHCP4OPTIONSOPTION_131_REMOTESTATISTICSSERVERIPADDRESS = '131-RemoteStatisticsServerIPAddress'
ENUM_DHCP4OPTIONSOPTION_132_8021PVLANID = '132-8021PVLANID'
ENUM_DHCP4OPTIONSOPTION_133_8021QL2PRIORITY = '133-8021QL2Priority'
ENUM_DHCP4OPTIONSOPTION_134_DIFFSERVCODEPOINT = '134-DiffservCodePoint'
ENUM_DHCP4OPTIONSOPTION_135_HTTPPROXYFORPHONESPECIFICAPPLICATIONS = '135-HTTPProxyForPhoneSpecificApplications'
ENUM_DHCP4OPTIONSOPTION_136_PANAAUTHENTICATIONAGENT = '136-PANAAuthenticationAgent'
ENUM_DHCP4OPTIONSOPTION_137_LOSTSERVER = '137-LoSTServer'
ENUM_DHCP4OPTIONSOPTION_138_CAPWAPACCESSCONTROLLERADDRESSES = '138-CAPWAPAccessControllerAddresses'
ENUM_DHCP4OPTIONSOPTION_139_OPTIONIPV4ADDRESSMOS = '139-OPTIONIPv4AddressMoS'
ENUM_DHCP4OPTIONSOPTION_140_OPTIONIPV4FQDNMOS = '140-OPTIONIPv4FQDNMoS'
ENUM_DHCP4OPTIONSOPTION_141_SIPUACONFIGURATIONSERVICEDOMAINS = '141-SIPUAConfigurationServiceDomains'
ENUM_DHCP4OPTIONSOPTION_142_OPTIONIPV4ADDRESSANDSF = '142-OPTIONIPv4AddressANDSF'
ENUM_DHCP4OPTIONSOPTION_143_OPTIONIPV6ADDRESSANDSF = '143-OPTIONIPv6AddressANDSF'
ENUM_DHCP4OPTIONSOPTION_150_TFTPSERVERADDRESS = '150-TFTPServerAddress'
ENUM_DHCP4OPTIONSOPTION_151_STATUSCODE = '151-StatusCode'
ENUM_DHCP4OPTIONSOPTION_152_BASETIME = '152-BaseTime'
ENUM_DHCP4OPTIONSOPTION_153_STARTTIMEOFSTATE = '153-StartTimeOfState'
ENUM_DHCP4OPTIONSOPTION_154_QUERYSTARTTIME = '154-QueryStartTime'
ENUM_DHCP4OPTIONSOPTION_155_QUERYENDTIME = '155-QueryEndTime'
ENUM_DHCP4OPTIONSOPTION_156_DHCPSTATE = '156-DHCPState'
ENUM_DHCP4OPTIONSOPTION_157_DATASOURCE = '157-DataSource'
ENUM_DHCP4OPTIONSOPTION_175_ETHERBOOT = '175-Etherboot'
ENUM_DHCP4OPTIONSOPTION_176_IPTELEPHONE = '176-IPTelephone'
ENUM_DHCP4OPTIONSOPTION_177_ETHERBOOTPACKETCABLEANDCABLEHOME = '177-EtherbootPacketCableAndCableHome'
ENUM_DHCP4OPTIONSOPTION_208_PXELINUXMAGICSTRING = '208-PXELinuxMagicString'
ENUM_DHCP4OPTIONSOPTION_209_PXELINUXCONFIGFILE = '209-PXELinuxConfigFile'
ENUM_DHCP4OPTIONSOPTION_210_PXELINUXPATHPREFIX = '210-PXELinuxPathPrefix'
ENUM_DHCP4OPTIONSOPTION_211_PXELINUXREBOOTTIME = '211-PXELinuxRebootTime'
ENUM_DHCP4OPTIONSOPTION_212_OPTION6RD = '212-OPTION6RD'
ENUM_DHCP4OPTIONSOPTION_213_OPTIONV4ACCESSDOMAIN = '213-OPTIONv4AccessDomain'
ENUM_DHCP4OPTIONSOPTION_220_SUBNETALLOCATION = '220-SubnetAllocation'
ENUM_DHCP4OPTIONSOPTION_221_VIRTUALSUBNETALLOCATION = '221-VirtualSubnetAllocation'
ENUM_DHCP4OPTIONSOPTION_224_RESERVED = '224-Reserved'
ENUM_DHCP4OPTIONSOPTION_225_RESERVED = '225-Reserved'
ENUM_DHCP4OPTIONSOPTION_226_RESERVED = '226-Reserved'
ENUM_DHCP4OPTIONSOPTION_227_RESERVED = '227-Reserved'
ENUM_DHCP4OPTIONSOPTION_228_RESERVED = '228-Reserved'
ENUM_DHCP4OPTIONSOPTION_229_RESERVED = '229-Reserved'
ENUM_DHCP4OPTIONSOPTION_230_RESERVED = '230-Reserved'
ENUM_DHCP4OPTIONSOPTION_231_RESERVED = '231-Reserved'
ENUM_DHCP4OPTIONSOPTION_232_RESERVED = '232-Reserved'
ENUM_DHCP4OPTIONSOPTION_233_RESERVED = '233-Reserved'
ENUM_DHCP4OPTIONSOPTION_234_RESERVED = '234-Reserved'
ENUM_DHCP4OPTIONSOPTION_235_RESERVED = '235-Reserved'
ENUM_DHCP4OPTIONSOPTION_236_RESERVED = '236-Reserved'
ENUM_DHCP4OPTIONSOPTION_237_RESERVED = '237-Reserved'
ENUM_DHCP4OPTIONSOPTION_238_RESERVED = '238-Reserved'
ENUM_DHCP4OPTIONSOPTION_239_RESERVED = '239-Reserved'
ENUM_DHCP4OPTIONSOPTION_240_RESERVED = '240-Reserved'
ENUM_DHCP4OPTIONSOPTION_241_RESERVED = '241-Reserved'
ENUM_DHCP4OPTIONSOPTION_242_RESERVED = '242-Reserved'
ENUM_DHCP4OPTIONSOPTION_243_RESERVED = '243-Reserved'
ENUM_DHCP4OPTIONSOPTION_244_RESERVED = '244-Reserved'
ENUM_DHCP4OPTIONSOPTION_245_RESERVED = '245-Reserved'
ENUM_DHCP4OPTIONSOPTION_246_RESERVED = '246-Reserved'
ENUM_DHCP4OPTIONSOPTION_247_RESERVED = '247-Reserved'
ENUM_DHCP4OPTIONSOPTION_248_RESERVED = '248-Reserved'
ENUM_DHCP4OPTIONSOPTION_249_RESERVED = '249-Reserved'
ENUM_DHCP4OPTIONSOPTION_250_RESERVED = '250-Reserved'
ENUM_DHCP4OPTIONSOPTION_251_RESERVED = '251-Reserved'
ENUM_DHCP4OPTIONSOPTION_252_RESERVED = '252-Reserved'
ENUM_DHCP4OPTIONSOPTION_253_RESERVED = '253-Reserved'
ENUM_DHCP4OPTIONSOPTION_254_RESERVED = '254-Reserved'
ENUM_DHCP4OPTIONSOPTION_255_END = '255-End'

ENUM_DHCP6OPTIONSOPTION_59_BOOTFILEURL = '59-BootfileUrl'
ENUM_DHCP6OPTIONSOPTION_56_NTPSERVERS = '56-NTPServers'
Y_OPERATINGSYSTEM = 'operatingSystem'
Y_VERSION = 'version'
Y_NODEUSER = 'nodeUser'
Y_YANG = 'yang'
Y_LLMDB = 'llmDb'
Y_PORT = 'port'
Y_IMAGES = 'images'
Y_DHCP = 'dhcp'
Y_ONBOARDINGUSERNAME = 'onboardingUsername'
Y_ONBOARDINGPASSWORD = 'onboardingPassword'
Y_VERSIONPATH = 'versionPath'
Y_VERSIONMATCH = 'versionMatch'
Y_SERIALNUMBERPATH = 'serialNumberPath'
Y_PLATFORMPATH = 'platformPath'
Y_CONTAINERIMAGE = 'containerImage'
Y_IMAGEPULLSECRET = 'imagePullSecret'
Y_LICENSE = 'license'
Y_ANNOTATE = 'annotate'
Y_IMAGE = 'image'
Y_IMAGEMD5 = 'imageMd5'
Y_PREFERREDADDRESSFAMILY = 'preferredAddressFamily'
Y_MANAGEMENTPOOLV4 = 'managementPoolv4'
Y_MANAGEMENTPOOLV6 = 'managementPoolv6'
Y_DHCP4OPTIONS = 'dhcp4Options'
Y_DHCP6OPTIONS = 'dhcp6Options'
Y_OPTION = 'option'
Y_VALUE = 'value'
# Package objects (GVK Schemas)
NODEPROFILE_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='NodeProfile')


class Dhcp4Options:
    def __init__(
        self,
        option: str,
        value: list[str],
    ):
        self.option = option
        self.value = value

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.option is not None:
            _rval[Y_OPTION] = self.option
        if self.value is not None:
            _rval[Y_VALUE] = self.value
        return _rval

    @staticmethod
    def from_input(obj) -> 'Dhcp4Options | None':
        if obj:
            _option = obj.get(Y_OPTION)
            _value = obj.get(Y_VALUE)
            return Dhcp4Options(
                option=_option,
                value=_value,
            )
        return None  # pragma: no cover


class Dhcp6Options:
    def __init__(
        self,
        option: str,
        value: list[str],
    ):
        self.option = option
        self.value = value

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.option is not None:
            _rval[Y_OPTION] = self.option
        if self.value is not None:
            _rval[Y_VALUE] = self.value
        return _rval

    @staticmethod
    def from_input(obj) -> 'Dhcp6Options | None':
        if obj:
            _option = obj.get(Y_OPTION)
            _value = obj.get(Y_VALUE)
            return Dhcp6Options(
                option=_option,
                value=_value,
            )
        return None  # pragma: no cover


class Dhcp:
    def __init__(
        self,
        preferredAddressFamily: str | None = None,
        managementPoolv4: str | None = None,
        managementPoolv6: str | None = None,
        dhcp4Options: list[Dhcp4Options] | None = None,
        dhcp6Options: list[Dhcp6Options] | None = None,
    ):
        self.preferredAddressFamily = preferredAddressFamily
        self.managementPoolv4 = managementPoolv4
        self.managementPoolv6 = managementPoolv6
        self.dhcp4Options = dhcp4Options
        self.dhcp6Options = dhcp6Options

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.preferredAddressFamily is not None:
            _rval[Y_PREFERREDADDRESSFAMILY] = self.preferredAddressFamily
        if self.managementPoolv4 is not None:
            _rval[Y_MANAGEMENTPOOLV4] = self.managementPoolv4
        if self.managementPoolv6 is not None:
            _rval[Y_MANAGEMENTPOOLV6] = self.managementPoolv6
        if self.dhcp4Options is not None:
            _rval[Y_DHCP4OPTIONS] = [x.to_input() for x in self.dhcp4Options]
        if self.dhcp6Options is not None:
            _rval[Y_DHCP6OPTIONS] = [x.to_input() for x in self.dhcp6Options]
        return _rval

    @staticmethod
    def from_input(obj) -> 'Dhcp | None':
        if obj:
            _preferredAddressFamily = obj.get(Y_PREFERREDADDRESSFAMILY)
            _managementPoolv4 = obj.get(Y_MANAGEMENTPOOLV4)
            _managementPoolv6 = obj.get(Y_MANAGEMENTPOOLV6)
            _dhcp4Options = []
            if obj.get(Y_DHCP4OPTIONS) is not None:
                for x in obj.get(Y_DHCP4OPTIONS):
                    _dhcp4Options.append(Dhcp4Options.from_input(x))
            _dhcp6Options = []
            if obj.get(Y_DHCP6OPTIONS) is not None:
                for x in obj.get(Y_DHCP6OPTIONS):
                    _dhcp6Options.append(Dhcp6Options.from_input(x))
            return Dhcp(
                preferredAddressFamily=_preferredAddressFamily,
                managementPoolv4=_managementPoolv4,
                managementPoolv6=_managementPoolv6,
                dhcp4Options=_dhcp4Options,
                dhcp6Options=_dhcp6Options,
            )
        return None  # pragma: no cover


class Image:
    def __init__(
        self,
        image: str,
        imageMd5: str | None = None,
    ):
        self.image = image
        self.imageMd5 = imageMd5

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.image is not None:
            _rval[Y_IMAGE] = self.image
        if self.imageMd5 is not None:
            _rval[Y_IMAGEMD5] = self.imageMd5
        return _rval

    @staticmethod
    def from_input(obj) -> 'Image | None':
        if obj:
            _image = obj.get(Y_IMAGE)
            _imageMd5 = obj.get(Y_IMAGEMD5)
            return Image(
                image=_image,
                imageMd5=_imageMd5,
            )
        return None  # pragma: no cover


class NodeProfileSpec:
    def __init__(
        self,
        operatingSystem: str,
        version: str,
        nodeUser: str,
        yang: str,
        onboardingUsername: str,
        onboardingPassword: str,
        versionPath: str,
        serialNumberPath: str,
        llmDb: str | None = None,
        port: int | None = None,
        images: list[Image] | None = None,
        dhcp: Dhcp | None = None,
        versionMatch: str | None = None,
        platformPath: str | None = None,
        containerImage: str | None = None,
        imagePullSecret: str | None = None,
        license: str | None = None,
        annotate: bool | None = None,
    ):
        self.operatingSystem = operatingSystem
        self.version = version
        self.nodeUser = nodeUser
        self.yang = yang
        self.onboardingUsername = onboardingUsername
        self.onboardingPassword = onboardingPassword
        self.versionPath = versionPath
        self.serialNumberPath = serialNumberPath
        self.llmDb = llmDb
        self.port = port
        self.images = images
        self.dhcp = dhcp
        self.versionMatch = versionMatch
        self.platformPath = platformPath
        self.containerImage = containerImage
        self.imagePullSecret = imagePullSecret
        self.license = license
        self.annotate = annotate

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.operatingSystem is not None:
            _rval[Y_OPERATINGSYSTEM] = self.operatingSystem
        if self.version is not None:
            _rval[Y_VERSION] = self.version
        if self.nodeUser is not None:
            _rval[Y_NODEUSER] = self.nodeUser
        if self.yang is not None:
            _rval[Y_YANG] = self.yang
        if self.onboardingUsername is not None:
            _rval[Y_ONBOARDINGUSERNAME] = self.onboardingUsername
        if self.onboardingPassword is not None:
            _rval[Y_ONBOARDINGPASSWORD] = self.onboardingPassword
        if self.versionPath is not None:
            _rval[Y_VERSIONPATH] = self.versionPath
        if self.serialNumberPath is not None:
            _rval[Y_SERIALNUMBERPATH] = self.serialNumberPath
        if self.llmDb is not None:
            _rval[Y_LLMDB] = self.llmDb
        if self.port is not None:
            _rval[Y_PORT] = self.port
        if self.images is not None:
            _rval[Y_IMAGES] = [x.to_input() for x in self.images]
        if self.dhcp is not None:
            _rval[Y_DHCP] = self.dhcp.to_input()
        if self.versionMatch is not None:
            _rval[Y_VERSIONMATCH] = self.versionMatch
        if self.platformPath is not None:
            _rval[Y_PLATFORMPATH] = self.platformPath
        if self.containerImage is not None:
            _rval[Y_CONTAINERIMAGE] = self.containerImage
        if self.imagePullSecret is not None:
            _rval[Y_IMAGEPULLSECRET] = self.imagePullSecret
        if self.license is not None:
            _rval[Y_LICENSE] = self.license
        if self.annotate is not None:
            _rval[Y_ANNOTATE] = self.annotate
        return _rval

    @staticmethod
    def from_input(obj) -> 'NodeProfileSpec | None':
        if obj:
            _operatingSystem = obj.get(Y_OPERATINGSYSTEM)
            _version = obj.get(Y_VERSION)
            _nodeUser = obj.get(Y_NODEUSER)
            _yang = obj.get(Y_YANG)
            _onboardingUsername = obj.get(Y_ONBOARDINGUSERNAME, "admin")
            _onboardingPassword = obj.get(Y_ONBOARDINGPASSWORD, "NokiaSrl1!")
            _versionPath = obj.get(Y_VERSIONPATH)
            _serialNumberPath = obj.get(Y_SERIALNUMBERPATH)
            _llmDb = obj.get(Y_LLMDB)
            _port = obj.get(Y_PORT, 57400)
            _images = []
            if obj.get(Y_IMAGES) is not None:
                for x in obj.get(Y_IMAGES):
                    _images.append(Image.from_input(x))
            _dhcp = Dhcp.from_input(obj.get(Y_DHCP))
            _versionMatch = obj.get(Y_VERSIONMATCH)
            _platformPath = obj.get(Y_PLATFORMPATH)
            _containerImage = obj.get(Y_CONTAINERIMAGE)
            _imagePullSecret = obj.get(Y_IMAGEPULLSECRET)
            _license = obj.get(Y_LICENSE)
            _annotate = obj.get(Y_ANNOTATE, False)
            return NodeProfileSpec(
                operatingSystem=_operatingSystem,
                version=_version,
                nodeUser=_nodeUser,
                yang=_yang,
                onboardingUsername=_onboardingUsername,
                onboardingPassword=_onboardingPassword,
                versionPath=_versionPath,
                serialNumberPath=_serialNumberPath,
                llmDb=_llmDb,
                port=_port,
                images=_images,
                dhcp=_dhcp,
                versionMatch=_versionMatch,
                platformPath=_platformPath,
                containerImage=_containerImage,
                imagePullSecret=_imagePullSecret,
                license=_license,
                annotate=_annotate,
            )
        return None  # pragma: no cover


class NodeProfileStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'NodeProfileStatus | None':
        if obj:
            return NodeProfileStatus(
            )
        return None  # pragma: no cover


class NodeProfile:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: NodeProfileSpec | None = None,
        status: NodeProfileStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = NODEPROFILE_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'NodeProfile | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = NodeProfileSpec.from_input(obj.get(Y_SPEC, None))
            _status = NodeProfileStatus.from_input(obj.get(Y_STATUS))
            return NodeProfile(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class NodeProfileList:
    def __init__(
        self,
        items: list[NodeProfile],
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
    def from_input(obj) -> 'NodeProfileList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return NodeProfileList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
