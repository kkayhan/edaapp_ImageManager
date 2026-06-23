#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *

ENUM_ONEVENTTYPE_CREATE = 'Create'
ENUM_ONEVENTTYPE_UPDATE = 'Update'
ENUM_ONEVENTTYPE_DELETE = 'Delete'
ENUM_ONEVENTTYPE_ = '*'

ENUM_INPUTOUTPUTTYPE_STRING = 'String'
ENUM_INPUTOUTPUTTYPE_NUMBER = 'Number'
ENUM_INPUTOUTPUTTYPE_BOOLEAN = 'Boolean'

ENUM_TARGETCLUSTER_MAIN = 'Main'
ENUM_TARGETCLUSTER_DIGITALTWIN = 'DigitalTwin'

ENUM_JOBIMAGE_EDA_TOOLBOX = 'eda-toolbox'
ENUM_JOBIMAGE_EDA_TESTMAN = 'eda-testman'
Y_TRIGGERS = 'triggers'
Y_ENV = 'env'
Y_JOBS = 'jobs'
Y_TARGET = 'target'
Y_EVENTS = 'events'
Y_WORKFLOWCALL = 'workflowCall'
Y_RESOURCETRIGGER = 'resourceTrigger'
Y_TYPE = 'type'
Y_GVK = 'gvk'
Y_FIELDS = 'fields'
Y_LABELS = 'labels'
Y_INPUTS = 'inputs'
Y_OUTPUTS = 'outputs'
Y_SECRETS = 'secrets'
Y_DESCRIPTION = 'description'
Y_REQUIRED = 'required'
Y_INPUTTYPE = 'inputType'
Y_DEFAULT = 'default'
Y_OUTPUTTYPE = 'outputType'
Y_OUTPUTVALUE = 'outputValue'
Y_RUNSIN = 'runsIn'
Y_WORKFLOW = 'workflow'
Y_COMPAREWITH = 'compareWith'
Y_NEEDS = 'needs'
Y_IF = 'if'
Y_STEPS = 'steps'
Y_TIMEOUTMINUTES = 'timeoutMinutes'
Y_CONTAINER = 'container'
Y_USES = 'uses'
Y_WITH = 'with'
Y_GROUP = 'group'
Y_VERSION = 'version'
Y_KIND = 'kind'
Y_ID = 'id'
Y_RUN = 'run'
Y_CONTINUEONERROR = 'continueOnError'
Y_IMAGE = 'image'
Y_CREDENTIALS = 'credentials'
Y_PORTS = 'ports'
Y_VOLUMES = 'volumes'
Y_OPTIONS = 'options'
Y_USERNAME = 'username'
Y_PASSWORD = 'password'
Y_VALID = 'valid'
Y_VALIDATIONERROR = 'validationError'
# Package objects (GVK Schemas)
PIPELINEDEFINITION_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='PipelineDefinition')


class CredentialsSpec:
    def __init__(
        self,
        username: str,
        password: str,
    ):
        self.username = username
        self.password = password

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.username is not None:
            _rval[Y_USERNAME] = self.username
        if self.password is not None:
            _rval[Y_PASSWORD] = self.password
        return _rval

    @staticmethod
    def from_input(obj) -> 'CredentialsSpec | None':
        if obj:
            _username = obj.get(Y_USERNAME)
            _password = obj.get(Y_PASSWORD)
            return CredentialsSpec(
                username=_username,
                password=_password,
            )
        return None  # pragma: no cover


