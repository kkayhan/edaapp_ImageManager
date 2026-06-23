#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *

ENUM_SHAREDIPSERVICEPORTPROTOCOL_TCP = 'TCP'
ENUM_SHAREDIPSERVICEPORTPROTOCOL_UDP = 'UDP'
ENUM_SHAREDIPSERVICEPORTPROTOCOL_SCTP = 'SCTP'
Y_PROTOCOL = 'protocol'
Y_PORT = 'port'
Y_TARGETPORT = 'targetPort'
Y_PODLABEL = 'podLabel'
Y_PORTS = 'ports'
Y_SERVICENAME = 'serviceName'
Y_SERVICENAMESPACE = 'serviceNamespace'
Y_ASSIGNEDIP = 'assignedIP'
Y_ALLOCATEDPORTS = 'allocatedPorts'
Y_OBSERVEDGENERATION = 'observedGeneration'
# Package objects (GVK Schemas)
SHAREDIPSERVICE_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='SharedIpService')


class AllocatedPortStatus:
    def __init__(
        self,
        name: str,
        port: int,
        protocol: object,
    ):
        self.name = name
        self.port = port
        self.protocol = protocol

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.name is not None:
            _rval[Y_NAME] = self.name
        if self.port is not None:
            _rval[Y_PORT] = self.port
        if self.protocol is not None:
            _rval[Y_PROTOCOL] = self.protocol
        return _rval

    @staticmethod
    def from_input(obj) -> 'AllocatedPortStatus | None':
        if obj:
            _name = obj.get(Y_NAME)
            _port = obj.get(Y_PORT)
            _protocol = obj.get(Y_PROTOCOL)
            return AllocatedPortStatus(
                name=_name,
                port=_port,
                protocol=_protocol,
            )
        return None  # pragma: no cover


class SharedIpServicePort:
    def __init__(
        self,
        port: int,
        name: str | None = None,
        protocol: object | None = None,
        targetPort: int | None = None,
    ):
        self.port = port
        self.name = name
        self.protocol = protocol
        self.targetPort = targetPort

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.port is not None:
            _rval[Y_PORT] = self.port
        if self.name is not None:
            _rval[Y_NAME] = self.name
        if self.protocol is not None:
            _rval[Y_PROTOCOL] = self.protocol
        if self.targetPort is not None:
            _rval[Y_TARGETPORT] = self.targetPort
        return _rval

    @staticmethod
    def from_input(obj) -> 'SharedIpServicePort | None':
        if obj:
            _port = obj.get(Y_PORT)
            _name = obj.get(Y_NAME)
            _protocol = obj.get(Y_PROTOCOL, "TCP")
            _targetPort = obj.get(Y_TARGETPORT)
            return SharedIpServicePort(
                port=_port,
                name=_name,
                protocol=_protocol,
                targetPort=_targetPort,
            )
        return None  # pragma: no cover


class SharedIpServiceSpec:
    def __init__(
        self,
        podLabel: dict[str, str],
        ports: list[SharedIpServicePort],
        serviceName: str | None = None,
        serviceNamespace: str | None = None,
    ):
        self.podLabel = podLabel
        self.ports = ports
        self.serviceName = serviceName
        self.serviceNamespace = serviceNamespace

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.podLabel is not None:
            _rval[Y_PODLABEL] = self.podLabel
        if self.ports is not None:
            _rval[Y_PORTS] = [x.to_input() for x in self.ports]
        if self.serviceName is not None:
            _rval[Y_SERVICENAME] = self.serviceName
        if self.serviceNamespace is not None:
            _rval[Y_SERVICENAMESPACE] = self.serviceNamespace
        return _rval

    @staticmethod
    def from_input(obj) -> 'SharedIpServiceSpec | None':
        if obj:
            _podLabel = obj.get(Y_PODLABEL)
            _ports = []
            if obj.get(Y_PORTS) is not None:
                for x in obj.get(Y_PORTS):
                    _ports.append(SharedIpServicePort.from_input(x))
            _serviceName = obj.get(Y_SERVICENAME)
            _serviceNamespace = obj.get(Y_SERVICENAMESPACE)
            return SharedIpServiceSpec(
                podLabel=_podLabel,
                ports=_ports,
                serviceName=_serviceName,
                serviceNamespace=_serviceNamespace,
            )
        return None  # pragma: no cover


class SharedIpServiceStatus:
    def __init__(
        self,
        assignedIP: str | None = None,
        allocatedPorts: list[AllocatedPortStatus] | None = None,
        serviceName: str | None = None,
        observedGeneration: int | None = None,
    ):
        self.assignedIP = assignedIP
        self.allocatedPorts = allocatedPorts
        self.serviceName = serviceName
        self.observedGeneration = observedGeneration

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.assignedIP is not None:
            _rval[Y_ASSIGNEDIP] = self.assignedIP
        if self.allocatedPorts is not None:
            _rval[Y_ALLOCATEDPORTS] = [x.to_input() for x in self.allocatedPorts]
        if self.serviceName is not None:
            _rval[Y_SERVICENAME] = self.serviceName
        if self.observedGeneration is not None:
            _rval[Y_OBSERVEDGENERATION] = self.observedGeneration
        return _rval

    @staticmethod
    def from_input(obj) -> 'SharedIpServiceStatus | None':
        if obj:
            _assignedIP = obj.get(Y_ASSIGNEDIP)
            _allocatedPorts = []
            if obj.get(Y_ALLOCATEDPORTS) is not None:
                for x in obj.get(Y_ALLOCATEDPORTS):
                    _allocatedPorts.append(AllocatedPortStatus.from_input(x))
            _serviceName = obj.get(Y_SERVICENAME)
            _observedGeneration = obj.get(Y_OBSERVEDGENERATION)
            return SharedIpServiceStatus(
                assignedIP=_assignedIP,
                allocatedPorts=_allocatedPorts,
                serviceName=_serviceName,
                observedGeneration=_observedGeneration,
            )
        return None  # pragma: no cover


class SharedIpService:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: SharedIpServiceSpec | None = None,
        status: SharedIpServiceStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = SHAREDIPSERVICE_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'SharedIpService | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = SharedIpServiceSpec.from_input(obj.get(Y_SPEC, None))
            _status = SharedIpServiceStatus.from_input(obj.get(Y_STATUS))
            return SharedIpService(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class SharedIpServiceList:
    def __init__(
        self,
        items: list[SharedIpService],
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
    def from_input(obj) -> 'SharedIpServiceList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return SharedIpServiceList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
