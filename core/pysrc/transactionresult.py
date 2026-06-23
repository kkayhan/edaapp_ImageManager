#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
Y_NAMESPACE = 'namespace'
Y_GVK = 'gvk'
Y_ACTION = 'action'
Y_OUTPUT = 'output'
Y_EXECUTIONTIMEUS = 'executionTimeUs'
Y_SCRIPT = 'script'
Y_ERRORS = 'errors'
Y_TOTALEXECUTIONTIMEMS = 'totalExecutionTimeMs'
Y_INSTANCESRUN = 'instancesRun'
Y_INPUTRESOURCECOUNT = 'inputResourceCount'
Y_TARGETSMODIFIED = 'targetsModified'
Y_TARGETSMODIFIEDCOUNT = 'targetsModifiedCount'
Y_ENGINETIMEMS = 'engineTimeMs'
Y_PUSHTIMEMS = 'pushTimeMs'
Y_PUBLISHTIMEMS = 'publishTimeMs'
Y_SAVETIMEMS = 'saveTimeMs'
Y_TOTALTIMEMS = 'totalTimeMs'
Y_APPSUMMARY = 'appSummary'
Y_DESCRIPTION = 'description'
Y_DRYRUN = 'dryRun'
Y_INPUTRESOURCES = 'inputResources'
Y_APPLICATIONERRORS = 'applicationErrors'
Y_GENERALERRORS = 'generalErrors'
Y_TARGETERRORS = 'targetErrors'
Y_RESULT = 'result'
Y_EXECUTIONSUMMARY = 'executionSummary'
Y_COMMIT = 'commit'
Y_USERNAME = 'username'
Y_TIMESTAMP = 'timestamp'
Y_BUNDLEDTRANSACTIONID = 'bundledTransactionId'
# Package objects (GVK Schemas)
TRANSACTIONRESULT_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='TransactionResult')


class AppSummary:
    def __init__(
        self,
        gvk: str,
        totalExecutionTimeMs: int,
        instancesRun: int,
    ):
        self.gvk = gvk
        self.totalExecutionTimeMs = totalExecutionTimeMs
        self.instancesRun = instancesRun

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.gvk is not None:
            _rval[Y_GVK] = self.gvk
        if self.totalExecutionTimeMs is not None:
            _rval[Y_TOTALEXECUTIONTIMEMS] = self.totalExecutionTimeMs
        if self.instancesRun is not None:
            _rval[Y_INSTANCESRUN] = self.instancesRun
        return _rval

    @staticmethod
    def from_input(obj) -> 'AppSummary | None':
        if obj:
            _gvk = obj.get(Y_GVK)
            _totalExecutionTimeMs = obj.get(Y_TOTALEXECUTIONTIMEMS)
            _instancesRun = obj.get(Y_INSTANCESRUN)
            return AppSummary(
                gvk=_gvk,
                totalExecutionTimeMs=_totalExecutionTimeMs,
                instancesRun=_instancesRun,
            )
        return None  # pragma: no cover


class TransactionScriptInfo:
    def __init__(
        self,
        output: str | None = None,
        executionTimeUs: int | None = None,
    ):
        self.output = output
        self.executionTimeUs = executionTimeUs

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.output is not None:
            _rval[Y_OUTPUT] = self.output
        if self.executionTimeUs is not None:
            _rval[Y_EXECUTIONTIMEUS] = self.executionTimeUs
        return _rval

    @staticmethod
    def from_input(obj) -> 'TransactionScriptInfo | None':
        if obj:
            _output = obj.get(Y_OUTPUT)
            _executionTimeUs = obj.get(Y_EXECUTIONTIMEUS)
            return TransactionScriptInfo(
                output=_output,
                executionTimeUs=_executionTimeUs,
            )
        return None  # pragma: no cover


