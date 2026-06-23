#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *

ENUM_KUBERNETESIMPORTSPOLICY_ALL = 'all'
ENUM_KUBERNETESIMPORTSPOLICY_SPEC = 'spec'
ENUM_KUBERNETESIMPORTSPOLICY_ = ''

ENUM_KUBERNETESEXPORTSPOLICY_ALL = 'all'
ENUM_KUBERNETESEXPORTSPOLICY_ = ''

ENUM_KUBERNETESMODE_NONE = 'None'

ENUM_SERVICECONFIGSERVICETYPE_CLUSTERIP = 'ClusterIP'
ENUM_SERVICECONFIGSERVICETYPE_NODEPORT = 'NodePort'
ENUM_SERVICECONFIGSERVICETYPE_LOADBALANCER = 'LoadBalancer'
ENUM_SERVICECONFIGSERVICETYPE_ = ''

ENUM_APIDEPLOYMENTCONFIGSERVICETYPE_CLUSTERIP = 'ClusterIP'
ENUM_APIDEPLOYMENTCONFIGSERVICETYPE_NODEPORT = 'NodePort'
ENUM_APIDEPLOYMENTCONFIGSERVICETYPE_LOADBALANCER = 'LoadBalancer'
ENUM_APIDEPLOYMENTCONFIGSERVICETYPE_ = ''

ENUM_CLUSTEREXTERNALPROXYMODE_NONE = 'None'
ENUM_CLUSTEREXTERNALPROXYMODE_FORWARD = 'Forward'
ENUM_CLUSTEREXTERNALPROXYMODE_XFORWARD = 'XForward'

ENUM_PERSISTENTVOLUMECLAIMOPTIONSACCESSMODE_READWRITEONCE = 'ReadWriteOnce'
ENUM_PERSISTENTVOLUMECLAIMOPTIONSACCESSMODE_READWRITEMANY = 'ReadWriteMany'
ENUM_PERSISTENTVOLUMECLAIMOPTIONSACCESSMODE_READONLYMANY = 'ReadOnlyMany'
ENUM_PERSISTENTVOLUMECLAIMOPTIONSACCESSMODE_READWRITEONCEPOD = 'ReadWriteOncePod'
Y_GROUP = 'group'
Y_VERSION = 'version'
Y_KIND = 'kind'
Y_REMOTE_PATH = 'remote-path'
Y_LOCAL_SCRIPT_DIR = 'local-script-dir'
Y_SCRIPT_TIMEOUT = 'script-timeout'
Y_NUM_INTERPRETERS = 'num-interpreters'
Y_HEAP_SIZE = 'heap-size'
Y_STDOUT_CAPTURE_LIMIT = 'stdout-capture-limit'
Y_LIMITS = 'limits'
Y_REQUESTS = 'requests'
Y_IMAGE = 'image'
Y_IMAGE_CREDENTIAL = 'image-credential'
Y_RESOURCES = 'resources'
Y_GVK = 'gvk'
Y_POLICY = 'policy'
Y_MODE = 'mode'
Y_IMPORTS = 'imports'
Y_EXPORTS = 'exports'
Y_REPLICAS = 'replicas'
Y_PYTHON = 'python'
Y_ENABLELOADBALANCERNODEPORTS = 'enableLoadBalancerNodePorts'
Y_SERVICETYPE = 'serviceType'
Y_CERTDURATION = 'certDuration'
Y_CERTRENEWBEFORE = 'certRenewBefore'
Y_MINORTHRESHOLD = 'minorThreshold'
Y_MAJORTHRESHOLD = 'majorThreshold'
Y_CRITICALTHRESHOLD = 'criticalThreshold'
Y_ALARMS = 'alarms'
Y_MODEL = 'model'
Y_APIKEY = 'apiKey'
Y_REPOSITORY = 'repository'
Y_URI = 'uri'
Y_CREDENTIAL = 'credential'
Y_SERVERS = 'servers'
Y_LOCALGIT = 'localGit'
Y_ADDRESS = 'address'
Y_PORT = 'port'
Y_IPV4ADDRESS = 'ipv4Address'
Y_IPV6ADDRESS = 'ipv6Address'
Y_DOMAINNAME = 'domainName'
Y_HTTPPORT = 'httpPort'
Y_HTTPSPORT = 'httpsPort'
Y_RELAXDOMAINNAMEENFORCEMENT = 'relaxDomainNameEnforcement'
Y_PROXYMODE = 'proxyMode'
Y_MEMBERS = 'members'
Y_ACTIVE = 'active'
Y_EXTERNAL = 'external'
Y_INTERNAL = 'internal'
Y_REDUNDANCY = 'redundancy'
Y_VALUE = 'value'
Y_APPLICATIONNAME = 'applicationName'
Y_SETTINGS = 'settings'
Y_ISCXAGENT = 'isCxAgent'
Y_VCLUSTER = 'vcluster'
Y_VCLUSTER_KUBERNETES = 'vcluster-kubernetes'
Y_VCLUSTER_ETCD = 'vcluster-etcd'
Y_VCLUSTER_COREDNS = 'vcluster-coredns'
Y_VCLUSTER_PLUGIN = 'vcluster-plugin'
Y_ETCDSTORAGE = 'etcdStorage'
Y_VCLUSTER_TRUSTMANAGER = 'vcluster-trustmanager'
Y_VCLUSTER_TRUSTMANAGER_CERTBUNDLE = 'vcluster-trustmanager-certbundle'
Y_VCLUSTER_HPM = 'vcluster-hpm'
Y_ENABLED = 'enabled'
Y_SIZE = 'size'
Y_ACCESSMODE = 'accessMode'
Y_STORAGECLASSNAME = 'storageClassName'
Y_REMOTE = 'remote'
Y_RUNSHAREDIPCONTROLLER = 'runSharedIPController'
Y_SHAREDADDRESS = 'sharedAddress'
Y_BRANCHEXTERNAL = 'branchExternal'
Y_STARTPORTRANGE = 'startPortRange'
Y_CXENABLE = 'cxEnable'
Y_HOSTPATH = 'hostPath'
Y_FILEPATH = 'filePath'
Y_BRANCHLOGSENABLE = 'branchLogsEnable'
Y_ENABLE = 'enable'
Y_LOGOUTPUT = 'logoutput'
Y_LOGCOLLECTOR = 'logcollector'
Y_PERSISTENTVOLUMECLAIM = 'persistentVolumeClaim'
Y_BRANCHINSTANCE = 'branchInstance'
Y_BRANCHOPTIONS = 'branchOptions'
Y_ALLOCATIONPOOLS = 'allocationPools'
Y_GIT = 'git'
Y_CLUSTER = 'cluster'
Y_CHECKPOINT_GIT_REPO = 'checkpoint-git-repo'
Y_SCRIPTS_GIT_REPO = 'scripts-git-repo'
Y_USER_SETTINGS_GIT_REPO = 'user-settings-git-repo'
Y_CERTIFICATE_GIT_REPO = 'certificate-git-repo'
Y_IDENTITY_GIT_REPO = 'identity-git-repo'
Y_AIENGINE = 'aiEngine'
Y_ARTIFACTSERVER = 'artifactServer'
Y_BOOTSTRAPSERVER = 'bootstrapServer'
Y_CERTCHECKER = 'certChecker'
Y_CX = 'cx'
Y_CXDP = 'cxdp'
Y_CLUSTERMANAGER = 'clusterManager'
Y_VCLUSTER = 'vCluster'
Y_NPP = 'npp'
Y_METRICSSERVER = 'metricsServer'
Y_STATECONTROLLER = 'stateController'
Y_STATEAGGREGATOR = 'stateAggregator'
Y_STATEENGINE = 'stateEngine'
Y_FLOWENGINE = 'flowEngine'
Y_APPSTORE = 'appStore'
Y_APPSTOREDOCS = 'appStoreDocs'
Y_APPSTOREFLOW = 'appStoreFlow'
Y_API = 'api'
Y_TESTMAN = 'testMan'
Y_IDENTITY = 'identity'
Y_IDENTITYDB = 'identitydb'
Y_LLM = 'llm'
Y_SIMULATE = 'simulate'
Y_SIMULATENODELABELSELECTOR = 'simulateNodeLabelSelector'
Y_SINGLESTACKSERVICES = 'singleStackServices'
Y_NPPNODELABELSELECTOR = 'nppNodeLabelSelector'
Y_KUBERNETES = 'kubernetes'
Y_CUSTOMSETTINGS = 'customSettings'
Y_CXCLUSTER = 'cxCluster'
Y_INTERNALCERTDURATION = 'internalCertDuration'
Y_INTERNALCERTRENEWBEFORE = 'internalCertRenewBefore'
Y_INTERNALCERTEXCLUDESINGLELABELNAMES = 'internalCertExcludeSingleLabelNames'
Y_LOGGING = 'logging'
Y_STATUS = 'status'
Y_ACTIVITYSTATE = 'activityState'
Y_REACHABLE = 'reachable'
Y_SYNCHRONIZED = 'synchronized'
Y_LICENSEDSTATE = 'licensedState'
Y_EXPIRATIONDATE = 'expirationDate'
Y_ACTIVELICENSE = 'activeLicense'
Y_RUN_STATUS = 'run-status'
Y_LICENSES = 'licenses'
# Package objects (GVK Schemas)
ENGINECONFIG_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='EngineConfig')


