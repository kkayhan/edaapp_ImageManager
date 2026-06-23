#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
from .topolink import Endpoint
Y_LOCAL = 'local'
Y_SIM = 'sim'
Y_SPEED = 'speed'
Y_LINKS = 'links'
Y_BONDNAME = 'bondName'
# Package objects (GVK Schemas)
SIMLINK_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='SimLink')


class SimLinkMember:
    def __init__(
        self,
        local: Endpoint,
        sim: Endpoint,
        speed: str | None = None,
    ):
        self.local = local
        self.sim = sim
        self.speed = speed

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.local is not None:
            _rval[Y_LOCAL] = self.local.to_input()
        if self.sim is not None:
            _rval[Y_SIM] = self.sim.to_input()
        if self.speed is not None:
            _rval[Y_SPEED] = self.speed
        return _rval

    @staticmethod
    def from_input(obj) -> 'SimLinkMember | None':
        if obj:
            _local = Endpoint.from_input(obj.get(Y_LOCAL))
            _sim = Endpoint.from_input(obj.get(Y_SIM))
            _speed = obj.get(Y_SPEED)
            return SimLinkMember(
                local=_local,
                sim=_sim,
                speed=_speed,
            )
        return None  # pragma: no cover


class SimLinkSpec:
    def __init__(
        self,
        links: list[SimLinkMember],
        bondName: str | None = None,
    ):
        self.links = links
        self.bondName = bondName

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.links is not None:
            _rval[Y_LINKS] = [x.to_input() for x in self.links]
        if self.bondName is not None:
            _rval[Y_BONDNAME] = self.bondName
        return _rval

    @staticmethod
    def from_input(obj) -> 'SimLinkSpec | None':
        if obj:
            _links = []
            if obj.get(Y_LINKS) is not None:
                for x in obj.get(Y_LINKS):
                    _links.append(SimLinkMember.from_input(x))
            _bondName = obj.get(Y_BONDNAME)
            return SimLinkSpec(
                links=_links,
                bondName=_bondName,
            )
        return None  # pragma: no cover


class SimLinkStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'SimLinkStatus | None':
        if obj:
            return SimLinkStatus(
            )
        return None  # pragma: no cover


class SimLink:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: SimLinkSpec | None = None,
        status: SimLinkStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = SIMLINK_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'SimLink | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = SimLinkSpec.from_input(obj.get(Y_SPEC, None))
            _status = SimLinkStatus.from_input(obj.get(Y_STATUS))
            return SimLink(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class SimLinkList:
    def __init__(
        self,
        items: list[SimLink],
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
    def from_input(obj) -> 'SimLinkList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return SimLinkList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
