#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
Y_DEFAULTARTIFACTNAMESPACE = 'defaultArtifactNamespace'
Y_DEFAULTREPO = 'defaultRepo'
Y_MAXUPLOADMIB = 'maxUploadMiB'
Y_FILEPULLBASEURL = 'filePullBaseUrl'
Y_RETENTIONDAYS = 'retentionDays'
Y_HEALTH = 'health'
Y_MESSAGE = 'message'
Y_LASTRECONCILETIME = 'lastReconcileTime'
Y_UPLOADSSTORED = 'uploadsStored'
Y_BYTESSTORED = 'bytesStored'
Y_ARTIFACTS = 'artifacts'
Y_VERSION = 'version'
Y_NAMESPACE = 'namespace'
Y_REPO = 'repo'
Y_FILEPATH = 'filePath'
Y_DOWNLOADSTATUS = 'downloadStatus'
Y_STATUSREASON = 'statusReason'
Y_EXTERNALURL = 'externalUrl'
# Package objects (GVK Schemas)
IMAGEMANAGERCONFIG_SCHEMA = eda.Schema(group='imagemanager.eda.edacommunity.com', version='v1alpha1', kind='ImageManagerConfig')


class ImageManagerConfigSpec:
    def __init__(
        self,
        defaultArtifactNamespace: str | None = None,
        defaultRepo: str | None = None,
        maxUploadMiB: int | None = None,
        filePullBaseUrl: str | None = None,
        retentionDays: int | None = None,
    ):
        self.defaultArtifactNamespace = defaultArtifactNamespace
        self.defaultRepo = defaultRepo
        self.maxUploadMiB = maxUploadMiB
        self.filePullBaseUrl = filePullBaseUrl
        self.retentionDays = retentionDays

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.defaultArtifactNamespace is not None:
            _rval[Y_DEFAULTARTIFACTNAMESPACE] = self.defaultArtifactNamespace
        if self.defaultRepo is not None:
            _rval[Y_DEFAULTREPO] = self.defaultRepo
        if self.maxUploadMiB is not None:
            _rval[Y_MAXUPLOADMIB] = self.maxUploadMiB
        if self.filePullBaseUrl is not None:
            _rval[Y_FILEPULLBASEURL] = self.filePullBaseUrl
        if self.retentionDays is not None:
            _rval[Y_RETENTIONDAYS] = self.retentionDays
        return _rval

    @staticmethod
    def from_input(obj) -> 'ImageManagerConfigSpec | None':
        if obj:
            _defaultArtifactNamespace = obj.get(Y_DEFAULTARTIFACTNAMESPACE, "eda")
            _defaultRepo = obj.get(Y_DEFAULTREPO, "images")
            _maxUploadMiB = obj.get(Y_MAXUPLOADMIB, 4096)
            _filePullBaseUrl = obj.get(Y_FILEPULLBASEURL)
            _retentionDays = obj.get(Y_RETENTIONDAYS, 0)
            return ImageManagerConfigSpec(
                defaultArtifactNamespace=_defaultArtifactNamespace,
                defaultRepo=_defaultRepo,
                maxUploadMiB=_maxUploadMiB,
                filePullBaseUrl=_filePullBaseUrl,
                retentionDays=_retentionDays,
            )
        return None  # pragma: no cover