class ResourceRequirements:
    def __init__(
        self,
        limits: ResourceList | None = None,
        requests: ResourceList | None = None,
    ):
        self.limits = limits
        self.requests = requests

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.limits is not None:
            _rval[Y_LIMITS] = self.limits
        if self.requests is not None:
            _rval[Y_REQUESTS] = self.requests
        return _rval

    @staticmethod
    def from_input(obj) -> 'ResourceRequirements | None':
        if obj:
            _limits = obj.get(Y_LIMITS)
            _requests = obj.get(Y_REQUESTS)
            return ResourceRequirements(
                limits=_limits,
                requests=_requests,
            )
        return None  # pragma: no cover


class APIDeploymentConfig:
    def __init__(
        self,
        image: str | None = None,
        image_credential: str | None = None,
        resources: ResourceRequirements | None = None,
        replicas: int | None = None,
        enableLoadBalancerNodePorts: bool | None = None,
        serviceType: str | None = None,
        certDuration: str | None = None,
        certRenewBefore: str | None = None,
    ):
        self.image = image
        self.image_credential = image_credential
        self.resources = resources
        self.replicas = replicas
        self.enableLoadBalancerNodePorts = enableLoadBalancerNodePorts
        self.serviceType = serviceType
        self.certDuration = certDuration
        self.certRenewBefore = certRenewBefore

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.image is not None:
            _rval[Y_IMAGE] = self.image
        if self.image_credential is not None:
            _rval[Y_IMAGE_CREDENTIAL] = self.image_credential
        if self.resources is not None:
            _rval[Y_RESOURCES] = self.resources.to_input()
        if self.replicas is not None:
            _rval[Y_REPLICAS] = self.replicas
        if self.enableLoadBalancerNodePorts is not None:
            _rval[Y_ENABLELOADBALANCERNODEPORTS] = self.enableLoadBalancerNodePorts
        if self.serviceType is not None:
            _rval[Y_SERVICETYPE] = self.serviceType
        if self.certDuration is not None:
            _rval[Y_CERTDURATION] = self.certDuration
        if self.certRenewBefore is not None:
            _rval[Y_CERTRENEWBEFORE] = self.certRenewBefore
        return _rval

    @staticmethod
    def from_input(obj) -> 'APIDeploymentConfig | None':
        if obj:
            _image = obj.get(Y_IMAGE)
            _image_credential = obj.get(Y_IMAGE_CREDENTIAL)
            _resources = ResourceRequirements.from_input(obj.get(Y_RESOURCES))
            _replicas = obj.get(Y_REPLICAS)
            _enableLoadBalancerNodePorts = obj.get(Y_ENABLELOADBALANCERNODEPORTS)
            _serviceType = obj.get(Y_SERVICETYPE, "LoadBalancer")
            _certDuration = obj.get(Y_CERTDURATION, "720h")
            _certRenewBefore = obj.get(Y_CERTRENEWBEFORE, "240h")
            return APIDeploymentConfig(
                image=_image,
                image_credential=_image_credential,
                resources=_resources,
                replicas=_replicas,
                enableLoadBalancerNodePorts=_enableLoadBalancerNodePorts,
                serviceType=_serviceType,
                certDuration=_certDuration,
                certRenewBefore=_certRenewBefore,
            )
        return None  # pragma: no cover


class AlarmThreshold:
    def __init__(
        self,
        minorThreshold: int | None = None,
        majorThreshold: int | None = None,
        criticalThreshold: int | None = None,
    ):
        self.minorThreshold = minorThreshold
        self.majorThreshold = majorThreshold
        self.criticalThreshold = criticalThreshold

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.minorThreshold is not None:
            _rval[Y_MINORTHRESHOLD] = self.minorThreshold
        if self.majorThreshold is not None:
            _rval[Y_MAJORTHRESHOLD] = self.majorThreshold
        if self.criticalThreshold is not None:
            _rval[Y_CRITICALTHRESHOLD] = self.criticalThreshold
        return _rval

    @staticmethod
    def from_input(obj) -> 'AlarmThreshold | None':
        if obj:
            _minorThreshold = obj.get(Y_MINORTHRESHOLD, 80)
            _majorThreshold = obj.get(Y_MAJORTHRESHOLD, 90)
            _criticalThreshold = obj.get(Y_CRITICALTHRESHOLD, 95)
            return AlarmThreshold(
                minorThreshold=_minorThreshold,
                majorThreshold=_majorThreshold,
                criticalThreshold=_criticalThreshold,
            )
        return None  # pragma: no cover


class AllocationPools:
    def __init__(
        self,
        alarms: AlarmThreshold | None = None,
    ):
        self.alarms = alarms

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.alarms is not None:
            _rval[Y_ALARMS] = self.alarms.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'AllocationPools | None':
        if obj:
            _alarms = AlarmThreshold.from_input(obj.get(Y_ALARMS))
            return AllocationPools(
                alarms=_alarms,
            )
        return None  # pragma: no cover


class BranchExternal:
    def __init__(
        self,
        domainName: str | None = None,
    ):
        self.domainName = domainName

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.domainName is not None:
            _rval[Y_DOMAINNAME] = self.domainName
        return _rval

    @staticmethod
    def from_input(obj) -> 'BranchExternal | None':
        if obj:
            _domainName = obj.get(Y_DOMAINNAME)
            return BranchExternal(
                domainName=_domainName,
            )
        return None  # pragma: no cover


class BranchInstance:
    def __init__(
        self,
        name: str | None = None,
        remote: bool | None = None,
        runSharedIPController: bool | None = None,
    ):
        self.name = name
        self.remote = remote
        self.runSharedIPController = runSharedIPController

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.name is not None:
            _rval[Y_NAME] = self.name
        if self.remote is not None:
            _rval[Y_REMOTE] = self.remote
        if self.runSharedIPController is not None:
            _rval[Y_RUNSHAREDIPCONTROLLER] = self.runSharedIPController
        return _rval

    @staticmethod
    def from_input(obj) -> 'BranchInstance | None':
        if obj:
            _name = obj.get(Y_NAME)
            _remote = obj.get(Y_REMOTE)
            _runSharedIPController = obj.get(Y_RUNSHAREDIPCONTROLLER)
            return BranchInstance(
                name=_name,
                remote=_remote,
                runSharedIPController=_runSharedIPController,
            )
        return None  # pragma: no cover


class BranchOptions:
    def __init__(
        self,
        sharedAddress: bool | None = None,
        branchExternal: BranchExternal | None = None,
        startPortRange: int | None = None,
    ):
        self.sharedAddress = sharedAddress
        self.branchExternal = branchExternal
        self.startPortRange = startPortRange

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.sharedAddress is not None:
            _rval[Y_SHAREDADDRESS] = self.sharedAddress
        if self.branchExternal is not None:
            _rval[Y_BRANCHEXTERNAL] = self.branchExternal.to_input()
        if self.startPortRange is not None:
            _rval[Y_STARTPORTRANGE] = self.startPortRange
        return _rval

    @staticmethod
    def from_input(obj) -> 'BranchOptions | None':
        if obj:
            _sharedAddress = obj.get(Y_SHAREDADDRESS)
            _branchExternal = BranchExternal.from_input(obj.get(Y_BRANCHEXTERNAL))
            _startPortRange = obj.get(Y_STARTPORTRANGE)
            return BranchOptions(
                sharedAddress=_sharedAddress,
                branchExternal=_branchExternal,
                startPortRange=_startPortRange,
            )
        return None  # pragma: no cover