class ContainerSpec:
    def __init__(
        self,
        image: str,
        credentials: CredentialsSpec | None = None,
        env: dict[str, str] | None = None,
        ports: list[int] | None = None,
        volumes: list[str] | None = None,
        options: str | None = None,
    ):
        self.image = image
        self.credentials = credentials
        self.env = env
        self.ports = ports
        self.volumes = volumes
        self.options = options

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.image is not None:
            _rval[Y_IMAGE] = self.image
        if self.credentials is not None:
            _rval[Y_CREDENTIALS] = self.credentials.to_input()
        if self.env is not None:
            _rval[Y_ENV] = self.env
        if self.ports is not None:
            _rval[Y_PORTS] = self.ports
        if self.volumes is not None:
            _rval[Y_VOLUMES] = self.volumes
        if self.options is not None:
            _rval[Y_OPTIONS] = self.options
        return _rval

    @staticmethod
    def from_input(obj) -> 'ContainerSpec | None':
        if obj:
            _image = obj.get(Y_IMAGE)
            _credentials = CredentialsSpec.from_input(obj.get(Y_CREDENTIALS))
            _env = obj.get(Y_ENV)
            _ports = obj.get(Y_PORTS)
            _volumes = obj.get(Y_VOLUMES)
            _options = obj.get(Y_OPTIONS)
            return ContainerSpec(
                image=_image,
                credentials=_credentials,
                env=_env,
                ports=_ports,
                volumes=_volumes,
                options=_options,
            )
        return None  # pragma: no cover


class ResourceGVK:
    def __init__(
        self,
        group: str | None = None,
        version: str | None = None,
        kind: str | None = None,
    ):
        self.group = group
        self.version = version
        self.kind = kind

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.group is not None:
            _rval[Y_GROUP] = self.group
        if self.version is not None:
            _rval[Y_VERSION] = self.version
        if self.kind is not None:
            _rval[Y_KIND] = self.kind
        return _rval

    @staticmethod
    def from_input(obj) -> 'ResourceGVK | None':
        if obj:
            _group = obj.get(Y_GROUP)
            _version = obj.get(Y_VERSION)
            _kind = obj.get(Y_KIND)
            return ResourceGVK(
                group=_group,
                version=_version,
                kind=_kind,
            )
        return None  # pragma: no cover


class StepSpec:
    def __init__(
        self,
        id: str | None = None,
        name: str | None = None,
        uses: str | None = None,
        run: str | None = None,
        with: dict[str, object] | None = None,
        env: dict[str, str] | None = None,
        if: str | None = None,
        continueOnError: bool | None = None,
        timeoutMinutes: int | None = None,
    ):
        self.id = id
        self.name = name
        self.uses = uses
        self.run = run
        self.with = with
        self.env = env
        self.if = if
        self.continueOnError = continueOnError
        self.timeoutMinutes = timeoutMinutes

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.id is not None:
            _rval[Y_ID] = self.id
        if self.name is not None:
            _rval[Y_NAME] = self.name
        if self.uses is not None:
            _rval[Y_USES] = self.uses
        if self.run is not None:
            _rval[Y_RUN] = self.run
        if self.with is not None:
            _rval[Y_WITH] = self.with
        if self.env is not None:
            _rval[Y_ENV] = self.env
        if self.if is not None:
            _rval[Y_IF] = self.if
        if self.continueOnError is not None:
            _rval[Y_CONTINUEONERROR] = self.continueOnError
        if self.timeoutMinutes is not None:
            _rval[Y_TIMEOUTMINUTES] = self.timeoutMinutes
        return _rval

    @staticmethod
    def from_input(obj) -> 'StepSpec | None':
        if obj:
            _id = obj.get(Y_ID)
            _name = obj.get(Y_NAME)
            _uses = obj.get(Y_USES)
            _run = obj.get(Y_RUN)
            _with = obj.get(Y_WITH)
            _env = obj.get(Y_ENV)
            _if = obj.get(Y_IF)
            _continueOnError = obj.get(Y_CONTINUEONERROR)
            _timeoutMinutes = obj.get(Y_TIMEOUTMINUTES)
            return StepSpec(
                id=_id,
                name=_name,
                uses=_uses,
                run=_run,
                with=_with,
                env=_env,
                if=_if,
                continueOnError=_continueOnError,
                timeoutMinutes=_timeoutMinutes,
            )
        return None  # pragma: no cover