class TrackedArtifact:
    def __init__(
        self,
        name: str,
        namespace: str,
        repo: str,
        filePath: str,
        downloadStatus: str | None = None,
        statusReason: str | None = None,
        externalUrl: str | None = None,
    ):
        self.name = name
        self.namespace = namespace
        self.repo = repo
        self.filePath = filePath
        self.downloadStatus = downloadStatus
        self.statusReason = statusReason
        self.externalUrl = externalUrl

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.name is not None:
            _rval[Y_NAME] = self.name
        if self.namespace is not None:
            _rval[Y_NAMESPACE] = self.namespace
        if self.repo is not None:
            _rval[Y_REPO] = self.repo
        if self.filePath is not None:
            _rval[Y_FILEPATH] = self.filePath
        if self.downloadStatus is not None:
            _rval[Y_DOWNLOADSTATUS] = self.downloadStatus
        if self.statusReason is not None:
            _rval[Y_STATUSREASON] = self.statusReason
        if self.externalUrl is not None:
            _rval[Y_EXTERNALURL] = self.externalUrl
        return _rval

    @staticmethod
    def from_input(obj) -> 'TrackedArtifact | None':
        if obj:
            _name = obj.get(Y_NAME)
            _namespace = obj.get(Y_NAMESPACE)
            _repo = obj.get(Y_REPO)
            _filePath = obj.get(Y_FILEPATH)
            _downloadStatus = obj.get(Y_DOWNLOADSTATUS)
            _statusReason = obj.get(Y_STATUSREASON)
            _externalUrl = obj.get(Y_EXTERNALURL)
            return TrackedArtifact(
                name=_name,
                namespace=_namespace,
                repo=_repo,
                filePath=_filePath,
                downloadStatus=_downloadStatus,
                statusReason=_statusReason,
                externalUrl=_externalUrl,
            )
        return None  # pragma: no cover


class ImageManagerConfigStatus:
    def __init__(
        self,
        health: str | None = None,
        message: str | None = None,
        lastReconcileTime: str | None = None,
        uploadsStored: int | None = None,
        bytesStored: int | None = None,
        artifacts: list[TrackedArtifact] | None = None,
        version: str | None = None,
    ):
        self.health = health
        self.message = message
        self.lastReconcileTime = lastReconcileTime
        self.uploadsStored = uploadsStored
        self.bytesStored = bytesStored
        self.artifacts = artifacts
        self.version = version

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.health is not None:
            _rval[Y_HEALTH] = self.health
        if self.message is not None:
            _rval[Y_MESSAGE] = self.message
        if self.lastReconcileTime is not None:
            _rval[Y_LASTRECONCILETIME] = self.lastReconcileTime
        if self.uploadsStored is not None:
            _rval[Y_UPLOADSSTORED] = self.uploadsStored
        if self.bytesStored is not None:
            _rval[Y_BYTESSTORED] = self.bytesStored
        if self.artifacts is not None:
            _rval[Y_ARTIFACTS] = [x.to_input() for x in self.artifacts]
        if self.version is not None:
            _rval[Y_VERSION] = self.version
        return _rval

    @staticmethod
    def from_input(obj) -> 'ImageManagerConfigStatus | None':
        if obj:
            _health = obj.get(Y_HEALTH)
            _message = obj.get(Y_MESSAGE)
            _lastReconcileTime = obj.get(Y_LASTRECONCILETIME)
            _uploadsStored = obj.get(Y_UPLOADSSTORED)
            _bytesStored = obj.get(Y_BYTESSTORED)
            _artifacts = []
            if obj.get(Y_ARTIFACTS) is not None:
                for x in obj.get(Y_ARTIFACTS):
                    _artifacts.append(TrackedArtifact.from_input(x))
            _version = obj.get(Y_VERSION)
            return ImageManagerConfigStatus(
                health=_health,
                message=_message,
                lastReconcileTime=_lastReconcileTime,
                uploadsStored=_uploadsStored,
                bytesStored=_bytesStored,
                artifacts=_artifacts,
                version=_version,
            )
        return None  # pragma: no cover


class ImageManagerConfig:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: ImageManagerConfigSpec | None = None,
        status: ImageManagerConfigStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = IMAGEMANAGERCONFIG_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'ImageManagerConfig | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = ImageManagerConfigSpec.from_input(obj.get(Y_SPEC, None))
            _status = ImageManagerConfigStatus.from_input(obj.get(Y_STATUS))
            return ImageManagerConfig(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class ImageManagerConfigList:
    def __init__(
        self,
        items: list[ImageManagerConfig],
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
    def from_input(obj) -> 'ImageManagerConfigList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return ImageManagerConfigList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