class ClusterExternal:
    def __init__(
        self,
        ipv4Address: str | None = None,
        ipv6Address: str | None = None,
        domainName: str | None = None,
        httpPort: int | None = None,
        httpsPort: int | None = None,
        relaxDomainNameEnforcement: bool | None = None,
        proxyMode: str | None = None,
    ):
        self.ipv4Address = ipv4Address
        self.ipv6Address = ipv6Address
        self.domainName = domainName
        self.httpPort = httpPort
        self.httpsPort = httpsPort
        self.relaxDomainNameEnforcement = relaxDomainNameEnforcement
        self.proxyMode = proxyMode

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.ipv4Address is not None:
            _rval[Y_IPV4ADDRESS] = self.ipv4Address
        if self.ipv6Address is not None:
            _rval[Y_IPV6ADDRESS] = self.ipv6Address
        if self.domainName is not None:
            _rval[Y_DOMAINNAME] = self.domainName
        if self.httpPort is not None:
            _rval[Y_HTTPPORT] = self.httpPort
        if self.httpsPort is not None:
            _rval[Y_HTTPSPORT] = self.httpsPort
        if self.relaxDomainNameEnforcement is not None:
            _rval[Y_RELAXDOMAINNAMEENFORCEMENT] = self.relaxDomainNameEnforcement
        if self.proxyMode is not None:
            _rval[Y_PROXYMODE] = self.proxyMode
        return _rval

    @staticmethod
    def from_input(obj) -> 'ClusterExternal | None':
        if obj:
            _ipv4Address = obj.get(Y_IPV4ADDRESS)
            _ipv6Address = obj.get(Y_IPV6ADDRESS)
            _domainName = obj.get(Y_DOMAINNAME)
            _httpPort = obj.get(Y_HTTPPORT)
            _httpsPort = obj.get(Y_HTTPSPORT)
            _relaxDomainNameEnforcement = obj.get(Y_RELAXDOMAINNAMEENFORCEMENT, False)
            _proxyMode = obj.get(Y_PROXYMODE, "None")
            return ClusterExternal(
                ipv4Address=_ipv4Address,
                ipv6Address=_ipv6Address,
                domainName=_domainName,
                httpPort=_httpPort,
                httpsPort=_httpsPort,
                relaxDomainNameEnforcement=_relaxDomainNameEnforcement,
                proxyMode=_proxyMode,
            )
        return None  # pragma: no cover


class ClusterInternal:
    def __init__(
        self,
        httpPort: int | None = None,
        httpsPort: int | None = None,
    ):
        self.httpPort = httpPort
        self.httpsPort = httpsPort

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.httpPort is not None:
            _rval[Y_HTTPPORT] = self.httpPort
        if self.httpsPort is not None:
            _rval[Y_HTTPSPORT] = self.httpsPort
        return _rval

    @staticmethod
    def from_input(obj) -> 'ClusterInternal | None':
        if obj:
            _httpPort = obj.get(Y_HTTPPORT)
            _httpsPort = obj.get(Y_HTTPSPORT)
            return ClusterInternal(
                httpPort=_httpPort,
                httpsPort=_httpsPort,
            )
        return None  # pragma: no cover


class ClusterMember:
    def __init__(
        self,
        name: str,
        address: str,
        port: int | None = None,
    ):
        self.name = name
        self.address = address
        self.port = port

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.name is not None:
            _rval[Y_NAME] = self.name
        if self.address is not None:
            _rval[Y_ADDRESS] = self.address
        if self.port is not None:
            _rval[Y_PORT] = self.port
        return _rval

    @staticmethod
    def from_input(obj) -> 'ClusterMember | None':
        if obj:
            _name = obj.get(Y_NAME)
            _address = obj.get(Y_ADDRESS)
            _port = obj.get(Y_PORT)
            return ClusterMember(
                name=_name,
                address=_address,
                port=_port,
            )
        return None  # pragma: no cover


class ClusterRedundancy:
    def __init__(
        self,
        members: list[ClusterMember],
        active: str,
    ):
        self.members = members
        self.active = active

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.members is not None:
            _rval[Y_MEMBERS] = [x.to_input() for x in self.members]
        if self.active is not None:
            _rval[Y_ACTIVE] = self.active
        return _rval

    @staticmethod
    def from_input(obj) -> 'ClusterRedundancy | None':
        if obj:
            _members = []
            if obj.get(Y_MEMBERS) is not None:
                for x in obj.get(Y_MEMBERS):
                    _members.append(ClusterMember.from_input(x))
            _active = obj.get(Y_ACTIVE)
            return ClusterRedundancy(
                members=_members,
                active=_active,
            )
        return None  # pragma: no cover


class Cluster:
    def __init__(
        self,
        external: ClusterExternal | None = None,
        internal: ClusterInternal | None = None,
        redundancy: ClusterRedundancy | None = None,
    ):
        self.external = external
        self.internal = internal
        self.redundancy = redundancy

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.external is not None:
            _rval[Y_EXTERNAL] = self.external.to_input()
        if self.internal is not None:
            _rval[Y_INTERNAL] = self.internal.to_input()
        if self.redundancy is not None:
            _rval[Y_REDUNDANCY] = self.redundancy.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'Cluster | None':
        if obj:
            _external = ClusterExternal.from_input(obj.get(Y_EXTERNAL))
            _internal = ClusterInternal.from_input(obj.get(Y_INTERNAL))
            _redundancy = ClusterRedundancy.from_input(obj.get(Y_REDUNDANCY))
            return Cluster(
                external=_external,
                internal=_internal,
                redundancy=_redundancy,
            )
        return None  # pragma: no cover


class ClusterMemberStatus:
    def __init__(
        self,
        name: str,
        reachable: bool,
        synchronized: bool,
        activityState: str | None = None,
    ):
        self.name = name
        self.reachable = reachable
        self.synchronized = synchronized
        self.activityState = activityState

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.name is not None:
            _rval[Y_NAME] = self.name
        if self.reachable is not None:
            _rval[Y_REACHABLE] = self.reachable
        if self.synchronized is not None:
            _rval[Y_SYNCHRONIZED] = self.synchronized
        if self.activityState is not None:
            _rval[Y_ACTIVITYSTATE] = self.activityState
        return _rval

    @staticmethod
    def from_input(obj) -> 'ClusterMemberStatus | None':
        if obj:
            _name = obj.get(Y_NAME)
            _reachable = obj.get(Y_REACHABLE)
            _synchronized = obj.get(Y_SYNCHRONIZED)
            _activityState = obj.get(Y_ACTIVITYSTATE)
            return ClusterMemberStatus(
                name=_name,
                reachable=_reachable,
                synchronized=_synchronized,
                activityState=_activityState,
            )
        return None  # pragma: no cover


class ClusterRedundancyStatus:
    def __init__(
        self,
        members: list[ClusterMemberStatus] | None = None,
    ):
        self.members = members

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.members is not None:
            _rval[Y_MEMBERS] = [x.to_input() for x in self.members]
        return _rval

    @staticmethod
    def from_input(obj) -> 'ClusterRedundancyStatus | None':
        if obj:
            _members = []
            if obj.get(Y_MEMBERS) is not None:
                for x in obj.get(Y_MEMBERS):
                    _members.append(ClusterMemberStatus.from_input(x))
            return ClusterRedundancyStatus(
                members=_members,
            )
        return None  # pragma: no cover


class ClusterStatus:
    def __init__(
        self,
        redundancy: ClusterRedundancyStatus | None = None,
    ):
        self.redundancy = redundancy

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.redundancy is not None:
            _rval[Y_REDUNDANCY] = self.redundancy.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'ClusterStatus | None':
        if obj:
            _redundancy = ClusterRedundancyStatus.from_input(obj.get(Y_REDUNDANCY))
            return ClusterStatus(
                redundancy=_redundancy,
            )
        return None  # pragma: no cover


class CustomApplicationSetting:
    def __init__(
        self,
        name: str | None = None,
        value: str | None = None,
    ):
        self.name = name
        self.value = value

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.name is not None:
            _rval[Y_NAME] = self.name
        if self.value is not None:
            _rval[Y_VALUE] = self.value
        return _rval

    @staticmethod
    def from_input(obj) -> 'CustomApplicationSetting | None':
        if obj:
            _name = obj.get(Y_NAME)
            _value = obj.get(Y_VALUE)
            return CustomApplicationSetting(
                name=_name,
                value=_value,
            )
        return None  # pragma: no cover


class CustomApplicationSettings:
    def __init__(
        self,
        applicationName: str | None = None,
        settings: list[CustomApplicationSetting] | None = None,
    ):
        self.applicationName = applicationName
        self.settings = settings

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.applicationName is not None:
            _rval[Y_APPLICATIONNAME] = self.applicationName
        if self.settings is not None:
            _rval[Y_SETTINGS] = [x.to_input() for x in self.settings]
        return _rval

    @staticmethod
    def from_input(obj) -> 'CustomApplicationSettings | None':
        if obj:
            _applicationName = obj.get(Y_APPLICATIONNAME)
            _settings = []
            if obj.get(Y_SETTINGS) is not None:
                for x in obj.get(Y_SETTINGS):
                    _settings.append(CustomApplicationSetting.from_input(x))
            return CustomApplicationSettings(
                applicationName=_applicationName,
                settings=_settings,
            )
        return None  # pragma: no cover