class JobSpec:
    def __init__(
        self,
        name: str | None = None,
        runsIn: str | None = None,
        workflow: ResourceGVK | None = None,
        compareWith: str | None = None,
        needs: list[str] | None = None,
        if: str | None = None,
        env: dict[str, str] | None = None,
        outputs: dict[str, str] | None = None,
        steps: list[StepSpec] | None = None,
        timeoutMinutes: int | None = None,
        container: ContainerSpec | None = None,
        uses: str | None = None,
        with: dict[str, object] | None = None,
    ):
        self.name = name
        self.runsIn = runsIn
        self.workflow = workflow
        self.compareWith = compareWith
        self.needs = needs
        self.if = if
        self.env = env
        self.outputs = outputs
        self.steps = steps
        self.timeoutMinutes = timeoutMinutes
        self.container = container
        self.uses = uses
        self.with = with

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.name is not None:
            _rval[Y_NAME] = self.name
        if self.runsIn is not None:
            _rval[Y_RUNSIN] = self.runsIn
        if self.workflow is not None:
            _rval[Y_WORKFLOW] = self.workflow.to_input()
        if self.compareWith is not None:
            _rval[Y_COMPAREWITH] = self.compareWith
        if self.needs is not None:
            _rval[Y_NEEDS] = self.needs
        if self.if is not None:
            _rval[Y_IF] = self.if
        if self.env is not None:
            _rval[Y_ENV] = self.env
        if self.outputs is not None:
            _rval[Y_OUTPUTS] = self.outputs
        if self.steps is not None:
            _rval[Y_STEPS] = [x.to_input() for x in self.steps]
        if self.timeoutMinutes is not None:
            _rval[Y_TIMEOUTMINUTES] = self.timeoutMinutes
        if self.container is not None:
            _rval[Y_CONTAINER] = self.container.to_input()
        if self.uses is not None:
            _rval[Y_USES] = self.uses
        if self.with is not None:
            _rval[Y_WITH] = self.with
        return _rval

    @staticmethod
    def from_input(obj) -> 'JobSpec | None':
        if obj:
            _name = obj.get(Y_NAME)
            _runsIn = obj.get(Y_RUNSIN)
            _workflow = ResourceGVK.from_input(obj.get(Y_WORKFLOW))
            _compareWith = obj.get(Y_COMPAREWITH)
            _needs = obj.get(Y_NEEDS)
            _if = obj.get(Y_IF)
            _env = obj.get(Y_ENV)
            _outputs = obj.get(Y_OUTPUTS)
            _steps = []
            if obj.get(Y_STEPS) is not None:
                for x in obj.get(Y_STEPS):
                    _steps.append(StepSpec.from_input(x))
            _timeoutMinutes = obj.get(Y_TIMEOUTMINUTES)
            _container = ContainerSpec.from_input(obj.get(Y_CONTAINER))
            _uses = obj.get(Y_USES)
            _with = obj.get(Y_WITH)
            return JobSpec(
                name=_name,
                runsIn=_runsIn,
                workflow=_workflow,
                compareWith=_compareWith,
                needs=_needs,
                if=_if,
                env=_env,
                outputs=_outputs,
                steps=_steps,
                timeoutMinutes=_timeoutMinutes,
                container=_container,
                uses=_uses,
                with=_with,
            )
        return None  # pragma: no cover


class ResourceTrigger:
    def __init__(
        self,
        type: list[str],
        gvk: ResourceGVK | None = None,
        fields: list[str] | None = None,
        labels: list[str] | None = None,
    ):
        self.type = type
        self.gvk = gvk
        self.fields = fields
        self.labels = labels

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.type is not None:
            _rval[Y_TYPE] = self.type
        if self.gvk is not None:
            _rval[Y_GVK] = self.gvk.to_input()
        if self.fields is not None:
            _rval[Y_FIELDS] = self.fields
        if self.labels is not None:
            _rval[Y_LABELS] = self.labels
        return _rval

    @staticmethod
    def from_input(obj) -> 'ResourceTrigger | None':
        if obj:
            _type = obj.get(Y_TYPE)
            _gvk = ResourceGVK.from_input(obj.get(Y_GVK))
            _fields = obj.get(Y_FIELDS)
            _labels = obj.get(Y_LABELS)
            return ResourceTrigger(
                type=_type,
                gvk=_gvk,
                fields=_fields,
                labels=_labels,
            )
        return None  # pragma: no cover


