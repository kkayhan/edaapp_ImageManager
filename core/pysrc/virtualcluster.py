#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
Y_KUBECONFIGSECRET = 'kubeconfigSecret'
Y_TARGETBRANCH = 'targetBranch'
Y_PHASE = 'phase'
Y_CONDITIONS = 'conditions'
Y_OBSERVEDGENERATION = 'observedGeneration'
Y_NAMESPACE = 'namespace'
Y_SERVICEURL = 'serviceUrl'
Y_VCLUSTERCLIENTREADY = 'vclusterClientReady'
Y_RESOURCES = 'resources'
Y_MESSAGE = 'message'
Y_LASTRECONCILETIME = 'lastReconcileTime'
Y_FAILURECOUNT = 'failureCount'
Y_HEALTHCHECKTIME = 'healthCheckTime'
Y_TARGETCLUSTERNAMESPACE = 'targetClusterNamespace'
Y_CLUSTERROLES = 'clusterRoles'
Y_CLUSTERROLEBINDINGS = 'clusterRoleBindings'
Y_SERVICEACCOUNTS = 'serviceAccounts'
Y_DEPLOYMENTS = 'deployments'
Y_STATEFULSETS = 'statefulSets'
Y_SERVICES = 'services'
# Package objects (GVK Schemas)
VIRTUALCLUSTER_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='VirtualCluster')


class BranchRef:
    def __init__(
        self,
        kubeconfigSecret: str,
    ):
        self.kubeconfigSecret = kubeconfigSecret

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.kubeconfigSecret is not None:
            _rval[Y_KUBECONFIGSECRET] = self.kubeconfigSecret
        return _rval

    @staticmethod
    def from_input(obj) -> 'BranchRef | None':
        if obj:
            _kubeconfigSecret = obj.get(Y_KUBECONFIGSECRET)
            return BranchRef(
                kubeconfigSecret=_kubeconfigSecret,
            )
        return None  # pragma: no cover


class TrackedResources:
    def __init__(
        self,
        clusterRoles: list[str] | None = None,
        clusterRoleBindings: list[str] | None = None,
        serviceAccounts: list[str] | None = None,
        deployments: list[str] | None = None,
        statefulSets: list[str] | None = None,
        services: list[str] | None = None,
    ):
        self.clusterRoles = clusterRoles
        self.clusterRoleBindings = clusterRoleBindings
        self.serviceAccounts = serviceAccounts
        self.deployments = deployments
        self.statefulSets = statefulSets
        self.services = services

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.clusterRoles is not None:
            _rval[Y_CLUSTERROLES] = self.clusterRoles
        if self.clusterRoleBindings is not None:
            _rval[Y_CLUSTERROLEBINDINGS] = self.clusterRoleBindings
        if self.serviceAccounts is not None:
            _rval[Y_SERVICEACCOUNTS] = self.serviceAccounts
        if self.deployments is not None:
            _rval[Y_DEPLOYMENTS] = self.deployments
        if self.statefulSets is not None:
            _rval[Y_STATEFULSETS] = self.statefulSets
        if self.services is not None:
            _rval[Y_SERVICES] = self.services
        return _rval

    @staticmethod
    def from_input(obj) -> 'TrackedResources | None':
        if obj:
            _clusterRoles = obj.get(Y_CLUSTERROLES)
            _clusterRoleBindings = obj.get(Y_CLUSTERROLEBINDINGS)
            _serviceAccounts = obj.get(Y_SERVICEACCOUNTS)
            _deployments = obj.get(Y_DEPLOYMENTS)
            _statefulSets = obj.get(Y_STATEFULSETS)
            _services = obj.get(Y_SERVICES)
            return TrackedResources(
                clusterRoles=_clusterRoles,
                clusterRoleBindings=_clusterRoleBindings,
                serviceAccounts=_serviceAccounts,
                deployments=_deployments,
                statefulSets=_statefulSets,
                services=_services,
            )
        return None  # pragma: no cover


class VirtualClusterSpec:
    def __init__(
        self,
        targetBranch: BranchRef | None = None,
    ):
        self.targetBranch = targetBranch

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.targetBranch is not None:
            _rval[Y_TARGETBRANCH] = self.targetBranch.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'VirtualClusterSpec | None':
        if obj:
            _targetBranch = BranchRef.from_input(obj.get(Y_TARGETBRANCH))
            return VirtualClusterSpec(
                targetBranch=_targetBranch,
            )
        return None  # pragma: no cover