class CxCluster:
    def __init__(
        self,
        isCxAgent: bool,
        address: str | None = None,
        port: int | None = None,
    ):
        self.isCxAgent = isCxAgent
        self.address = address
        self.port = port

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.isCxAgent is not None:
            _rval[Y_ISCXAGENT] = self.isCxAgent
        if self.address is not None:
            _rval[Y_ADDRESS] = self.address
        if self.port is not None:
            _rval[Y_PORT] = self.port
        return _rval

    @staticmethod
    def from_input(obj) -> 'CxCluster | None':
        if obj:
            _isCxAgent = obj.get(Y_ISCXAGENT)
            _address = obj.get(Y_ADDRESS)
            _port = obj.get(Y_PORT)
            return CxCluster(
                isCxAgent=_isCxAgent,
                address=_address,
                port=_port,
            )
        return None  # pragma: no cover


class DeploymentConfig:
    def __init__(
        self,
        image: str | None = None,
        image_credential: str | None = None,
        resources: ResourceRequirements | None = None,
        replicas: int | None = None,
    ):
        self.image = image
        self.image_credential = image_credential
        self.resources = resources
        self.replicas = replicas

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.image is not None:
            _rval[Y_IMAGE] = self.image
        if self.image_credential is not None:
            _rval[Y_IMAGE_CREDENTIAL] = self.image_credential
        if self.resources is not None:
            _rval[Y_RESOURCES] = self.resources.to_input()
        if self.replicas is not None:
            _rval[Y_REPLICAS] = self.replicas
        return _rval

    @staticmethod
    def from_input(obj) -> 'DeploymentConfig | None':
        if obj:
            _image = obj.get(Y_IMAGE)
            _image_credential = obj.get(Y_IMAGE_CREDENTIAL)
            _resources = ResourceRequirements.from_input(obj.get(Y_RESOURCES))
            _replicas = obj.get(Y_REPLICAS)
            return DeploymentConfig(
                image=_image,
                image_credential=_image_credential,
                resources=_resources,
                replicas=_replicas,
            )
        return None  # pragma: no cover


class EngineConfigPython:
    def __init__(
        self,
        local_script_dir: str | None = None,
        script_timeout: int | None = None,
        num_interpreters: int | None = None,
        heap_size: int | None = None,
        stdout_capture_limit: int | None = None,
    ):
        self.local_script_dir = local_script_dir
        self.script_timeout = script_timeout
        self.num_interpreters = num_interpreters
        self.heap_size = heap_size
        self.stdout_capture_limit = stdout_capture_limit

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.local_script_dir is not None:
            _rval[Y_LOCAL_SCRIPT_DIR] = self.local_script_dir
        if self.script_timeout is not None:
            _rval[Y_SCRIPT_TIMEOUT] = self.script_timeout
        if self.num_interpreters is not None:
            _rval[Y_NUM_INTERPRETERS] = self.num_interpreters
        if self.heap_size is not None:
            _rval[Y_HEAP_SIZE] = self.heap_size
        if self.stdout_capture_limit is not None:
            _rval[Y_STDOUT_CAPTURE_LIMIT] = self.stdout_capture_limit
        return _rval

    @staticmethod
    def from_input(obj) -> 'EngineConfigPython | None':
        if obj:
            _local_script_dir = obj.get(Y_LOCAL_SCRIPT_DIR)
            _script_timeout = obj.get(Y_SCRIPT_TIMEOUT)
            _num_interpreters = obj.get(Y_NUM_INTERPRETERS)
            _heap_size = obj.get(Y_HEAP_SIZE)
            _stdout_capture_limit = obj.get(Y_STDOUT_CAPTURE_LIMIT)
            return EngineConfigPython(
                local_script_dir=_local_script_dir,
                script_timeout=_script_timeout,
                num_interpreters=_num_interpreters,
                heap_size=_heap_size,
                stdout_capture_limit=_stdout_capture_limit,
            )
        return None  # pragma: no cover


class EngineGitRepo:
    def __init__(
        self,
        remote_path: str | None = None,
    ):
        self.remote_path = remote_path

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.remote_path is not None:
            _rval[Y_REMOTE_PATH] = self.remote_path
        return _rval

    @staticmethod
    def from_input(obj) -> 'EngineGitRepo | None':
        if obj:
            _remote_path = obj.get(Y_REMOTE_PATH)
            return EngineGitRepo(
                remote_path=_remote_path,
            )
        return None  # pragma: no cover


class GitServer:
    def __init__(
        self,
        uri: str,
        credential: str,
        name: str | None = None,
    ):
        self.uri = uri
        self.credential = credential
        self.name = name

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.uri is not None:
            _rval[Y_URI] = self.uri
        if self.credential is not None:
            _rval[Y_CREDENTIAL] = self.credential
        if self.name is not None:
            _rval[Y_NAME] = self.name
        return _rval

    @staticmethod
    def from_input(obj) -> 'GitServer | None':
        if obj:
            _uri = obj.get(Y_URI)
            _credential = obj.get(Y_CREDENTIAL)
            _name = obj.get(Y_NAME)
            return GitServer(
                uri=_uri,
                credential=_credential,
                name=_name,
            )
        return None  # pragma: no cover


class Git:
    def __init__(
        self,
        servers: list[GitServer] | None = None,
        localGit: bool | None = None,
        image: str | None = None,
        image_credential: str | None = None,
        resources: ResourceRequirements | None = None,
    ):
        self.servers = servers
        self.localGit = localGit
        self.image = image
        self.image_credential = image_credential
        self.resources = resources

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.servers is not None:
            _rval[Y_SERVERS] = [x.to_input() for x in self.servers]
        if self.localGit is not None:
            _rval[Y_LOCALGIT] = self.localGit
        if self.image is not None:
            _rval[Y_IMAGE] = self.image
        if self.image_credential is not None:
            _rval[Y_IMAGE_CREDENTIAL] = self.image_credential
        if self.resources is not None:
            _rval[Y_RESOURCES] = self.resources.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'Git | None':
        if obj:
            _servers = []
            if obj.get(Y_SERVERS) is not None:
                for x in obj.get(Y_SERVERS):
                    _servers.append(GitServer.from_input(x))
            _localGit = obj.get(Y_LOCALGIT)
            _image = obj.get(Y_IMAGE)
            _image_credential = obj.get(Y_IMAGE_CREDENTIAL)
            _resources = ResourceRequirements.from_input(obj.get(Y_RESOURCES))
            return Git(
                servers=_servers,
                localGit=_localGit,
                image=_image,
                image_credential=_image_credential,
                resources=_resources,
            )
        return None  # pragma: no cover


class ImageConfig:
    def __init__(
        self,
        image: str | None = None,
        image_credential: str | None = None,
        resources: ResourceRequirements | None = None,
    ):
        self.image = image
        self.image_credential = image_credential
        self.resources = resources

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.image is not None:
            _rval[Y_IMAGE] = self.image
        if self.image_credential is not None:
            _rval[Y_IMAGE_CREDENTIAL] = self.image_credential
        if self.resources is not None:
            _rval[Y_RESOURCES] = self.resources.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'ImageConfig | None':
        if obj:
            _image = obj.get(Y_IMAGE)
            _image_credential = obj.get(Y_IMAGE_CREDENTIAL)
            _resources = ResourceRequirements.from_input(obj.get(Y_RESOURCES))
            return ImageConfig(
                image=_image,
                image_credential=_image_credential,
                resources=_resources,
            )
        return None  # pragma: no cover


class KEngineIntentGroupVersionKind:
    def __init__(
        self,
        version: str,
        kind: str,
        group: str | None = None,
    ):
        self.version = version
        self.kind = kind
        self.group = group

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.version is not None:
            _rval[Y_VERSION] = self.version
        if self.kind is not None:
            _rval[Y_KIND] = self.kind
        if self.group is not None:
            _rval[Y_GROUP] = self.group
        return _rval

    @staticmethod
    def from_input(obj) -> 'KEngineIntentGroupVersionKind | None':
        if obj:
            _version = obj.get(Y_VERSION)
            _kind = obj.get(Y_KIND)
            _group = obj.get(Y_GROUP)
            return KEngineIntentGroupVersionKind(
                version=_version,
                kind=_kind,
                group=_group,
            )
        return None  # pragma: no cover


