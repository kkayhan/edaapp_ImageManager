#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
Y_GROUP = 'group'
Y_VERSION = 'version'
Y_KIND = 'kind'
Y_JSONSCHEMASPEC = 'jsonSchemaSpec'
Y_JSONSCHEMASTATUS = 'jsonSchemaStatus'
Y_IMAGE = 'image'
Y_IMAGEPULLSECRETS = 'imagePullSecrets'
Y_FLOWDEFINITIONRESOURCE = 'flowDefinitionResource'
Y_FLOWDEFINITIONSCHEMA = 'flowDefinitionSchema'
Y_NAMESPACED = 'namespaced'
# Package objects (GVK Schemas)
WORKFLOWDEFINITION_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='WorkflowDefinition')


class FlowDefinitionResource:
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
    def from_input(obj) -> 'FlowDefinitionResource | None':
        if obj:
            _version = obj.get(Y_VERSION)
            _kind = obj.get(Y_KIND)
            _group = obj.get(Y_GROUP)
            return FlowDefinitionResource(
                version=_version,
                kind=_kind,
                group=_group,
            )
        return None  # pragma: no cover


class WorkflowDefinitionSchema:
    def __init__(
        self,
        jsonSchemaSpec: str | None = None,
        jsonSchemaStatus: str | None = None,
    ):
        self.jsonSchemaSpec = jsonSchemaSpec
        self.jsonSchemaStatus = jsonSchemaStatus

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.jsonSchemaSpec is not None:
            _rval[Y_JSONSCHEMASPEC] = self.jsonSchemaSpec
        if self.jsonSchemaStatus is not None:
            _rval[Y_JSONSCHEMASTATUS] = self.jsonSchemaStatus
        return _rval

    @staticmethod
    def from_input(obj) -> 'WorkflowDefinitionSchema | None':
        if obj:
            _jsonSchemaSpec = obj.get(Y_JSONSCHEMASPEC)
            _jsonSchemaStatus = obj.get(Y_JSONSCHEMASTATUS)
            return WorkflowDefinitionSchema(
                jsonSchemaSpec=_jsonSchemaSpec,
                jsonSchemaStatus=_jsonSchemaStatus,
            )
        return None  # pragma: no cover


class WorkflowDefinitionSpec:
    def __init__(
        self,
        image: str,
        imagePullSecrets: list[str] | None = None,
        flowDefinitionResource: FlowDefinitionResource | None = None,
        flowDefinitionSchema: WorkflowDefinitionSchema | None = None,
        namespaced: bool | None = None,
    ):
        self.image = image
        self.imagePullSecrets = imagePullSecrets
        self.flowDefinitionResource = flowDefinitionResource
        self.flowDefinitionSchema = flowDefinitionSchema
        self.namespaced = namespaced

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.image is not None:
            _rval[Y_IMAGE] = self.image
        if self.imagePullSecrets is not None:
            _rval[Y_IMAGEPULLSECRETS] = self.imagePullSecrets
        if self.flowDefinitionResource is not None:
            _rval[Y_FLOWDEFINITIONRESOURCE] = self.flowDefinitionResource.to_input()
        if self.flowDefinitionSchema is not None:
            _rval[Y_FLOWDEFINITIONSCHEMA] = self.flowDefinitionSchema.to_input()
        if self.namespaced is not None:
            _rval[Y_NAMESPACED] = self.namespaced
        return _rval

    @staticmethod
    def from_input(obj) -> 'WorkflowDefinitionSpec | None':
        if obj:
            _image = obj.get(Y_IMAGE)
            _imagePullSecrets = obj.get(Y_IMAGEPULLSECRETS)
            _flowDefinitionResource = FlowDefinitionResource.from_input(obj.get(Y_FLOWDEFINITIONRESOURCE))
            _flowDefinitionSchema = WorkflowDefinitionSchema.from_input(obj.get(Y_FLOWDEFINITIONSCHEMA))
            _namespaced = obj.get(Y_NAMESPACED, True)
            return WorkflowDefinitionSpec(
                image=_image,
                imagePullSecrets=_imagePullSecrets,
                flowDefinitionResource=_flowDefinitionResource,
                flowDefinitionSchema=_flowDefinitionSchema,
                namespaced=_namespaced,
            )
        return None  # pragma: no cover


class WorkflowDefinitionStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'WorkflowDefinitionStatus | None':
        if obj:
            return WorkflowDefinitionStatus(
            )
        return None  # pragma: no cover


class WorkflowDefinition:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: WorkflowDefinitionSpec | None = None,
        status: WorkflowDefinitionStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = WORKFLOWDEFINITION_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'WorkflowDefinition | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = WorkflowDefinitionSpec.from_input(obj.get(Y_SPEC, None))
            _status = WorkflowDefinitionStatus.from_input(obj.get(Y_STATUS))
            return WorkflowDefinition(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class WorkflowDefinitionList:
    def __init__(
        self,
        items: list[WorkflowDefinition],
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
    def from_input(obj) -> 'WorkflowDefinitionList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return WorkflowDefinitionList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
