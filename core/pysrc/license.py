#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
Y_ENABLED = 'enabled'
Y_DATA = 'data'
Y_VALID = 'valid'
Y_USED = 'used'
Y_ISSUEDDATE = 'issuedDate'
Y_STARTDATE = 'startDate'
Y_EXPIRED = 'expired'
Y_EXPIRATIONDATE = 'expirationDate'
Y_COMMENT = 'comment'
# Package objects (GVK Schemas)
LICENSE_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='License')


class LicenseSpec:
    def __init__(
        self,
        enabled: bool,
        data: str,
    ):
        self.enabled = enabled
        self.data = data

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.enabled is not None:
            _rval[Y_ENABLED] = self.enabled
        if self.data is not None:
            _rval[Y_DATA] = self.data
        return _rval

    @staticmethod
    def from_input(obj) -> 'LicenseSpec | None':
        if obj:
            _enabled = obj.get(Y_ENABLED, True)
            _data = obj.get(Y_DATA)
            return LicenseSpec(
                enabled=_enabled,
                data=_data,
            )
        return None  # pragma: no cover


class LicenseStatus:
    def __init__(
        self,
        valid: bool,
        used: bool,
        expired: bool,
        issuedDate: str | None = None,
        startDate: str | None = None,
        expirationDate: str | None = None,
        comment: str | None = None,
    ):
        self.valid = valid
        self.used = used
        self.expired = expired
        self.issuedDate = issuedDate
        self.startDate = startDate
        self.expirationDate = expirationDate
        self.comment = comment

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.valid is not None:
            _rval[Y_VALID] = self.valid
        if self.used is not None:
            _rval[Y_USED] = self.used
        if self.expired is not None:
            _rval[Y_EXPIRED] = self.expired
        if self.issuedDate is not None:
            _rval[Y_ISSUEDDATE] = self.issuedDate
        if self.startDate is not None:
            _rval[Y_STARTDATE] = self.startDate
        if self.expirationDate is not None:
            _rval[Y_EXPIRATIONDATE] = self.expirationDate
        if self.comment is not None:
            _rval[Y_COMMENT] = self.comment
        return _rval

    @staticmethod
    def from_input(obj) -> 'LicenseStatus | None':
        if obj:
            _valid = obj.get(Y_VALID)
            _used = obj.get(Y_USED)
            _expired = obj.get(Y_EXPIRED)
            _issuedDate = obj.get(Y_ISSUEDDATE)
            _startDate = obj.get(Y_STARTDATE)
            _expirationDate = obj.get(Y_EXPIRATIONDATE)
            _comment = obj.get(Y_COMMENT)
            return LicenseStatus(
                valid=_valid,
                used=_used,
                expired=_expired,
                issuedDate=_issuedDate,
                startDate=_startDate,
                expirationDate=_expirationDate,
                comment=_comment,
            )
        return None  # pragma: no cover


class License:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: LicenseSpec | None = None,
        status: LicenseStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = LICENSE_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'License | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = LicenseSpec.from_input(obj.get(Y_SPEC, None))
            _status = LicenseStatus.from_input(obj.get(Y_STATUS))
            return License(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class LicenseList:
    def __init__(
        self,
        items: list[License],
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
    def from_input(obj) -> 'LicenseList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return LicenseList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