class TriggerEvent:
    def __init__(
        self,
        resourceTrigger: list[ResourceTrigger] | None = None,
    ):
        self.resourceTrigger = resourceTrigger

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.resourceTrigger is not None:
            _rval[Y_RESOURCETRIGGER] = [x.to_input() for x in self.resourceTrigger]
        return _rval

    @staticmethod
    def from_input(obj) -> 'TriggerEvent | None':
        if obj:
            _resourceTrigger = []
            if obj.get(Y_RESOURCETRIGGER) is not None:
                for x in obj.get(Y_RESOURCETRIGGER):
                    _resourceTrigger.append(ResourceTrigger.from_input(x))
            return TriggerEvent(
                resourceTrigger=_resourceTrigger,
            )
        return None  # pragma: no cover


class WorkflowInput:
    def __init__(
        self,
        inputType: str,
        description: str | None = None,
        required: bool | None = None,
        default: object | None = None,
    ):
        self.inputType = inputType
        self.description = description
        self.required = required
        self.default = default

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.inputType is not None:
            _rval[Y_INPUTTYPE] = self.inputType
        if self.description is not None:
            _rval[Y_DESCRIPTION] = self.description
        if self.required is not None:
            _rval[Y_REQUIRED] = self.required
        if self.default is not None:
            _rval[Y_DEFAULT] = self.default
        return _rval

    @staticmethod
    def from_input(obj) -> 'WorkflowInput | None':
        if obj:
            _inputType = obj.get(Y_INPUTTYPE)
            _description = obj.get(Y_DESCRIPTION)
            _required = obj.get(Y_REQUIRED)
            _default = obj.get(Y_DEFAULT)
            return WorkflowInput(
                inputType=_inputType,
                description=_description,
                required=_required,
                default=_default,
            )
        return None  # pragma: no cover


class WorkflowOutput:
    def __init__(
        self,
        outputType: str,
        outputValue: str,
        description: str | None = None,
    ):
        self.outputType = outputType
        self.outputValue = outputValue
        self.description = description

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.outputType is not None:
            _rval[Y_OUTPUTTYPE] = self.outputType
        if self.outputValue is not None:
            _rval[Y_OUTPUTVALUE] = self.outputValue
        if self.description is not None:
            _rval[Y_DESCRIPTION] = self.description
        return _rval

    @staticmethod
    def from_input(obj) -> 'WorkflowOutput | None':
        if obj:
            _outputType = obj.get(Y_OUTPUTTYPE)
            _outputValue = obj.get(Y_OUTPUTVALUE)
            _description = obj.get(Y_DESCRIPTION)
            return WorkflowOutput(
                outputType=_outputType,
                outputValue=_outputValue,
                description=_description,
            )
        return None  # pragma: no cover


class WorkflowSecret:
    def __init__(
        self,
        description: str | None = None,
        required: bool | None = None,
    ):
        self.description = description
        self.required = required

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.description is not None:
            _rval[Y_DESCRIPTION] = self.description
        if self.required is not None:
            _rval[Y_REQUIRED] = self.required
        return _rval

    @staticmethod
    def from_input(obj) -> 'WorkflowSecret | None':
        if obj:
            _description = obj.get(Y_DESCRIPTION)
            _required = obj.get(Y_REQUIRED)
            return WorkflowSecret(
                description=_description,
                required=_required,
            )
        return None  # pragma: no cover


class WorkflowCallTrigger:
    def __init__(
        self,
        inputs: dict[str, WorkflowInput] | None = None,
        outputs: dict[str, WorkflowOutput] | None = None,
        secrets: dict[str, WorkflowSecret] | None = None,
    ):
        self.inputs = inputs
        self.outputs = outputs
        self.secrets = secrets

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.inputs is not None:
            _rval[Y_INPUTS] = {k: v.to_input() for k, v in self.inputs.items()}
        if self.outputs is not None:
            _rval[Y_OUTPUTS] = {k: v.to_input() for k, v in self.outputs.items()}
        if self.secrets is not None:
            _rval[Y_SECRETS] = {k: v.to_input() for k, v in self.secrets.items()}
        return _rval

    @staticmethod
    def from_input(obj) -> 'WorkflowCallTrigger | None':
        if obj:
            _inputs = {}
            if obj.get(Y_INPUTS) is not None:
                for k, v in obj.get(Y_INPUTS).items():
                    _inputs[k] = WorkflowInput.from_input(v)
            _outputs = {}
            if obj.get(Y_OUTPUTS) is not None:
                for k, v in obj.get(Y_OUTPUTS).items():
                    _outputs[k] = WorkflowOutput.from_input(v)
            _secrets = {}
            if obj.get(Y_SECRETS) is not None:
                for k, v in obj.get(Y_SECRETS).items():
                    _secrets[k] = WorkflowSecret.from_input(v)
            return WorkflowCallTrigger(
                inputs=_inputs,
                outputs=_outputs,
                secrets=_secrets,
            )
        return None  # pragma: no cover


