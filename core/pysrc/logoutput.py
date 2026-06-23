#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *

ENUM_SYSLOGMODE_TCP = 'tcp'
ENUM_SYSLOGMODE_UDP = 'udp'
ENUM_SYSLOGMODE_ = ''

ENUM_SYSLOGSYSLOGFORMAT_RFC3164 = 'rfc3164'
ENUM_SYSLOGSYSLOGFORMAT_RFC5424 = 'rfc5424'
ENUM_SYSLOGSYSLOGFORMAT_ = ''
Y_MATCH = 'match'
Y_HOST = 'host'
Y_PORT = 'port'
Y_SKIPVERIFY = 'skipVerify'
Y_CLIENTCERT = 'clientCert'
Y_MODE = 'mode'
Y_SYSLOGFORMAT = 'syslogFormat'
Y_SYSLOGMAXSIZE = 'syslogMaxsize'
Y_SYSLOGSEVERITYKEY = 'syslogSeverityKey'
Y_SYSLOGFACILITYKEY = 'syslogFacilityKey'
Y_SYSLOGHOSTNAMEKEY = 'syslogHostnameKey'
Y_SYSLOGAPPNAMEKEY = 'syslogAppnameKey'
Y_SYSLOGPROCIDKEY = 'syslogProcidKey'
Y_SYSLOGMSGIDKEY = 'syslogMsgidKey'
Y_SYSLOGSDKEY = 'syslogSdKey'
Y_SYSLOGMESSAGEKEY = 'syslogMessageKey'
Y_TLS = 'tls'
Y_FORWARD = 'forward'
Y_SYSLOG = 'syslog'
# Package objects (GVK Schemas)
LOGOUTPUT_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='LogOutput')


class Forward:
    def __init__(
        self,
        match: str | None = None,
        host: str | None = None,
        port: int | None = None,
    ):
        self.match = match
        self.host = host
        self.port = port

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.match is not None:
            _rval[Y_MATCH] = self.match
        if self.host is not None:
            _rval[Y_HOST] = self.host
        if self.port is not None:
            _rval[Y_PORT] = self.port
        return _rval

    @staticmethod
    def from_input(obj) -> 'Forward | None':
        if obj:
            _match = obj.get(Y_MATCH, "*")
            _host = obj.get(Y_HOST)
            _port = obj.get(Y_PORT)
            return Forward(
                match=_match,
                host=_host,
                port=_port,
            )
        return None  # pragma: no cover


class SyslogTLS:
    def __init__(
        self,
        skipVerify: bool | None = None,
        clientCert: bool | None = None,
    ):
        self.skipVerify = skipVerify
        self.clientCert = clientCert

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.skipVerify is not None:
            _rval[Y_SKIPVERIFY] = self.skipVerify
        if self.clientCert is not None:
            _rval[Y_CLIENTCERT] = self.clientCert
        return _rval

    @staticmethod
    def from_input(obj) -> 'SyslogTLS | None':
        if obj:
            _skipVerify = obj.get(Y_SKIPVERIFY, False)
            _clientCert = obj.get(Y_CLIENTCERT, False)
            return SyslogTLS(
                skipVerify=_skipVerify,
                clientCert=_clientCert,
            )
        return None  # pragma: no cover


