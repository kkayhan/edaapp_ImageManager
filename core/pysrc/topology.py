#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
from .topobreakout import TopoBreakout
from .topolink import TopoLinkSpec
from .toponode import TopoNodeSpec

ENUM_TOPOLOGYLINKENCAPTYPE_NULL = 'null'
ENUM_TOPOLOGYLINKENCAPTYPE_DOT1Q = 'dot1q'
Y_LABELS = 'labels'
Y_ANNOTATIONS = 'annotations'
Y_SPEC = 'spec'
Y_ENCAPTYPE = 'encapType'
Y_NODES = 'nodes'
Y_LINKS = 'links'
Y_BREAKOUTS = 'breakouts'
# Package objects (GVK Schemas)
TOPOLOGY_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='Topology')


class TopologyLink:
    def __init__(
        self,
        name: str,
        spec: TopoLinkSpec,
        labels: dict[str, str] | None = None,
        annotations: dict[str, str] | None = None,
        encapType: str | None = None,
    ):
        self.name = name
        self.spec = spec
        self.labels = labels
        self.annotations = annotations
        self.encapType = encapType

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.name is not None:
            _rval[Y_NAME] = self.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.labels is not None:
            _rval[Y_LABELS] = self.labels
        if self.annotations is not None:
            _rval[Y_ANNOTATIONS] = self.annotations
        if self.encapType is not None:
            _rval[Y_ENCAPTYPE] = self.encapType
        return _rval

    @staticmethod
    def from_input(obj) -> 'TopologyLink | None':
        if obj:
            _name = obj.get(Y_NAME)
            _spec = TopoLinkSpec.from_input(obj.get(Y_SPEC))
            _labels = obj.get(Y_LABELS)
            _annotations = obj.get(Y_ANNOTATIONS)
            _encapType = obj.get(Y_ENCAPTYPE, "null")
            return TopologyLink(
                name=_name,
                spec=_spec,
                labels=_labels,
                annotations=_annotations,
                encapType=_encapType,
            )
        return None  # pragma: no cover


class TopologyNode:
    def __init__(
        self,
        name: str,
        spec: TopoNodeSpec,
        labels: dict[str, str] | None = None,
        annotations: dict[str, str] | None = None,
    ):
        self.name = name
        self.spec = spec
        self.labels = labels
        self.annotations = annotations

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.name is not None:
            _rval[Y_NAME] = self.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.labels is not None:
            _rval[Y_LABELS] = self.labels
        if self.annotations is not None:
            _rval[Y_ANNOTATIONS] = self.annotations
        return _rval

    @staticmethod
    def from_input(obj) -> 'TopologyNode | None':
        if obj:
            _name = obj.get(Y_NAME)
            _spec = TopoNodeSpec.from_input(obj.get(Y_SPEC))
            _labels = obj.get(Y_LABELS)
            _annotations = obj.get(Y_ANNOTATIONS)
            return TopologyNode(
                name=_name,
                spec=_spec,
                labels=_labels,
                annotations=_annotations,
            )
        return None  # pragma: no cover


class TopologySpec:
    def __init__(
        self,
        nodes: list[TopologyNode],
        links: list[TopologyLink],
        breakouts: list[TopoBreakout],
    ):
        self.nodes = nodes
        self.links = links
        self.breakouts = breakouts

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.nodes is not None:
            _rval[Y_NODES] = [x.to_input() for x in self.nodes]
        if self.links is not None:
            _rval[Y_LINKS] = [x.to_input() for x in self.links]
        if self.breakouts is not None:
            _rval[Y_BREAKOUTS] = [x.to_input() for x in self.breakouts]
        return _rval

    @staticmethod
    def from_input(obj) -> 'TopologySpec | None':
        if obj:
            _nodes = []
            if obj.get(Y_NODES) is not None:
                for x in obj.get(Y_NODES):
                    _nodes.append(TopologyNode.from_input(x))
            _links = []
            if obj.get(Y_LINKS) is not None:
                for x in obj.get(Y_LINKS):
                    _links.append(TopologyLink.from_input(x))
            _breakouts = []
            if obj.get(Y_BREAKOUTS) is not None:
                for x in obj.get(Y_BREAKOUTS):
                    _breakouts.append(TopoBreakout.from_input(x))
            return TopologySpec(
                nodes=_nodes,
                links=_links,
                breakouts=_breakouts,
            )
        return None  # pragma: no cover


class TopologyStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'TopologyStatus | None':
        if obj:
            return TopologyStatus(
            )
        return None  # pragma: no cover


class Topology:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: TopologySpec | None = None,
        status: TopologyStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = TOPOLOGY_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'Topology | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = TopologySpec.from_input(obj.get(Y_SPEC, None))
            _status = TopologyStatus.from_input(obj.get(Y_STATUS))
            return Topology(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class TopologyList:
    def __init__(
        self,
        items: list[Topology],
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
    def from_input(obj) -> 'TopologyList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return TopologyList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