class KubernetesExports:
    def __init__(
        self,
        gvk: KEngineIntentGroupVersionKind,
        policy: str,
    ):
        self.gvk = gvk
        self.policy = policy

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.gvk is not None:
            _rval[Y_GVK] = self.gvk.to_input()
        if self.policy is not None:
            _rval[Y_POLICY] = self.policy
        return _rval

    @staticmethod
    def from_input(obj) -> 'KubernetesExports | None':
        if obj:
            _gvk = KEngineIntentGroupVersionKind.from_input(obj.get(Y_GVK))
            _policy = obj.get(Y_POLICY)
            return KubernetesExports(
                gvk=_gvk,
                policy=_policy,
            )
        return None  # pragma: no cover


class KubernetesImports:
    def __init__(
        self,
        gvk: KEngineIntentGroupVersionKind,
        policy: str,
    ):
        self.gvk = gvk
        self.policy = policy

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.gvk is not None:
            _rval[Y_GVK] = self.gvk.to_input()
        if self.policy is not None:
            _rval[Y_POLICY] = self.policy
        return _rval

    @staticmethod
    def from_input(obj) -> 'KubernetesImports | None':
        if obj:
            _gvk = KEngineIntentGroupVersionKind.from_input(obj.get(Y_GVK))
            _policy = obj.get(Y_POLICY)
            return KubernetesImports(
                gvk=_gvk,
                policy=_policy,
            )
        return None  # pragma: no cover


class Kubernetes:
    def __init__(
        self,
        mode: str | None = None,
        imports: list[KubernetesImports] | None = None,
        exports: list[KubernetesExports] | None = None,
    ):
        self.mode = mode
        self.imports = imports
        self.exports = exports

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.mode is not None:
            _rval[Y_MODE] = self.mode
        if self.imports is not None:
            _rval[Y_IMPORTS] = [x.to_input() for x in self.imports]
        if self.exports is not None:
            _rval[Y_EXPORTS] = [x.to_input() for x in self.exports]
        return _rval

    @staticmethod
    def from_input(obj) -> 'Kubernetes | None':
        if obj:
            _mode = obj.get(Y_MODE)
            _imports = []
            if obj.get(Y_IMPORTS) is not None:
                for x in obj.get(Y_IMPORTS):
                    _imports.append(KubernetesImports.from_input(x))
            _exports = []
            if obj.get(Y_EXPORTS) is not None:
                for x in obj.get(Y_EXPORTS):
                    _exports.append(KubernetesExports.from_input(x))
            return Kubernetes(
                mode=_mode,
                imports=_imports,
                exports=_exports,
            )
        return None  # pragma: no cover


class LLM:
    def __init__(
        self,
        model: str | None = None,
        apiKey: str | None = None,
    ):
        self.model = model
        self.apiKey = apiKey

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.model is not None:
            _rval[Y_MODEL] = self.model
        if self.apiKey is not None:
            _rval[Y_APIKEY] = self.apiKey
        return _rval

    @staticmethod
    def from_input(obj) -> 'LLM | None':
        if obj:
            _model = obj.get(Y_MODEL, "gpt-4-1106-preview")
            _apiKey = obj.get(Y_APIKEY)
            return LLM(
                model=_model,
                apiKey=_apiKey,
            )
        return None  # pragma: no cover


class LogOutputOptions:
    def __init__(
        self,
        image: str | None = None,
        image_credential: str | None = None,
        resources: ResourceRequirements | None = None,
        cxEnable: bool | None = None,
        hostPath: str | None = None,
        filePath: str | None = None,
        branchLogsEnable: bool | None = None,
    ):
        self.image = image
        self.image_credential = image_credential
        self.resources = resources
        self.cxEnable = cxEnable
        self.hostPath = hostPath
        self.filePath = filePath
        self.branchLogsEnable = branchLogsEnable

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.image is not None:
            _rval[Y_IMAGE] = self.image
        if self.image_credential is not None:
            _rval[Y_IMAGE_CREDENTIAL] = self.image_credential
        if self.resources is not None:
            _rval[Y_RESOURCES] = self.resources.to_input()
        if self.cxEnable is not None:
            _rval[Y_CXENABLE] = self.cxEnable
        if self.hostPath is not None:
            _rval[Y_HOSTPATH] = self.hostPath
        if self.filePath is not None:
            _rval[Y_FILEPATH] = self.filePath
        if self.branchLogsEnable is not None:
            _rval[Y_BRANCHLOGSENABLE] = self.branchLogsEnable
        return _rval

    @staticmethod
    def from_input(obj) -> 'LogOutputOptions | None':
        if obj:
            _image = obj.get(Y_IMAGE)
            _image_credential = obj.get(Y_IMAGE_CREDENTIAL)
            _resources = ResourceRequirements.from_input(obj.get(Y_RESOURCES))
            _cxEnable = obj.get(Y_CXENABLE)
            _hostPath = obj.get(Y_HOSTPATH)
            _filePath = obj.get(Y_FILEPATH)
            _branchLogsEnable = obj.get(Y_BRANCHLOGSENABLE)
            return LogOutputOptions(
                image=_image,
                image_credential=_image_credential,
                resources=_resources,
                cxEnable=_cxEnable,
                hostPath=_hostPath,
                filePath=_filePath,
                branchLogsEnable=_branchLogsEnable,
            )
        return None  # pragma: no cover


class PersistentVolumeClaimOptions:
    def __init__(
        self,
        enabled: bool | None = None,
        size: str | None = None,
        accessMode: str | None = None,
        storageClassName: str | None = None,
    ):
        self.enabled = enabled
        self.size = size
        self.accessMode = accessMode
        self.storageClassName = storageClassName

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.enabled is not None:
            _rval[Y_ENABLED] = self.enabled
        if self.size is not None:
            _rval[Y_SIZE] = self.size
        if self.accessMode is not None:
            _rval[Y_ACCESSMODE] = self.accessMode
        if self.storageClassName is not None:
            _rval[Y_STORAGECLASSNAME] = self.storageClassName
        return _rval

    @staticmethod
    def from_input(obj) -> 'PersistentVolumeClaimOptions | None':
        if obj:
            _enabled = obj.get(Y_ENABLED)
            _size = obj.get(Y_SIZE)
            _accessMode = obj.get(Y_ACCESSMODE, "ReadWriteOnce")
            _storageClassName = obj.get(Y_STORAGECLASSNAME)
            return PersistentVolumeClaimOptions(
                enabled=_enabled,
                size=_size,
                accessMode=_accessMode,
                storageClassName=_storageClassName,
            )
        return None  # pragma: no cover


class LoggingOptions:
    def __init__(
        self,
        enable: bool | None = None,
        logoutput: LogOutputOptions | None = None,
        logcollector: ImageConfig | None = None,
        persistentVolumeClaim: PersistentVolumeClaimOptions | None = None,
    ):
        self.enable = enable
        self.logoutput = logoutput
        self.logcollector = logcollector
        self.persistentVolumeClaim = persistentVolumeClaim

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.enable is not None:
            _rval[Y_ENABLE] = self.enable
        if self.logoutput is not None:
            _rval[Y_LOGOUTPUT] = self.logoutput.to_input()
        if self.logcollector is not None:
            _rval[Y_LOGCOLLECTOR] = self.logcollector.to_input()
        if self.persistentVolumeClaim is not None:
            _rval[Y_PERSISTENTVOLUMECLAIM] = self.persistentVolumeClaim.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'LoggingOptions | None':
        if obj:
            _enable = obj.get(Y_ENABLE)
            _logoutput = LogOutputOptions.from_input(obj.get(Y_LOGOUTPUT))
            _logcollector = ImageConfig.from_input(obj.get(Y_LOGCOLLECTOR))
            _persistentVolumeClaim = PersistentVolumeClaimOptions.from_input(obj.get(Y_PERSISTENTVOLUMECLAIM))
            return LoggingOptions(
                enable=_enable,
                logoutput=_logoutput,
                logcollector=_logcollector,
                persistentVolumeClaim=_persistentVolumeClaim,
            )
        return None  # pragma: no cover


class SEDeploymentConfig:
    def __init__(
        self,
        image: str | None = None,
        image_credential: str | None = None,
        resources: ResourceRequirements | None = None,
        replicas: int | None = None,
        python: EngineConfigPython | None = None,
    ):
        self.image = image
        self.image_credential = image_credential
        self.resources = resources
        self.replicas = replicas
        self.python = python

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.image is not None:
            _rval[Y_IMAGE] = self.image
        if self.image_credential is not None:
            _rval[Y_IMAGE_CREDENTIAL] = self.image_credential
        if self.resources is not None:
            _rval[Y_RESOURCES] = self.resources.to_input()
        if self.replicas is not None:
            _rval[Y_REPLICAS] = self.replicas
        if self.python is not None:
            _rval[Y_PYTHON] = self.python.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'SEDeploymentConfig | None':
        if obj:
            _image = obj.get(Y_IMAGE)
            _image_credential = obj.get(Y_IMAGE_CREDENTIAL)
            _resources = ResourceRequirements.from_input(obj.get(Y_RESOURCES))
            _replicas = obj.get(Y_REPLICAS)
            _python = EngineConfigPython.from_input(obj.get(Y_PYTHON))
            return SEDeploymentConfig(
                image=_image,
                image_credential=_image_credential,
                resources=_resources,
                replicas=_replicas,
                python=_python,
            )
        return None  # pragma: no cover