class ApplicationErrors:
    def __init__(
        self,
        namespace: str,
        gvk: str,
        name: str,
        script: TransactionScriptInfo,
        errors: list[str] | None = None,
    ):
        self.namespace = namespace
        self.gvk = gvk
        self.name = name
        self.script = script
        self.errors = errors

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.namespace is not None:
            _rval[Y_NAMESPACE] = self.namespace
        if self.gvk is not None:
            _rval[Y_GVK] = self.gvk
        if self.name is not None:
            _rval[Y_NAME] = self.name
        if self.script is not None:
            _rval[Y_SCRIPT] = self.script.to_input()
        if self.errors is not None:
            _rval[Y_ERRORS] = self.errors
        return _rval

    @staticmethod
    def from_input(obj) -> 'ApplicationErrors | None':
        if obj:
            _namespace = obj.get(Y_NAMESPACE)
            _gvk = obj.get(Y_GVK)
            _name = obj.get(Y_NAME)
            _script = TransactionScriptInfo.from_input(obj.get(Y_SCRIPT))
            _errors = obj.get(Y_ERRORS)
            return ApplicationErrors(
                namespace=_namespace,
                gvk=_gvk,
                name=_name,
                script=_script,
                errors=_errors,
            )
        return None  # pragma: no cover


class TargetSummary:
    def __init__(
        self,
        namespace: str,
        name: str,
    ):
        self.namespace = namespace
        self.name = name

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.namespace is not None:
            _rval[Y_NAMESPACE] = self.namespace
        if self.name is not None:
            _rval[Y_NAME] = self.name
        return _rval

    @staticmethod
    def from_input(obj) -> 'TargetSummary | None':
        if obj:
            _namespace = obj.get(Y_NAMESPACE)
            _name = obj.get(Y_NAME)
            return TargetSummary(
                namespace=_namespace,
                name=_name,
            )
        return None  # pragma: no cover


class ExecutionSummary:
    def __init__(
        self,
        inputResourceCount: int | None = None,
        targetsModified: list[TargetSummary] | None = None,
        targetsModifiedCount: int | None = None,
        engineTimeMs: int | None = None,
        pushTimeMs: int | None = None,
        publishTimeMs: int | None = None,
        saveTimeMs: int | None = None,
        totalTimeMs: int | None = None,
        appSummary: list[AppSummary] | None = None,
    ):
        self.inputResourceCount = inputResourceCount
        self.targetsModified = targetsModified
        self.targetsModifiedCount = targetsModifiedCount
        self.engineTimeMs = engineTimeMs
        self.pushTimeMs = pushTimeMs
        self.publishTimeMs = publishTimeMs
        self.saveTimeMs = saveTimeMs
        self.totalTimeMs = totalTimeMs
        self.appSummary = appSummary

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.inputResourceCount is not None:
            _rval[Y_INPUTRESOURCECOUNT] = self.inputResourceCount
        if self.targetsModified is not None:
            _rval[Y_TARGETSMODIFIED] = [x.to_input() for x in self.targetsModified]
        if self.targetsModifiedCount is not None:
            _rval[Y_TARGETSMODIFIEDCOUNT] = self.targetsModifiedCount
        if self.engineTimeMs is not None:
            _rval[Y_ENGINETIMEMS] = self.engineTimeMs
        if self.pushTimeMs is not None:
            _rval[Y_PUSHTIMEMS] = self.pushTimeMs
        if self.publishTimeMs is not None:
            _rval[Y_PUBLISHTIMEMS] = self.publishTimeMs
        if self.saveTimeMs is not None:
            _rval[Y_SAVETIMEMS] = self.saveTimeMs
        if self.totalTimeMs is not None:
            _rval[Y_TOTALTIMEMS] = self.totalTimeMs
        if self.appSummary is not None:
            _rval[Y_APPSUMMARY] = [x.to_input() for x in self.appSummary]
        return _rval

    @staticmethod
    def from_input(obj) -> 'ExecutionSummary | None':
        if obj:
            _inputResourceCount = obj.get(Y_INPUTRESOURCECOUNT)
            _targetsModified = []
            if obj.get(Y_TARGETSMODIFIED) is not None:
                for x in obj.get(Y_TARGETSMODIFIED):
                    _targetsModified.append(TargetSummary.from_input(x))
            _targetsModifiedCount = obj.get(Y_TARGETSMODIFIEDCOUNT)
            _engineTimeMs = obj.get(Y_ENGINETIMEMS)
            _pushTimeMs = obj.get(Y_PUSHTIMEMS)
            _publishTimeMs = obj.get(Y_PUBLISHTIMEMS)
            _saveTimeMs = obj.get(Y_SAVETIMEMS)
            _totalTimeMs = obj.get(Y_TOTALTIMEMS)
            _appSummary = []
            if obj.get(Y_APPSUMMARY) is not None:
                for x in obj.get(Y_APPSUMMARY):
                    _appSummary.append(AppSummary.from_input(x))
            return ExecutionSummary(
                inputResourceCount=_inputResourceCount,
                targetsModified=_targetsModified,
                targetsModifiedCount=_targetsModifiedCount,
                engineTimeMs=_engineTimeMs,
                pushTimeMs=_pushTimeMs,
                publishTimeMs=_publishTimeMs,
                saveTimeMs=_saveTimeMs,
                totalTimeMs=_totalTimeMs,
                appSummary=_appSummary,
            )
        return None  # pragma: no cover


