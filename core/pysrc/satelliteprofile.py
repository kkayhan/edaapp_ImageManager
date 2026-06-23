#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
from .nodeprofile import Image
Y_OPERATINGSYSTEM = 'operatingSystem'
Y_VERSION = 'version'
Y_IMAGES = 'images'
Y_VERSIONPATH = 'versionPath'
Y_VERSIONMATCH = 'versionMatch'
Y_SERIALNUMBERPATH = 'serialNumberPath'
Y_PLATFORMPATH = 'platformPath'
Y_CONTAINERIMAGE = 'containerImage'
Y_IMAGEPULLSECRET = 'imagePullSecret'
Y_LICENSE = 'license'
# Package objects (GVK Schemas)
SATELLITEPROFILE_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='SatelliteProfile')


class SatelliteProfileSpec:
    def __init__(
        self,
        operatingSystem: str,
        version: str,
        versionPath: str,
        serialNumberPath: str,
        images: list[Image] | None = None,
        versionMatch: str | None = None,
        platformPath: str | None = None,
        containerImage: str | None = None,
        imagePullSecret: str | None = None,
        license: str | None = None,
    ):
        self.operatingSystem = operatingSystem
        self.version = version
        self.versionPath = versionPath
        self.serialNumberPath = serialNumberPath
        self.images = images
        self.versionMatch = versionMatch
        self.platformPath = platformPath
        self.containerImage = containerImage
        self.imagePullSecret = imagePullSecret
        self.license = license

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.operatingSystem is not None:
            _rval[Y_OPERATINGSYSTEM] = self.operatingSystem
        if self.version is not None:
            _rval[Y_VERSION] = self.version
        if self.versionPath is not None:
            _rval[Y_VERSIONPATH] = self.versionPath
        if self.serialNumberPath is not None:
            _rval[Y_SERIALNUMBERPATH] = self.serialNumberPath
        if self.images is not None:
            _rval[Y_IMAGES] = [x.to_input() for x in self.images]
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
        return _rval

    @staticmethod
    def from_input(obj) -> 'SatelliteProfileSpec | None':
        if obj:
            _operatingSystem = obj.get(Y_OPERATINGSYSTEM)
            _version = obj.get(Y_VERSION)
            _versionPath = obj.get(Y_VERSIONPATH)
            _serialNumberPath = obj.get(Y_SERIALNUMBERPATH)
            _images = []
            if obj.get(Y_IMAGES) is not None:
                for x in obj.get(Y_IMAGES):
                    _images.append(Image.from_input(x))
            _versionMatch = obj.get(Y_VERSIONMATCH)
            _platformPath = obj.get(Y_PLATFORMPATH)
            _containerImage = obj.get(Y_CONTAINERIMAGE)
            _imagePullSecret = obj.get(Y_IMAGEPULLSECRET)
            _license = obj.get(Y_LICENSE)
            return SatelliteProfileSpec(
                operatingSystem=_operatingSystem,
                version=_version,
                versionPath=_versionPath,
                serialNumberPath=_serialNumberPath,
                images=_images,
                versionMatch=_versionMatch,
                platformPath=_platformPath,
                containerImage=_containerImage,
                imagePullSecret=_imagePullSecret,
                license=_license,
            )
        return None  # pragma: no cover


class SatelliteProfileStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'SatelliteProfileStatus | None':
        if obj:
            return SatelliteProfileStatus(
            )
        return None  # pragma: no cover


class SatelliteProfile:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: SatelliteProfileSpec | None = None,
        status: SatelliteProfileStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = SATELLITEPROFILE_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'SatelliteProfile | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = SatelliteProfileSpec.from_input(obj.get(Y_SPEC, None))
            _status = SatelliteProfileStatus.from_input(obj.get(Y_STATUS))
            return SatelliteProfile(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class SatelliteProfileList:
    def __init__(
        self,
        items: list[SatelliteProfile],
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
    def from_input(obj) -> 'SatelliteProfileList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return SatelliteProfileList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