class VClusterOptions:
    def __init__(
        self,
        vcluster: ImageConfig | None = None,
        vcluster_kubernetes: ImageConfig | None = None,
        vcluster_etcd: ImageConfig | None = None,
        vcluster_coredns: ImageConfig | None = None,
        vcluster_plugin: ImageConfig | None = None,
        etcdStorage: PersistentVolumeClaimOptions | None = None,
        vcluster_trustmanager: ImageConfig | None = None,
        vcluster_trustmanager_certbundle: ImageConfig | None = None,
        vcluster_hpm: ImageConfig | None = None,
    ):
        self.vcluster = vcluster
        self.vcluster_kubernetes = vcluster_kubernetes
        self.vcluster_etcd = vcluster_etcd
        self.vcluster_coredns = vcluster_coredns
        self.vcluster_plugin = vcluster_plugin
        self.etcdStorage = etcdStorage
        self.vcluster_trustmanager = vcluster_trustmanager
        self.vcluster_trustmanager_certbundle = vcluster_trustmanager_certbundle
        self.vcluster_hpm = vcluster_hpm

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.vcluster is not None:
            _rval[Y_VCLUSTER] = self.vcluster.to_input()
        if self.vcluster_kubernetes is not None:
            _rval[Y_VCLUSTER_KUBERNETES] = self.vcluster_kubernetes.to_input()
        if self.vcluster_etcd is not None:
            _rval[Y_VCLUSTER_ETCD] = self.vcluster_etcd.to_input()
        if self.vcluster_coredns is not None:
            _rval[Y_VCLUSTER_COREDNS] = self.vcluster_coredns.to_input()
        if self.vcluster_plugin is not None:
            _rval[Y_VCLUSTER_PLUGIN] = self.vcluster_plugin.to_input()
        if self.etcdStorage is not None:
            _rval[Y_ETCDSTORAGE] = self.etcdStorage.to_input()
        if self.vcluster_trustmanager is not None:
            _rval[Y_VCLUSTER_TRUSTMANAGER] = self.vcluster_trustmanager.to_input()
        if self.vcluster_trustmanager_certbundle is not None:
            _rval[Y_VCLUSTER_TRUSTMANAGER_CERTBUNDLE] = self.vcluster_trustmanager_certbundle.to_input()
        if self.vcluster_hpm is not None:
            _rval[Y_VCLUSTER_HPM] = self.vcluster_hpm.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'VClusterOptions | None':
        if obj:
            _vcluster = ImageConfig.from_input(obj.get(Y_VCLUSTER))
            _vcluster_kubernetes = ImageConfig.from_input(obj.get(Y_VCLUSTER_KUBERNETES))
            _vcluster_etcd = ImageConfig.from_input(obj.get(Y_VCLUSTER_ETCD))
            _vcluster_coredns = ImageConfig.from_input(obj.get(Y_VCLUSTER_COREDNS))
            _vcluster_plugin = ImageConfig.from_input(obj.get(Y_VCLUSTER_PLUGIN))
            _etcdStorage = PersistentVolumeClaimOptions.from_input(obj.get(Y_ETCDSTORAGE))
            _vcluster_trustmanager = ImageConfig.from_input(obj.get(Y_VCLUSTER_TRUSTMANAGER))
            _vcluster_trustmanager_certbundle = ImageConfig.from_input(obj.get(Y_VCLUSTER_TRUSTMANAGER_CERTBUNDLE))
            _vcluster_hpm = ImageConfig.from_input(obj.get(Y_VCLUSTER_HPM))
            return VClusterOptions(
                vcluster=_vcluster,
                vcluster_kubernetes=_vcluster_kubernetes,
                vcluster_etcd=_vcluster_etcd,
                vcluster_coredns=_vcluster_coredns,
                vcluster_plugin=_vcluster_plugin,
                etcdStorage=_etcdStorage,
                vcluster_trustmanager=_vcluster_trustmanager,
                vcluster_trustmanager_certbundle=_vcluster_trustmanager_certbundle,
                vcluster_hpm=_vcluster_hpm,
            )
        return None  # pragma: no cover