class OnClause:
    def __init__(
        self,
        events: TriggerEvent | None = None,
        workflowCall: WorkflowCallTrigger | None = None,
    ):
        self.events = events
        self.workflowCall = workflowCall

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.events is not None:
            _rval[Y_EVENTS] = self.events.to_input()
        if self.workflowCall is not None:
            _rval[Y_WORKFLOWCALL] = self.workflowCall.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'OnClause | None':
        if obj:
            _events = TriggerEvent.from_input(obj.get(Y_EVENTS))
            _workflowCall = WorkflowCallTrigger.from_input(obj.get(Y_WORKFLOWCALL))
            return OnClause(
                events=_events,
                workflowCall=_workflowCall,
            )
        return None  # pragma: no cover


class PipelineDefinitionSpec:
    def __init__(
        self,
        triggers: OnClause,
        jobs: dict[str, JobSpec],
        name: str | None = None,
        env: dict[str, str] | None = None,
        target: list[str] | None = None,
    ):
        self.triggers = triggers
        self.jobs = jobs
        self.name = name
        self.env = env
        self.target = target

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.triggers is not None:
            _rval[Y_TRIGGERS] = self.triggers.to_input()
        if self.jobs is not None:
            _rval[Y_JOBS] = {k: v.to_input() for k, v in self.jobs.items()}
        if self.name is not None:
            _rval[Y_NAME] = self.name
        if self.env is not None:
            _rval[Y_ENV] = self.env
        if self.target is not None:
            _rval[Y_TARGET] = self.target
        return _rval

    @staticmethod
    def from_input(obj) -> 'PipelineDefinitionSpec | None':
        if obj:
            _triggers = OnClause.from_input(obj.get(Y_TRIGGERS))
            _jobs = {}
            if obj.get(Y_JOBS) is not None:
                for k, v in obj.get(Y_JOBS).items():
                    _jobs[k] = JobSpec.from_input(v)
            _name = obj.get(Y_NAME)
            _env = obj.get(Y_ENV)
            _target = obj.get(Y_TARGET)
            return PipelineDefinitionSpec(
                triggers=_triggers,
                jobs=_jobs,
                name=_name,
                env=_env,
                target=_target,
            )
        return None  # pragma: no cover


class PipelineDefinitionStatus:
    def __init__(
        self,
        valid: bool,
        validationError: str | None = None,
    ):
        self.valid = valid
        self.validationError = validationError

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.valid is not None:
            _rval[Y_VALID] = self.valid
        if self.validationError is not None:
            _rval[Y_VALIDATIONERROR] = self.validationError
        return _rval

    @staticmethod
    def from_input(obj) -> 'PipelineDefinitionStatus | None':
        if obj:
            _valid = obj.get(Y_VALID)
            _validationError = obj.get(Y_VALIDATIONERROR)
            return PipelineDefinitionStatus(
                valid=_valid,
                validationError=_validationError,
            )
        return None  # pragma: no cover


class PipelineDefinition:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: PipelineDefinitionSpec | None = None,
        status: PipelineDefinitionStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = PIPELINEDEFINITION_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'PipelineDefinition | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = PipelineDefinitionSpec.from_input(obj.get(Y_SPEC, None))
            _status = PipelineDefinitionStatus.from_input(obj.get(Y_STATUS))
            return PipelineDefinition(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class PipelineDefinitionList:
    def __init__(
        self,
        items: list[PipelineDefinition],
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
    def from_input(obj) -> 'PipelineDefinitionList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return PipelineDefinitionList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