class TargetErrors:
    def __init__(
        self,
        namespace: str,
        name: str,
        errors: list[str] | None = None,
    ):
        self.namespace = namespace
        self.name = name
        self.errors = errors

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.namespace is not None:
            _rval[Y_NAMESPACE] = self.namespace
        if self.name is not None:
            _rval[Y_NAME] = self.name
        if self.errors is not None:
            _rval[Y_ERRORS] = self.errors
        return _rval

    @staticmethod
    def from_input(obj) -> 'TargetErrors | None':
        if obj:
            _namespace = obj.get(Y_NAMESPACE)
            _name = obj.get(Y_NAME)
            _errors = obj.get(Y_ERRORS)
            return TargetErrors(
                namespace=_namespace,
                name=_name,
                errors=_errors,
            )
        return None  # pragma: no cover


class TransactionResource:
    def __init__(
        self,
        namespace: str,
        gvk: str,
        name: str,
        action: str | None = None,
    ):
        self.namespace = namespace
        self.gvk = gvk
        self.name = name
        self.action = action

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.namespace is not None:
            _rval[Y_NAMESPACE] = self.namespace
        if self.gvk is not None:
            _rval[Y_GVK] = self.gvk
        if self.name is not None:
            _rval[Y_NAME] = self.name
        if self.action is not None:
            _rval[Y_ACTION] = self.action
        return _rval

    @staticmethod
    def from_input(obj) -> 'TransactionResource | None':
        if obj:
            _namespace = obj.get(Y_NAMESPACE)
            _gvk = obj.get(Y_GVK)
            _name = obj.get(Y_NAME)
            _action = obj.get(Y_ACTION)
            return TransactionResource(
                namespace=_namespace,
                gvk=_gvk,
                name=_name,
                action=_action,
            )
        return None  # pragma: no cover