class VirtualClusterStatus:
    def __init__(
        self,
        phase: str | None = None,
        conditions: list[object] | None = None,
        observedGeneration: int | None = None,
        namespace: str | None = None,
        serviceUrl: str | None = None,
        kubeconfigSecret: str | None = None,
        vclusterClientReady: bool | None = None,
        resources: TrackedResources | None = None,
        message: str | None = None,
        lastReconcileTime: object | None = None,
        failureCount: int | None = None,
        healthCheckTime: object | None = None,
        targetClusterNamespace: str | None = None,
    ):
        self.phase = phase
        self.conditions = conditions
        self.observedGeneration = observedGeneration
        self.namespace = namespace
        self.serviceUrl = serviceUrl
        self.kubeconfigSecret = kubeconfigSecret
        self.vclusterClientReady = vclusterClientReady
        self.resources = resources
        self.message = message
        self.lastReconcileTime = lastReconcileTime
        self.failureCount = failureCount
        self.healthCheckTime = healthCheckTime
        self.targetClusterNamespace = targetClusterNamespace

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.phase is not None:
            _rval[Y_PHASE] = self.phase
        if self.conditions is not None:
            _rval[Y_CONDITIONS] = self.conditions
        if self.observedGeneration is not None:
            _rval[Y_OBSERVEDGENERATION] = self.observedGeneration
        if self.namespace is not None:
            _rval[Y_NAMESPACE] = self.namespace
        if self.serviceUrl is not None:
            _rval[Y_SERVICEURL] = self.serviceUrl
        if self.kubeconfigSecret is not None:
            _rval[Y_KUBECONFIGSECRET] = self.kubeconfigSecret
        if self.vclusterClientReady is not None:
            _rval[Y_VCLUSTERCLIENTREADY] = self.vclusterClientReady
        if self.resources is not None:
            _rval[Y_RESOURCES] = self.resources.to_input()
        if self.message is not None:
            _rval[Y_MESSAGE] = self.message
        if self.lastReconcileTime is not None:
            _rval[Y_LASTRECONCILETIME] = self.lastReconcileTime
        if self.failureCount is not None:
            _rval[Y_FAILURECOUNT] = self.failureCount
        if self.healthCheckTime is not None:
            _rval[Y_HEALTHCHECKTIME] = self.healthCheckTime
        if self.targetClusterNamespace is not None:
            _rval[Y_TARGETCLUSTERNAMESPACE] = self.targetClusterNamespace
        return _rval

    @staticmethod
    def from_input(obj) -> 'VirtualClusterStatus | None':
        if obj:
            _phase = obj.get(Y_PHASE)
            _conditions = obj.get(Y_CONDITIONS)
            _observedGeneration = obj.get(Y_OBSERVEDGENERATION)
            _namespace = obj.get(Y_NAMESPACE)
            _serviceUrl = obj.get(Y_SERVICEURL)
            _kubeconfigSecret = obj.get(Y_KUBECONFIGSECRET)
            _vclusterClientReady = obj.get(Y_VCLUSTERCLIENTREADY)
            _resources = TrackedResources.from_input(obj.get(Y_RESOURCES))
            _message = obj.get(Y_MESSAGE)
            _lastReconcileTime = obj.get(Y_LASTRECONCILETIME)
            _failureCount = obj.get(Y_FAILURECOUNT)
            _healthCheckTime = obj.get(Y_HEALTHCHECKTIME)
            _targetClusterNamespace = obj.get(Y_TARGETCLUSTERNAMESPACE)
            return VirtualClusterStatus(
                phase=_phase,
                conditions=_conditions,
                observedGeneration=_observedGeneration,
                namespace=_namespace,
                serviceUrl=_serviceUrl,
                kubeconfigSecret=_kubeconfigSecret,
                vclusterClientReady=_vclusterClientReady,
                resources=_resources,
                message=_message,
                lastReconcileTime=_lastReconcileTime,
                failureCount=_failureCount,
                healthCheckTime=_healthCheckTime,
                targetClusterNamespace=_targetClusterNamespace,
            )
        return None  # pragma: no cover


class VirtualCluster:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: VirtualClusterSpec | None = None,
        status: VirtualClusterStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = VIRTUALCLUSTER_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'VirtualCluster | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = VirtualClusterSpec.from_input(obj.get(Y_SPEC, None))
            _status = VirtualClusterStatus.from_input(obj.get(Y_STATUS))
            return VirtualCluster(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class VirtualClusterList:
    def __init__(
        self,
        items: list[VirtualCluster],
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
    def from_input(obj) -> 'VirtualClusterList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return VirtualClusterList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
