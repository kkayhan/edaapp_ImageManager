#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *

ENUM_PIPELINESTATE_PENDING = 'Pending'
ENUM_PIPELINESTATE_RUNNING = 'Running'
ENUM_PIPELINESTATE_SUCCEEDED = 'Succeeded'
ENUM_PIPELINESTATE_FAILED = 'Failed'
ENUM_PIPELINESTATE_ERROR = 'Error'

ENUM_JOBSTATE_PENDING = 'Pending'
ENUM_JOBSTATE_RUNNING = 'Running'
ENUM_JOBSTATE_SUCCEEDED = 'Succeeded'
ENUM_JOBSTATE_FAILED = 'Failed'
ENUM_JOBSTATE_SKIPPED = 'Skipped'
Y_PIPELINEDEFINITIONS = 'pipelineDefinitions'
Y_TRANSACTIONID = 'transactionId'
Y_TARGET = 'target'
Y_NAMESPACE = 'namespace'
Y_ID = 'id'
Y_STATE = 'state'
Y_STARTTIME = 'startTime'
Y_COMPLETIONTIME = 'completionTime'
Y_JOBSTATUSES = 'jobStatuses'
Y_START_TIME = 'start-time'
Y_COMPLETION_TIME = 'completion-time'
Y_WORKFLOW_ID = 'workflow-id'
# Package objects (GVK Schemas)
TRANSACTIONPIPELINE_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='TransactionPipeline')


class JobStatus:
    def __init__(
        self,
        state: str | None = None,
        start_time: object | None = None,
        completion_time: object | None = None,
        workflow_id: str | None = None,
    ):
        self.state = state
        self.start_time = start_time
        self.completion_time = completion_time
        self.workflow_id = workflow_id

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.state is not None:
            _rval[Y_STATE] = self.state
        if self.start_time is not None:
            _rval[Y_START_TIME] = self.start_time
        if self.completion_time is not None:
            _rval[Y_COMPLETION_TIME] = self.completion_time
        if self.workflow_id is not None:
            _rval[Y_WORKFLOW_ID] = self.workflow_id
        return _rval

    @staticmethod
    def from_input(obj) -> 'JobStatus | None':
        if obj:
            _state = obj.get(Y_STATE)
            _start_time = obj.get(Y_START_TIME)
            _completion_time = obj.get(Y_COMPLETION_TIME)
            _workflow_id = obj.get(Y_WORKFLOW_ID)
            return JobStatus(
                state=_state,
                start_time=_start_time,
                completion_time=_completion_time,
                workflow_id=_workflow_id,
            )
        return None  # pragma: no cover


class PipelineDefinitionRef:
    def __init__(
        self,
        name: str | None = None,
        namespace: str | None = None,
    ):
        self.name = name
        self.namespace = namespace

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.name is not None:
            _rval[Y_NAME] = self.name
        if self.namespace is not None:
            _rval[Y_NAMESPACE] = self.namespace
        return _rval

    @staticmethod
    def from_input(obj) -> 'PipelineDefinitionRef | None':
        if obj:
            _name = obj.get(Y_NAME)
            _namespace = obj.get(Y_NAMESPACE)
            return PipelineDefinitionRef(
                name=_name,
                namespace=_namespace,
            )
        return None  # pragma: no cover


class TransactionPipelineSpec:
    def __init__(
        self,
        pipelineDefinitions: list[PipelineDefinitionRef] | None = None,
        transactionId: int | None = None,
        target: list[str] | None = None,
    ):
        self.pipelineDefinitions = pipelineDefinitions
        self.transactionId = transactionId
        self.target = target

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.pipelineDefinitions is not None:
            _rval[Y_PIPELINEDEFINITIONS] = [x.to_input() for x in self.pipelineDefinitions]
        if self.transactionId is not None:
            _rval[Y_TRANSACTIONID] = self.transactionId
        if self.target is not None:
            _rval[Y_TARGET] = self.target
        return _rval

    @staticmethod
    def from_input(obj) -> 'TransactionPipelineSpec | None':
        if obj:
            _pipelineDefinitions = []
            if obj.get(Y_PIPELINEDEFINITIONS) is not None:
                for x in obj.get(Y_PIPELINEDEFINITIONS):
                    _pipelineDefinitions.append(PipelineDefinitionRef.from_input(x))
            _transactionId = obj.get(Y_TRANSACTIONID)
            _target = obj.get(Y_TARGET)
            return TransactionPipelineSpec(
                pipelineDefinitions=_pipelineDefinitions,
                transactionId=_transactionId,
                target=_target,
            )
        return None  # pragma: no cover


class TransactionPipelineStatus:
    def __init__(
        self,
        id: int | None = None,
        state: str | None = None,
        startTime: object | None = None,
        completionTime: object | None = None,
        jobStatuses: dict[str, JobStatus] | None = None,
    ):
        self.id = id
        self.state = state
        self.startTime = startTime
        self.completionTime = completionTime
        self.jobStatuses = jobStatuses

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.id is not None:
            _rval[Y_ID] = self.id
        if self.state is not None:
            _rval[Y_STATE] = self.state
        if self.startTime is not None:
            _rval[Y_STARTTIME] = self.startTime
        if self.completionTime is not None:
            _rval[Y_COMPLETIONTIME] = self.completionTime
        if self.jobStatuses is not None:
            _rval[Y_JOBSTATUSES] = {k: v.to_input() for k, v in self.jobStatuses.items()}
        return _rval

    @staticmethod
    def from_input(obj) -> 'TransactionPipelineStatus | None':
        if obj:
            _id = obj.get(Y_ID)
            _state = obj.get(Y_STATE)
            _startTime = obj.get(Y_STARTTIME)
            _completionTime = obj.get(Y_COMPLETIONTIME)
            _jobStatuses = {}
            if obj.get(Y_JOBSTATUSES) is not None:
                for k, v in obj.get(Y_JOBSTATUSES).items():
                    _jobStatuses[k] = JobStatus.from_input(v)
            return TransactionPipelineStatus(
                id=_id,
                state=_state,
                startTime=_startTime,
                completionTime=_completionTime,
                jobStatuses=_jobStatuses,
            )
        return None  # pragma: no cover


class TransactionPipeline:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: TransactionPipelineSpec | None = None,
        status: TransactionPipelineStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = TRANSACTIONPIPELINE_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'TransactionPipeline | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = TransactionPipelineSpec.from_input(obj.get(Y_SPEC, None))
            _status = TransactionPipelineStatus.from_input(obj.get(Y_STATUS))
            return TransactionPipeline(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class TransactionPipelineList:
    def __init__(
        self,
        items: list[TransactionPipeline],
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
    def from_input(obj) -> 'TransactionPipelineList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return TransactionPipelineList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