class EngineConfigSpec:
    def __init__(
        self,
        simulate: bool,
        branchInstance: BranchInstance | None = None,
        branchOptions: BranchOptions | None = None,
        allocationPools: AllocationPools | None = None,
        git: Git | None = None,
        cluster: Cluster | None = None,
        checkpoint_git_repo: EngineGitRepo | None = None,
        scripts_git_repo: EngineGitRepo | None = None,
        user_settings_git_repo: EngineGitRepo | None = None,
        certificate_git_repo: EngineGitRepo | None = None,
        identity_git_repo: EngineGitRepo | None = None,
        python: EngineConfigPython | None = None,
        aiEngine: DeploymentConfig | None = None,
        artifactServer: ImageConfig | None = None,
        bootstrapServer: ImageConfig | None = None,
        certChecker: ImageConfig | None = None,
        cx: ImageConfig | None = None,
        cxdp: ImageConfig | None = None,
        clusterManager: ImageConfig | None = None,
        vCluster: VClusterOptions | None = None,
        npp: ImageConfig | None = None,
        metricsServer: ImageConfig | None = None,
        stateController: ImageConfig | None = None,
        stateAggregator: DeploymentConfig | None = None,
        stateEngine: SEDeploymentConfig | None = None,
        flowEngine: ImageConfig | None = None,
        appStore: ImageConfig | None = None,
        appStoreDocs: ImageConfig | None = None,
        appStoreFlow: ImageConfig | None = None,
        api: APIDeploymentConfig | None = None,
        testMan: ImageConfig | None = None,
        identity: DeploymentConfig | None = None,
        identitydb: DeploymentConfig | None = None,
        llm: LLM | None = None,
        simulateNodeLabelSelector: list[str] | None = None,
        singleStackServices: bool | None = None,
        nppNodeLabelSelector: list[str] | None = None,
        kubernetes: Kubernetes | None = None,
        customSettings: list[CustomApplicationSettings] | None = None,
        cxCluster: CxCluster | None = None,
        internalCertDuration: str | None = None,
        internalCertRenewBefore: str | None = None,
        internalCertExcludeSingleLabelNames: bool | None = None,
        logging: LoggingOptions | None = None,
    ):
        self.simulate = simulate
        self.branchInstance = branchInstance
        self.branchOptions = branchOptions
        self.allocationPools = allocationPools
        self.git = git
        self.cluster = cluster
        self.checkpoint_git_repo = checkpoint_git_repo
        self.scripts_git_repo = scripts_git_repo
        self.user_settings_git_repo = user_settings_git_repo
        self.certificate_git_repo = certificate_git_repo
        self.identity_git_repo = identity_git_repo
        self.python = python
        self.aiEngine = aiEngine
        self.artifactServer = artifactServer
        self.bootstrapServer = bootstrapServer
        self.certChecker = certChecker
        self.cx = cx
        self.cxdp = cxdp
        self.clusterManager = clusterManager
        self.vCluster = vCluster
        self.npp = npp
        self.metricsServer = metricsServer
        self.stateController = stateController
        self.stateAggregator = stateAggregator
        self.stateEngine = stateEngine
        self.flowEngine = flowEngine
        self.appStore = appStore
        self.appStoreDocs = appStoreDocs
        self.appStoreFlow = appStoreFlow
        self.api = api
        self.testMan = testMan
        self.identity = identity
        self.identitydb = identitydb
        self.llm = llm
        self.simulateNodeLabelSelector = simulateNodeLabelSelector
        self.singleStackServices = singleStackServices
        self.nppNodeLabelSelector = nppNodeLabelSelector
        self.kubernetes = kubernetes
        self.customSettings = customSettings
        self.cxCluster = cxCluster
        self.internalCertDuration = internalCertDuration
        self.internalCertRenewBefore = internalCertRenewBefore
        self.internalCertExcludeSingleLabelNames = internalCertExcludeSingleLabelNames
        self.logging = logging

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.simulate is not None:
            _rval[Y_SIMULATE] = self.simulate
        if self.branchInstance is not None:
            _rval[Y_BRANCHINSTANCE] = self.branchInstance.to_input()
        if self.branchOptions is not None:
            _rval[Y_BRANCHOPTIONS] = self.branchOptions.to_input()
        if self.allocationPools is not None:
            _rval[Y_ALLOCATIONPOOLS] = self.allocationPools.to_input()
        if self.git is not None:
            _rval[Y_GIT] = self.git.to_input()
        if self.cluster is not None:
            _rval[Y_CLUSTER] = self.cluster.to_input()
        if self.checkpoint_git_repo is not None:
            _rval[Y_CHECKPOINT_GIT_REPO] = self.checkpoint_git_repo.to_input()
        if self.scripts_git_repo is not None:
            _rval[Y_SCRIPTS_GIT_REPO] = self.scripts_git_repo.to_input()
        if self.user_settings_git_repo is not None:
            _rval[Y_USER_SETTINGS_GIT_REPO] = self.user_settings_git_repo.to_input()
        if self.certificate_git_repo is not None:
            _rval[Y_CERTIFICATE_GIT_REPO] = self.certificate_git_repo.to_input()
        if self.identity_git_repo is not None:
            _rval[Y_IDENTITY_GIT_REPO] = self.identity_git_repo.to_input()
        if self.python is not None:
            _rval[Y_PYTHON] = self.python.to_input()
        if self.aiEngine is not None:
            _rval[Y_AIENGINE] = self.aiEngine.to_input()
        if self.artifactServer is not None:
            _rval[Y_ARTIFACTSERVER] = self.artifactServer.to_input()
        if self.bootstrapServer is not None:
            _rval[Y_BOOTSTRAPSERVER] = self.bootstrapServer.to_input()
        if self.certChecker is not None:
            _rval[Y_CERTCHECKER] = self.certChecker.to_input()
        if self.cx is not None:
            _rval[Y_CX] = self.cx.to_input()
        if self.cxdp is not None:
            _rval[Y_CXDP] = self.cxdp.to_input()
        if self.clusterManager is not None:
            _rval[Y_CLUSTERMANAGER] = self.clusterManager.to_input()
        if self.vCluster is not None:
            _rval[Y_VCLUSTER] = self.vCluster.to_input()
        if self.npp is not None:
            _rval[Y_NPP] = self.npp.to_input()
        if self.metricsServer is not None:
            _rval[Y_METRICSSERVER] = self.metricsServer.to_input()
        if self.stateController is not None:
            _rval[Y_STATECONTROLLER] = self.stateController.to_input()
        if self.stateAggregator is not None:
            _rval[Y_STATEAGGREGATOR] = self.stateAggregator.to_input()
        if self.stateEngine is not None:
            _rval[Y_STATEENGINE] = self.stateEngine.to_input()
        if self.flowEngine is not None:
            _rval[Y_FLOWENGINE] = self.flowEngine.to_input()
        if self.appStore is not None:
            _rval[Y_APPSTORE] = self.appStore.to_input()
        if self.appStoreDocs is not None:
            _rval[Y_APPSTOREDOCS] = self.appStoreDocs.to_input()
        if self.appStoreFlow is not None:
            _rval[Y_APPSTOREFLOW] = self.appStoreFlow.to_input()
        if self.api is not None:
            _rval[Y_API] = self.api.to_input()
        if self.testMan is not None:
            _rval[Y_TESTMAN] = self.testMan.to_input()
        if self.identity is not None:
            _rval[Y_IDENTITY] = self.identity.to_input()
        if self.identitydb is not None:
            _rval[Y_IDENTITYDB] = self.identitydb.to_input()
        if self.llm is not None:
            _rval[Y_LLM] = self.llm.to_input()
        if self.simulateNodeLabelSelector is not None:
            _rval[Y_SIMULATENODELABELSELECTOR] = self.simulateNodeLabelSelector
        if self.singleStackServices is not None:
            _rval[Y_SINGLESTACKSERVICES] = self.singleStackServices
        if self.nppNodeLabelSelector is not None:
            _rval[Y_NPPNODELABELSELECTOR] = self.nppNodeLabelSelector
        if self.kubernetes is not None:
            _rval[Y_KUBERNETES] = self.kubernetes.to_input()
        if self.customSettings is not None:
            _rval[Y_CUSTOMSETTINGS] = [x.to_input() for x in self.customSettings]
        if self.cxCluster is not None:
            _rval[Y_CXCLUSTER] = self.cxCluster.to_input()
        if self.internalCertDuration is not None:
            _rval[Y_INTERNALCERTDURATION] = self.internalCertDuration
        if self.internalCertRenewBefore is not None:
            _rval[Y_INTERNALCERTRENEWBEFORE] = self.internalCertRenewBefore
        if self.internalCertExcludeSingleLabelNames is not None:
            _rval[Y_INTERNALCERTEXCLUDESINGLELABELNAMES] = self.internalCertExcludeSingleLabelNames
        if self.logging is not None:
            _rval[Y_LOGGING] = self.logging.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'EngineConfigSpec | None':
        if obj:
            _simulate = obj.get(Y_SIMULATE, True)
            _branchInstance = BranchInstance.from_input(obj.get(Y_BRANCHINSTANCE))
            _branchOptions = BranchOptions.from_input(obj.get(Y_BRANCHOPTIONS))
            _allocationPools = AllocationPools.from_input(obj.get(Y_ALLOCATIONPOOLS))
            _git = Git.from_input(obj.get(Y_GIT))
            _cluster = Cluster.from_input(obj.get(Y_CLUSTER))
            _checkpoint_git_repo = EngineGitRepo.from_input(obj.get(Y_CHECKPOINT_GIT_REPO))
            _scripts_git_repo = EngineGitRepo.from_input(obj.get(Y_SCRIPTS_GIT_REPO))
            _user_settings_git_repo = EngineGitRepo.from_input(obj.get(Y_USER_SETTINGS_GIT_REPO))
            _certificate_git_repo = EngineGitRepo.from_input(obj.get(Y_CERTIFICATE_GIT_REPO))
            _identity_git_repo = EngineGitRepo.from_input(obj.get(Y_IDENTITY_GIT_REPO))
            _python = EngineConfigPython.from_input(obj.get(Y_PYTHON))
            _aiEngine = DeploymentConfig.from_input(obj.get(Y_AIENGINE))
            _artifactServer = ImageConfig.from_input(obj.get(Y_ARTIFACTSERVER))
            _bootstrapServer = ImageConfig.from_input(obj.get(Y_BOOTSTRAPSERVER))
            _certChecker = ImageConfig.from_input(obj.get(Y_CERTCHECKER))
            _cx = ImageConfig.from_input(obj.get(Y_CX))
            _cxdp = ImageConfig.from_input(obj.get(Y_CXDP))
            _clusterManager = ImageConfig.from_input(obj.get(Y_CLUSTERMANAGER))
            _vCluster = VClusterOptions.from_input(obj.get(Y_VCLUSTER))
            _npp = ImageConfig.from_input(obj.get(Y_NPP))
            _metricsServer = ImageConfig.from_input(obj.get(Y_METRICSSERVER))
            _stateController = ImageConfig.from_input(obj.get(Y_STATECONTROLLER))
            _stateAggregator = DeploymentConfig.from_input(obj.get(Y_STATEAGGREGATOR))
            _stateEngine = SEDeploymentConfig.from_input(obj.get(Y_STATEENGINE))
            _flowEngine = ImageConfig.from_input(obj.get(Y_FLOWENGINE))
            _appStore = ImageConfig.from_input(obj.get(Y_APPSTORE))
            _appStoreDocs = ImageConfig.from_input(obj.get(Y_APPSTOREDOCS))
            _appStoreFlow = ImageConfig.from_input(obj.get(Y_APPSTOREFLOW))
            _api = APIDeploymentConfig.from_input(obj.get(Y_API))
            _testMan = ImageConfig.from_input(obj.get(Y_TESTMAN))
            _identity = DeploymentConfig.from_input(obj.get(Y_IDENTITY))
            _identitydb = DeploymentConfig.from_input(obj.get(Y_IDENTITYDB))
            _llm = LLM.from_input(obj.get(Y_LLM))
            _simulateNodeLabelSelector = obj.get(Y_SIMULATENODELABELSELECTOR)
            _singleStackServices = obj.get(Y_SINGLESTACKSERVICES)
            _nppNodeLabelSelector = obj.get(Y_NPPNODELABELSELECTOR)
            _kubernetes = Kubernetes.from_input(obj.get(Y_KUBERNETES))
            _customSettings = []
            if obj.get(Y_CUSTOMSETTINGS) is not None:
                for x in obj.get(Y_CUSTOMSETTINGS):
                    _customSettings.append(CustomApplicationSettings.from_input(x))
            _cxCluster = CxCluster.from_input(obj.get(Y_CXCLUSTER))
            _internalCertDuration = obj.get(Y_INTERNALCERTDURATION, "720h")
            _internalCertRenewBefore = obj.get(Y_INTERNALCERTRENEWBEFORE, "240h")
            _internalCertExcludeSingleLabelNames = obj.get(Y_INTERNALCERTEXCLUDESINGLELABELNAMES)
            _logging = LoggingOptions.from_input(obj.get(Y_LOGGING))
            return EngineConfigSpec(
                simulate=_simulate,
                branchInstance=_branchInstance,
                branchOptions=_branchOptions,
                allocationPools=_allocationPools,
                git=_git,
                cluster=_cluster,
                checkpoint_git_repo=_checkpoint_git_repo,
                scripts_git_repo=_scripts_git_repo,
                user_settings_git_repo=_user_settings_git_repo,
                certificate_git_repo=_certificate_git_repo,
                identity_git_repo=_identity_git_repo,
                python=_python,
                aiEngine=_aiEngine,
                artifactServer=_artifactServer,
                bootstrapServer=_bootstrapServer,
                certChecker=_certChecker,
                cx=_cx,
                cxdp=_cxdp,
                clusterManager=_clusterManager,
                vCluster=_vCluster,
                npp=_npp,
                metricsServer=_metricsServer,
                stateController=_stateController,
                stateAggregator=_stateAggregator,
                stateEngine=_stateEngine,
                flowEngine=_flowEngine,
                appStore=_appStore,
                appStoreDocs=_appStoreDocs,
                appStoreFlow=_appStoreFlow,
                api=_api,
                testMan=_testMan,
                identity=_identity,
                identitydb=_identitydb,
                llm=_llm,
                simulateNodeLabelSelector=_simulateNodeLabelSelector,
                singleStackServices=_singleStackServices,
                nppNodeLabelSelector=_nppNodeLabelSelector,
                kubernetes=_kubernetes,
                customSettings=_customSettings,
                cxCluster=_cxCluster,
                internalCertDuration=_internalCertDuration,
                internalCertRenewBefore=_internalCertRenewBefore,
                internalCertExcludeSingleLabelNames=_internalCertExcludeSingleLabelNames,
                logging=_logging,
            )
        return None  # pragma: no cover