class Syslog:
    def __init__(
        self,
        host: str,
        match: str | None = None,
        port: int | None = None,
        mode: str | None = None,
        syslogFormat: str | None = None,
        syslogMaxsize: int | None = None,
        syslogSeverityKey: str | None = None,
        syslogFacilityKey: str | None = None,
        syslogHostnameKey: str | None = None,
        syslogAppnameKey: str | None = None,
        syslogProcidKey: str | None = None,
        syslogMsgidKey: str | None = None,
        syslogSdKey: str | None = None,
        syslogMessageKey: str | None = None,
        tls: SyslogTLS | None = None,
    ):
        self.host = host
        self.match = match
        self.port = port
        self.mode = mode
        self.syslogFormat = syslogFormat
        self.syslogMaxsize = syslogMaxsize
        self.syslogSeverityKey = syslogSeverityKey
        self.syslogFacilityKey = syslogFacilityKey
        self.syslogHostnameKey = syslogHostnameKey
        self.syslogAppnameKey = syslogAppnameKey
        self.syslogProcidKey = syslogProcidKey
        self.syslogMsgidKey = syslogMsgidKey
        self.syslogSdKey = syslogSdKey
        self.syslogMessageKey = syslogMessageKey
        self.tls = tls

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.host is not None:
            _rval[Y_HOST] = self.host
        if self.match is not None:
            _rval[Y_MATCH] = self.match
        if self.port is not None:
            _rval[Y_PORT] = self.port
        if self.mode is not None:
            _rval[Y_MODE] = self.mode
        if self.syslogFormat is not None:
            _rval[Y_SYSLOGFORMAT] = self.syslogFormat
        if self.syslogMaxsize is not None:
            _rval[Y_SYSLOGMAXSIZE] = self.syslogMaxsize
        if self.syslogSeverityKey is not None:
            _rval[Y_SYSLOGSEVERITYKEY] = self.syslogSeverityKey
        if self.syslogFacilityKey is not None:
            _rval[Y_SYSLOGFACILITYKEY] = self.syslogFacilityKey
        if self.syslogHostnameKey is not None:
            _rval[Y_SYSLOGHOSTNAMEKEY] = self.syslogHostnameKey
        if self.syslogAppnameKey is not None:
            _rval[Y_SYSLOGAPPNAMEKEY] = self.syslogAppnameKey
        if self.syslogProcidKey is not None:
            _rval[Y_SYSLOGPROCIDKEY] = self.syslogProcidKey
        if self.syslogMsgidKey is not None:
            _rval[Y_SYSLOGMSGIDKEY] = self.syslogMsgidKey
        if self.syslogSdKey is not None:
            _rval[Y_SYSLOGSDKEY] = self.syslogSdKey
        if self.syslogMessageKey is not None:
            _rval[Y_SYSLOGMESSAGEKEY] = self.syslogMessageKey
        if self.tls is not None:
            _rval[Y_TLS] = self.tls.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'Syslog | None':
        if obj:
            _host = obj.get(Y_HOST)
            _match = obj.get(Y_MATCH, "*")
            _port = obj.get(Y_PORT, 514)
            _mode = obj.get(Y_MODE, "udp")
            _syslogFormat = obj.get(Y_SYSLOGFORMAT, "rfc5424")
            _syslogMaxsize = obj.get(Y_SYSLOGMAXSIZE)
            _syslogSeverityKey = obj.get(Y_SYSLOGSEVERITYKEY)
            _syslogFacilityKey = obj.get(Y_SYSLOGFACILITYKEY)
            _syslogHostnameKey = obj.get(Y_SYSLOGHOSTNAMEKEY, "kube_host")
            _syslogAppnameKey = obj.get(Y_SYSLOGAPPNAMEKEY, "kube_pod_name")
            _syslogProcidKey = obj.get(Y_SYSLOGPROCIDKEY)
            _syslogMsgidKey = obj.get(Y_SYSLOGMSGIDKEY)
            _syslogSdKey = obj.get(Y_SYSLOGSDKEY)
            _syslogMessageKey = obj.get(Y_SYSLOGMESSAGEKEY, "log")
            _tls = SyslogTLS.from_input(obj.get(Y_TLS))
            return Syslog(
                host=_host,
                match=_match,
                port=_port,
                mode=_mode,
                syslogFormat=_syslogFormat,
                syslogMaxsize=_syslogMaxsize,
                syslogSeverityKey=_syslogSeverityKey,
                syslogFacilityKey=_syslogFacilityKey,
                syslogHostnameKey=_syslogHostnameKey,
                syslogAppnameKey=_syslogAppnameKey,
                syslogProcidKey=_syslogProcidKey,
                syslogMsgidKey=_syslogMsgidKey,
                syslogSdKey=_syslogSdKey,
                syslogMessageKey=_syslogMessageKey,
                tls=_tls,
            )
        return None  # pragma: no cover


class OutputSpec:
    def __init__(
        self,
        forward: Forward | None = None,
        syslog: Syslog | None = None,
    ):
        self.forward = forward
        self.syslog = syslog

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.forward is not None:
            _rval[Y_FORWARD] = self.forward.to_input()
        if self.syslog is not None:
            _rval[Y_SYSLOG] = self.syslog.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'OutputSpec | None':
        if obj:
            _forward = Forward.from_input(obj.get(Y_FORWARD))
            _syslog = Syslog.from_input(obj.get(Y_SYSLOG))
            return OutputSpec(
                forward=_forward,
                syslog=_syslog,
            )
        return None  # pragma: no cover


class OutputStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'OutputStatus | None':
        if obj:
            return OutputStatus(
            )
        return None  # pragma: no cover


class LogOutput:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: LogOutputSpec | None = None,
        status: LogOutputStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = LOGOUTPUT_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'LogOutput | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = LogOutputSpec.from_input(obj.get(Y_SPEC, None))
            _status = LogOutputStatus.from_input(obj.get(Y_STATUS))
            return LogOutput(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class LogOutputList:
    def __init__(
        self,
        items: list[LogOutput],
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
    def from_input(obj) -> 'LogOutputList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return LogOutputList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
