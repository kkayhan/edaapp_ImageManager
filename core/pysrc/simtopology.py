#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *

ENUM_EDGESIMNODETYPE_LINUX = 'Linux'
ENUM_EDGESIMNODETYPE_TESTMAN = 'TestMan'
ENUM_EDGESIMNODETYPE_SRLTEST = 'SrlTest'
Y_TYPE = 'type'
Y_IMAGE = 'image'
Y_IMAGEPULLSECRET = 'imagePullSecret'
Y_NODE = 'node'
Y_INTERFACE = 'interface'
Y_SIMNODE = 'simNode'
Y_SIMNODEINTERFACE = 'simNodeInterface'
Y_TOPOLOGY = 'topology'
Y_SIMNODES = 'simNodes'
# Package objects (GVK Schemas)
SIMTOPOLOGY_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='SimTopology')


class EdgeSimNode:
    def __init__(
        self,
        name: str,
        type: str,
        image: str,
        imagePullSecret: str | None = None,
    ):
        self.name = name
        self.type = type
        self.image = image
        self.imagePullSecret = imagePullSecret

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.name is not None:
            _rval[Y_NAME] = self.name
        if self.type is not None:
            _rval[Y_TYPE] = self.type
        if self.image is not None:
            _rval[Y_IMAGE] = self.image
        if self.imagePullSecret is not None:
            _rval[Y_IMAGEPULLSECRET] = self.imagePullSecret
        return _rval

    @staticmethod
    def from_input(obj) -> 'EdgeSimNode | None':
        if obj:
            _name = obj.get(Y_NAME)
            _type = obj.get(Y_TYPE)
            _image = obj.get(Y_IMAGE)
            _imagePullSecret = obj.get(Y_IMAGEPULLSECRET)
            return EdgeSimNode(
                name=_name,
                type=_type,
                image=_image,
                imagePullSecret=_imagePullSecret,
            )
        return None  # pragma: no cover


class NodeSimTopology:
    def __init__(
        self,
        node: str,
        interface: str,
        simNode: str,
        simNodeInterface: str | None = None,
    ):
        self.node = node
        self.interface = interface
        self.simNode = simNode
        self.simNodeInterface = simNodeInterface

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.node is not None:
            _rval[Y_NODE] = self.node
        if self.interface is not None:
            _rval[Y_INTERFACE] = self.interface
        if self.simNode is not None:
            _rval[Y_SIMNODE] = self.simNode
        if self.simNodeInterface is not None:
            _rval[Y_SIMNODEINTERFACE] = self.simNodeInterface
        return _rval

    @staticmethod
    def from_input(obj) -> 'NodeSimTopology | None':
        if obj:
            _node = obj.get(Y_NODE)
            _interface = obj.get(Y_INTERFACE)
            _simNode = obj.get(Y_SIMNODE)
            _simNodeInterface = obj.get(Y_SIMNODEINTERFACE)
            return NodeSimTopology(
                node=_node,
                interface=_interface,
                simNode=_simNode,
                simNodeInterface=_simNodeInterface,
            )
        return None  # pragma: no cover


class SimTopologySpec:
    def __init__(
        self,
        topology: list[NodeSimTopology],
        simNodes: list[EdgeSimNode],
    ):
        self.topology = topology
        self.simNodes = simNodes

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.topology is not None:
            _rval[Y_TOPOLOGY] = [x.to_input() for x in self.topology]
        if self.simNodes is not None:
            _rval[Y_SIMNODES] = [x.to_input() for x in self.simNodes]
        return _rval

    @staticmethod
    def from_input(obj) -> 'SimTopologySpec | None':
        if obj:
            _topology = []
            if obj.get(Y_TOPOLOGY) is not None:
                for x in obj.get(Y_TOPOLOGY):
                    _topology.append(NodeSimTopology.from_input(x))
            _simNodes = []
            if obj.get(Y_SIMNODES) is not None:
                for x in obj.get(Y_SIMNODES):
                    _simNodes.append(EdgeSimNode.from_input(x))
            return SimTopologySpec(
                topology=_topology,
                simNodes=_simNodes,
            )
        return None  # pragma: no cover


class SimTopologyStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'SimTopologyStatus | None':
        if obj:
            return SimTopologyStatus(
            )
        return None  # pragma: no cover


class SimTopology:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: SimTopologySpec | None = None,
        status: SimTopologyStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = SIMTOPOLOGY_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'SimTopology | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = SimTopologySpec.from_input(obj.get(Y_SPEC, None))
            _status = SimTopologyStatus.from_input(obj.get(Y_STATUS))
            return SimTopology(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class SimTopologyList:
    def __init__(
        self,
        items: list[SimTopology],
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
    def from_input(obj) -> 'SimTopologyList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return SimTopologyList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