class EngineLicenseStatus:
    def __init__(
        self,
        licensedState: str | None = None,
        expirationDate: str | None = None,
        activeLicense: str | None = None,
    ):
        self.licensedState = licensedState
        self.expirationDate = expirationDate
        self.activeLicense = activeLicense

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.licensedState is not None:
            _rval[Y_LICENSEDSTATE] = self.licensedState
        if self.expirationDate is not None:
            _rval[Y_EXPIRATIONDATE] = self.expirationDate
        if self.activeLicense is not None:
            _rval[Y_ACTIVELICENSE] = self.activeLicense
        return _rval

    @staticmethod
    def from_input(obj) -> 'EngineLicenseStatus | None':
        if obj:
            _licensedState = obj.get(Y_LICENSEDSTATE)
            _expirationDate = obj.get(Y_EXPIRATIONDATE)
            _activeLicense = obj.get(Y_ACTIVELICENSE)
            return EngineLicenseStatus(
                licensedState=_licensedState,
                expirationDate=_expirationDate,
                activeLicense=_activeLicense,
            )
        return None  # pragma: no cover


class GitServerStatus:
    def __init__(
        self,
        name: str,
        status: str | None = None,
    ):
        self.name = name
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.name is not None:
            _rval[Y_NAME] = self.name
        if self.status is not None:
            _rval[Y_STATUS] = self.status
        return _rval

    @staticmethod
    def from_input(obj) -> 'GitServerStatus | None':
        if obj:
            _name = obj.get(Y_NAME)
            _status = obj.get(Y_STATUS)
            return GitServerStatus(
                name=_name,
                status=_status,
            )
        return None  # pragma: no cover


class GitStatus:
    def __init__(
        self,
        servers: list[GitServerStatus] | None = None,
    ):
        self.servers = servers

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.servers is not None:
            _rval[Y_SERVERS] = [x.to_input() for x in self.servers]
        return _rval

    @staticmethod
    def from_input(obj) -> 'GitStatus | None':
        if obj:
            _servers = []
            if obj.get(Y_SERVERS) is not None:
                for x in obj.get(Y_SERVERS):
                    _servers.append(GitServerStatus.from_input(x))
            return GitStatus(
                servers=_servers,
            )
        return None  # pragma: no cover


class EngineConfigStatus:
    def __init__(
        self,
        run_status: str | None = None,
        activityState: str | None = None,
        git: GitStatus | None = None,
        cluster: ClusterStatus | None = None,
        licenses: EngineLicenseStatus | None = None,
    ):
        self.run_status = run_status
        self.activityState = activityState
        self.git = git
        self.cluster = cluster
        self.licenses = licenses

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.run_status is not None:
            _rval[Y_RUN_STATUS] = self.run_status
        if self.activityState is not None:
            _rval[Y_ACTIVITYSTATE] = self.activityState
        if self.git is not None:
            _rval[Y_GIT] = self.git.to_input()
        if self.cluster is not None:
            _rval[Y_CLUSTER] = self.cluster.to_input()
        if self.licenses is not None:
            _rval[Y_LICENSES] = self.licenses.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'EngineConfigStatus | None':
        if obj:
            _run_status = obj.get(Y_RUN_STATUS)
            _activityState = obj.get(Y_ACTIVITYSTATE)
            _git = GitStatus.from_input(obj.get(Y_GIT))
            _cluster = ClusterStatus.from_input(obj.get(Y_CLUSTER))
            _licenses = EngineLicenseStatus.from_input(obj.get(Y_LICENSES))
            return EngineConfigStatus(
                run_status=_run_status,
                activityState=_activityState,
                git=_git,
                cluster=_cluster,
                licenses=_licenses,
            )
        return None  # pragma: no cover


class EngineIntentGroupVersionKind:
    def __init__(
        self,
        version: str,
        kind: str,
        group: str | None = None,
    ):
        self.version = version
        self.kind = kind
        self.group = group

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.version is not None:
            _rval[Y_VERSION] = self.version
        if self.kind is not None:
            _rval[Y_KIND] = self.kind
        if self.group is not None:
            _rval[Y_GROUP] = self.group
        return _rval

    @staticmethod
    def from_input(obj) -> 'EngineIntentGroupVersionKind | None':
        if obj:
            _version = obj.get(Y_VERSION)
            _kind = obj.get(Y_KIND)
            _group = obj.get(Y_GROUP)
            return EngineIntentGroupVersionKind(
                version=_version,
                kind=_kind,
                group=_group,
            )
        return None  # pragma: no cover


class GitRepository:
    def __init__(
        self,
        repository: str,
    ):
        self.repository = repository

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.repository is not None:
            _rval[Y_REPOSITORY] = self.repository
        return _rval

    @staticmethod
    def from_input(obj) -> 'GitRepository | None':
        if obj:
            _repository = obj.get(Y_REPOSITORY)
            return GitRepository(
                repository=_repository,
            )
        return None  # pragma: no cover


class ServiceConfig:
    def __init__(
        self,
        enableLoadBalancerNodePorts: bool | None = None,
        serviceType: str | None = None,
    ):
        self.enableLoadBalancerNodePorts = enableLoadBalancerNodePorts
        self.serviceType = serviceType

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.enableLoadBalancerNodePorts is not None:
            _rval[Y_ENABLELOADBALANCERNODEPORTS] = self.enableLoadBalancerNodePorts
        if self.serviceType is not None:
            _rval[Y_SERVICETYPE] = self.serviceType
        return _rval

    @staticmethod
    def from_input(obj) -> 'ServiceConfig | None':
        if obj:
            _enableLoadBalancerNodePorts = obj.get(Y_ENABLELOADBALANCERNODEPORTS)
            _serviceType = obj.get(Y_SERVICETYPE, "LoadBalancer")
            return ServiceConfig(
                enableLoadBalancerNodePorts=_enableLoadBalancerNodePorts,
                serviceType=_serviceType,
            )
        return None  # pragma: no cover


class EngineConfig:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: EngineConfigSpec | None = None,
        status: EngineConfigStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = ENGINECONFIG_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'EngineConfig | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = EngineConfigSpec.from_input(obj.get(Y_SPEC, None))
            _status = EngineConfigStatus.from_input(obj.get(Y_STATUS))
            return EngineConfig(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class EngineConfigList:
    def __init__(
        self,
        items: list[EngineConfig],
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
    def from_input(obj) -> 'EngineConfigList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return EngineConfigList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