class TransactionResultSpec:
    def __init__(
        self,
        description: str | None = None,
        dryRun: bool | None = None,
        inputResources: list[TransactionResource] | None = None,
        applicationErrors: list[ApplicationErrors] | None = None,
        generalErrors: list[str] | None = None,
        targetErrors: list[TargetErrors] | None = None,
        result: str | None = None,
        executionSummary: ExecutionSummary | None = None,
        commit: str | None = None,
        username: str | None = None,
        timestamp: object | None = None,
        bundledTransactionId: int | None = None,
    ):
        self.description = description
        self.dryRun = dryRun
        self.inputResources = inputResources
        self.applicationErrors = applicationErrors
        self.generalErrors = generalErrors
        self.targetErrors = targetErrors
        self.result = result
        self.executionSummary = executionSummary
        self.commit = commit
        self.username = username
        self.timestamp = timestamp
        self.bundledTransactionId = bundledTransactionId

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.description is not None:
            _rval[Y_DESCRIPTION] = self.description
        if self.dryRun is not None:
            _rval[Y_DRYRUN] = self.dryRun
        if self.inputResources is not None:
            _rval[Y_INPUTRESOURCES] = [x.to_input() for x in self.inputResources]
        if self.applicationErrors is not None:
            _rval[Y_APPLICATIONERRORS] = [x.to_input() for x in self.applicationErrors]
        if self.generalErrors is not None:
            _rval[Y_GENERALERRORS] = self.generalErrors
        if self.targetErrors is not None:
            _rval[Y_TARGETERRORS] = [x.to_input() for x in self.targetErrors]
        if self.result is not None:
            _rval[Y_RESULT] = self.result
        if self.executionSummary is not None:
            _rval[Y_EXECUTIONSUMMARY] = self.executionSummary.to_input()
        if self.commit is not None:
            _rval[Y_COMMIT] = self.commit
        if self.username is not None:
            _rval[Y_USERNAME] = self.username
        if self.timestamp is not None:
            _rval[Y_TIMESTAMP] = self.timestamp
        if self.bundledTransactionId is not None:
            _rval[Y_BUNDLEDTRANSACTIONID] = self.bundledTransactionId
        return _rval

    @staticmethod
    def from_input(obj) -> 'TransactionResultSpec | None':
        if obj:
            _description = obj.get(Y_DESCRIPTION)
            _dryRun = obj.get(Y_DRYRUN)
            _inputResources = []
            if obj.get(Y_INPUTRESOURCES) is not None:
                for x in obj.get(Y_INPUTRESOURCES):
                    _inputResources.append(TransactionResource.from_input(x))
            _applicationErrors = []
            if obj.get(Y_APPLICATIONERRORS) is not None:
                for x in obj.get(Y_APPLICATIONERRORS):
                    _applicationErrors.append(ApplicationErrors.from_input(x))
            _generalErrors = obj.get(Y_GENERALERRORS)
            _targetErrors = []
            if obj.get(Y_TARGETERRORS) is not None:
                for x in obj.get(Y_TARGETERRORS):
                    _targetErrors.append(TargetErrors.from_input(x))
            _result = obj.get(Y_RESULT)
            _executionSummary = ExecutionSummary.from_input(obj.get(Y_EXECUTIONSUMMARY))
            _commit = obj.get(Y_COMMIT)
            _username = obj.get(Y_USERNAME)
            _timestamp = obj.get(Y_TIMESTAMP)
            _bundledTransactionId = obj.get(Y_BUNDLEDTRANSACTIONID)
            return TransactionResultSpec(
                description=_description,
                dryRun=_dryRun,
                inputResources=_inputResources,
                applicationErrors=_applicationErrors,
                generalErrors=_generalErrors,
                targetErrors=_targetErrors,
                result=_result,
                executionSummary=_executionSummary,
                commit=_commit,
                username=_username,
                timestamp=_timestamp,
                bundledTransactionId=_bundledTransactionId,
            )
        return None  # pragma: no cover


class TransactionResultStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'TransactionResultStatus | None':
        if obj:
            return TransactionResultStatus(
            )
        return None  # pragma: no cover


class TransactionResult:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: TransactionResultSpec | None = None,
        status: TransactionResultStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = TRANSACTIONRESULT_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'TransactionResult | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = TransactionResultSpec.from_input(obj.get(Y_SPEC, None))
            _status = TransactionResultStatus.from_input(obj.get(Y_STATUS))
            return TransactionResult(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class TransactionResultList:
    def __init__(
        self,
        items: list[TransactionResult],
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
    def from_input(obj) -> 'TransactionResultList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return TransactionResultList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
