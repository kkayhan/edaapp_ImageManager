#!/usr/bin/env python3
# Auto-generated classes based on your _types.go file (with special logic for CRDs that embed metav1.ObjectMeta)
# The change on this file will be overwritten by running edabuilder create or generate.
import eda_common as eda

from . import Metadata, Y_NAME

from .constants import *
from .engineconfig import KubernetesExports, KubernetesImports

ENUM_UICOMMONPANEL_MAIN = 'main'
ENUM_UICOMMONPANEL_SYSTEM_ADMINISTRATION = 'system_administration'
ENUM_UICOMMONPANEL_ = ''

ENUM_SCRIPTTYPE_CONFIG = 'config'
ENUM_SCRIPTTYPE_STATE = 'state'

ENUM_CRDAPIEXPOSE_NONE = 'none'
ENUM_CRDAPIEXPOSE_READ = 'read'
ENUM_CRDAPIEXPOSE_READWRITE = 'readWrite'

ENUM_CRDKUBERNETESIMPORTPOLICY_ALL = 'all'
ENUM_CRDKUBERNETESIMPORTPOLICY_SPEC = 'spec'
ENUM_CRDKUBERNETESIMPORTPOLICY_ = ''

ENUM_CRDKUBERNETESEXPORTPOLICY_ALL = 'all'
ENUM_CRDKUBERNETESEXPORTPOLICY_ = ''

ENUM_CRDRESOURCETYPE_TRANSACTIONAL = 'Transactional'
ENUM_CRDRESOURCETYPE_KUBERNETES = 'Kubernetes'

ENUM_REQUIREKUBERNETESIMPORTSPOLICY_ALL = 'all'
ENUM_REQUIREKUBERNETESIMPORTSPOLICY_SPEC = 'spec'
ENUM_REQUIREKUBERNETESIMPORTSPOLICY_ = ''

ENUM_REQUIREKUBERNETESEXPORTSPOLICY_ALL = 'all'
ENUM_REQUIREKUBERNETESEXPORTSPOLICY_SPEC = 'spec'
ENUM_REQUIREKUBERNETESEXPORTSPOLICY_ = ''

ENUM_REQUIREMENTSTATE_PRESENT = 'Present'
ENUM_REQUIREMENTSTATE_ABSENT = 'Absent'
Y_KIND = 'kind'
Y_PATH = 'path'
Y_README = 'readme'
Y_SOURCE = 'source'
Y_DOCUMENTATION = 'documentation'
Y_LICENSE = 'license'
Y_SCREENSHOTS = 'screenshots'
Y_OCISPECVERSION = 'ociSpecVersion'
Y_SRCURI = 'srcURI'
Y_CATEGORIES = 'categories'
Y_SETTINGS = 'settings'
Y_CHANGELOG = 'changelog'
Y_SUPPORT = 'support'
Y_CATEGORY = 'category'
Y_PANEL = 'panel'
Y_ICON = 'icon'
Y_DESTINATION = 'destination'
Y_UI = 'ui'
Y_TYPE = 'type'
Y_TRIGGER = 'trigger'
Y_EXPOSE = 'expose'
Y_IMPORTPOLICY = 'importPolicy'
Y_EXPORTPOLICY = 'exportPolicy'
Y_PLURAL = 'plural'
Y_SINGULAR = 'singular'
Y_LISTKIND = 'listKind'
Y_MATCHTAGS = 'matchTags'
Y_NAMES = 'names'
Y_SCHEMA = 'schema'
Y_API = 'api'
Y_RESOURCETYPE = 'resourceType'
Y_KUBERNETES = 'kubernetes'
Y_NAMESPACED = 'namespaced'
Y_WORKFLOW = 'workflow'
Y_CONVERSIONSCRIPT = 'conversionScript'
Y_AI = 'ai'
Y_TABLE = 'table'
Y_IMAGE = 'image'
Y_DEFINITION = 'definition'
Y_PULLSECRET = 'pullSecret'
Y_POLICY = 'policy'
Y_IMPORTS = 'imports'
Y_EXPORTS = 'exports'
Y_APPID = 'appId'
Y_APPNAME = 'appName'
Y_VENDOR = 'vendor'
Y_VERSION = 'version'
Y_STATE = 'state'
Y_CONTAINER = 'container'
Y_ARTIFACT = 'artifact'
Y_FILE = 'file'
Y_CRD = 'crd'
Y_CR = 'cr'
Y_BOOTSTRAPRESOURCE = 'bootstrapResource'
Y_SCRIPT = 'script'
Y_VIEW = 'view'
Y_DBSCHEMA = 'dbSchema'
Y_I18N = 'i18n'
Y_GROUP = 'group'
Y_TITLE = 'title'
Y_DESCRIPTION = 'description'
Y_SUPPORTEDENDPOINTS = 'supportedEndpoints'
Y_SUPPORTEDCOREVERSIONS = 'supportedCoreVersions'
Y_REQUIREMENTS = 'requirements'
Y_AUTHOR = 'author'
Y_APPINFO = 'appInfo'
Y_COMPONENTS = 'components'
Y_DEPENDENCIES = 'dependencies'
Y_GITREFERENCE = 'gitReference'
Y_GITPATHPREFIX = 'gitPathPrefix'
# Package objects (GVK Schemas)
MANIFEST_SCHEMA = eda.Schema(group='core.eda.nokia.com', version='v1', kind='Manifest')


class AI:
    def __init__(
        self,
        matchTags: list[str] | None = None,
    ):
        self.matchTags = matchTags

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.matchTags is not None:
            _rval[Y_MATCHTAGS] = self.matchTags
        return _rval

    @staticmethod
    def from_input(obj) -> 'AI | None':
        if obj:
            _matchTags = obj.get(Y_MATCHTAGS)
            return AI(
                matchTags=_matchTags,
            )
        return None  # pragma: no cover


class AppInfo:
    def __init__(
        self,
        readme: str | None = None,
        source: str | None = None,
        documentation: str | None = None,
        license: str | None = None,
        screenshots: list[str] | None = None,
        ociSpecVersion: str | None = None,
        srcURI: str | None = None,
        categories: list[str] | None = None,
        settings: str | None = None,
        changelog: str | None = None,
        support: str | None = None,
    ):
        self.readme = readme
        self.source = source
        self.documentation = documentation
        self.license = license
        self.screenshots = screenshots
        self.ociSpecVersion = ociSpecVersion
        self.srcURI = srcURI
        self.categories = categories
        self.settings = settings
        self.changelog = changelog
        self.support = support

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.readme is not None:
            _rval[Y_README] = self.readme
        if self.source is not None:
            _rval[Y_SOURCE] = self.source
        if self.documentation is not None:
            _rval[Y_DOCUMENTATION] = self.documentation
        if self.license is not None:
            _rval[Y_LICENSE] = self.license
        if self.screenshots is not None:
            _rval[Y_SCREENSHOTS] = self.screenshots
        if self.ociSpecVersion is not None:
            _rval[Y_OCISPECVERSION] = self.ociSpecVersion
        if self.srcURI is not None:
            _rval[Y_SRCURI] = self.srcURI
        if self.categories is not None:
            _rval[Y_CATEGORIES] = self.categories
        if self.settings is not None:
            _rval[Y_SETTINGS] = self.settings
        if self.changelog is not None:
            _rval[Y_CHANGELOG] = self.changelog
        if self.support is not None:
            _rval[Y_SUPPORT] = self.support
        return _rval

    @staticmethod
    def from_input(obj) -> 'AppInfo | None':
        if obj:
            _readme = obj.get(Y_README)
            _source = obj.get(Y_SOURCE)
            _documentation = obj.get(Y_DOCUMENTATION)
            _license = obj.get(Y_LICENSE)
            _screenshots = obj.get(Y_SCREENSHOTS)
            _ociSpecVersion = obj.get(Y_OCISPECVERSION)
            _srcURI = obj.get(Y_SRCURI)
            _categories = obj.get(Y_CATEGORIES)
            _settings = obj.get(Y_SETTINGS)
            _changelog = obj.get(Y_CHANGELOG)
            _support = obj.get(Y_SUPPORT)
            return AppInfo(
                readme=_readme,
                source=_source,
                documentation=_documentation,
                license=_license,
                screenshots=_screenshots,
                ociSpecVersion=_ociSpecVersion,
                srcURI=_srcURI,
                categories=_categories,
                settings=_settings,
                changelog=_changelog,
                support=_support,
            )
        return None  # pragma: no cover


class Artifact:
    def __init__(
        self,
        path: str,
        destination: str | None = None,
    ):
        self.path = path
        self.destination = destination

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.path is not None:
            _rval[Y_PATH] = self.path
        if self.destination is not None:
            _rval[Y_DESTINATION] = self.destination
        return _rval

    @staticmethod
    def from_input(obj) -> 'Artifact | None':
        if obj:
            _path = obj.get(Y_PATH)
            _destination = obj.get(Y_DESTINATION)
            return Artifact(
                path=_path,
                destination=_destination,
            )
        return None  # pragma: no cover


class CR:
    def __init__(
        self,
        path: str,
    ):
        self.path = path

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.path is not None:
            _rval[Y_PATH] = self.path
        return _rval

    @staticmethod
    def from_input(obj) -> 'CR | None':
        if obj:
            _path = obj.get(Y_PATH)
            return CR(
                path=_path,
            )
        return None  # pragma: no cover


class CRDApi:
    def __init__(
        self,
        expose: str | None = None,
    ):
        self.expose = expose

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.expose is not None:
            _rval[Y_EXPOSE] = self.expose
        return _rval

    @staticmethod
    def from_input(obj) -> 'CRDApi | None':
        if obj:
            _expose = obj.get(Y_EXPOSE, "readWrite")
            return CRDApi(
                expose=_expose,
            )
        return None  # pragma: no cover


class CRDKubernetes:
    def __init__(
        self,
        importPolicy: str | None = None,
        exportPolicy: str | None = None,
    ):
        self.importPolicy = importPolicy
        self.exportPolicy = exportPolicy

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.importPolicy is not None:
            _rval[Y_IMPORTPOLICY] = self.importPolicy
        if self.exportPolicy is not None:
            _rval[Y_EXPORTPOLICY] = self.exportPolicy
        return _rval

    @staticmethod
    def from_input(obj) -> 'CRDKubernetes | None':
        if obj:
            _importPolicy = obj.get(Y_IMPORTPOLICY)
            _exportPolicy = obj.get(Y_EXPORTPOLICY)
            return CRDKubernetes(
                importPolicy=_importPolicy,
                exportPolicy=_exportPolicy,
            )
        return None  # pragma: no cover


class CRDNames:
    def __init__(
        self,
        plural: str,
        singular: str,
        kind: str,
        listKind: str,
    ):
        self.plural = plural
        self.singular = singular
        self.kind = kind
        self.listKind = listKind

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.plural is not None:
            _rval[Y_PLURAL] = self.plural
        if self.singular is not None:
            _rval[Y_SINGULAR] = self.singular
        if self.kind is not None:
            _rval[Y_KIND] = self.kind
        if self.listKind is not None:
            _rval[Y_LISTKIND] = self.listKind
        return _rval

    @staticmethod
    def from_input(obj) -> 'CRDNames | None':
        if obj:
            _plural = obj.get(Y_PLURAL)
            _singular = obj.get(Y_SINGULAR)
            _kind = obj.get(Y_KIND)
            _listKind = obj.get(Y_LISTKIND)
            return CRDNames(
                plural=_plural,
                singular=_singular,
                kind=_kind,
                listKind=_listKind,
            )
        return None  # pragma: no cover


class UICommon:
    def __init__(
        self,
        name: str,
        category: str | None = None,
        panel: str | None = None,
        icon: str | None = None,
    ):
        self.name = name
        self.category = category
        self.panel = panel
        self.icon = icon

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.name is not None:
            _rval[Y_NAME] = self.name
        if self.category is not None:
            _rval[Y_CATEGORY] = self.category
        if self.panel is not None:
            _rval[Y_PANEL] = self.panel
        if self.icon is not None:
            _rval[Y_ICON] = self.icon
        return _rval

    @staticmethod
    def from_input(obj) -> 'UICommon | None':
        if obj:
            _name = obj.get(Y_NAME)
            _category = obj.get(Y_CATEGORY)
            _panel = obj.get(Y_PANEL)
            _icon = obj.get(Y_ICON)
            return UICommon(
                name=_name,
                category=_category,
                panel=_panel,
                icon=_icon,
            )
        return None  # pragma: no cover


class CRD:
    def __init__(
        self,
        path: str,
        names: CRDNames | None = None,
        schema: str | None = None,
        api: CRDApi | None = None,
        resourceType: str | None = None,
        kubernetes: CRDKubernetes | None = None,
        ui: UICommon | None = None,
        namespaced: bool | None = None,
        workflow: bool | None = None,
        conversionScript: str | None = None,
        ai: AI | None = None,
    ):
        self.path = path
        self.names = names
        self.schema = schema
        self.api = api
        self.resourceType = resourceType
        self.kubernetes = kubernetes
        self.ui = ui
        self.namespaced = namespaced
        self.workflow = workflow
        self.conversionScript = conversionScript
        self.ai = ai

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.path is not None:
            _rval[Y_PATH] = self.path
        if self.names is not None:
            _rval[Y_NAMES] = self.names.to_input()
        if self.schema is not None:
            _rval[Y_SCHEMA] = self.schema
        if self.api is not None:
            _rval[Y_API] = self.api.to_input()
        if self.resourceType is not None:
            _rval[Y_RESOURCETYPE] = self.resourceType
        if self.kubernetes is not None:
            _rval[Y_KUBERNETES] = self.kubernetes.to_input()
        if self.ui is not None:
            _rval[Y_UI] = self.ui.to_input()
        if self.namespaced is not None:
            _rval[Y_NAMESPACED] = self.namespaced
        if self.workflow is not None:
            _rval[Y_WORKFLOW] = self.workflow
        if self.conversionScript is not None:
            _rval[Y_CONVERSIONSCRIPT] = self.conversionScript
        if self.ai is not None:
            _rval[Y_AI] = self.ai.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'CRD | None':
        if obj:
            _path = obj.get(Y_PATH)
            _names = CRDNames.from_input(obj.get(Y_NAMES))
            _schema = obj.get(Y_SCHEMA)
            _api = CRDApi.from_input(obj.get(Y_API))
            _resourceType = obj.get(Y_RESOURCETYPE)
            _kubernetes = CRDKubernetes.from_input(obj.get(Y_KUBERNETES))
            _ui = UICommon.from_input(obj.get(Y_UI))
            _namespaced = obj.get(Y_NAMESPACED, True)
            _workflow = obj.get(Y_WORKFLOW)
            _conversionScript = obj.get(Y_CONVERSIONSCRIPT)
            _ai = AI.from_input(obj.get(Y_AI))
            return CRD(
                path=_path,
                names=_names,
                schema=_schema,
                api=_api,
                resourceType=_resourceType,
                kubernetes=_kubernetes,
                ui=_ui,
                namespaced=_namespaced,
                workflow=_workflow,
                conversionScript=_conversionScript,
                ai=_ai,
            )
        return None  # pragma: no cover


class Container:
    def __init__(
        self,
        image: str,
        name: str,
        pullSecret: str | None = None,
    ):
        self.image = image
        self.name = name
        self.pullSecret = pullSecret

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.image is not None:
            _rval[Y_IMAGE] = self.image
        if self.name is not None:
            _rval[Y_NAME] = self.name
        if self.pullSecret is not None:
            _rval[Y_PULLSECRET] = self.pullSecret
        return _rval

    @staticmethod
    def from_input(obj) -> 'Container | None':
        if obj:
            _image = obj.get(Y_IMAGE)
            _name = obj.get(Y_NAME)
            _pullSecret = obj.get(Y_PULLSECRET)
            return Container(
                image=_image,
                name=_name,
                pullSecret=_pullSecret,
            )
        return None  # pragma: no cover


class DBSchema:
    def __init__(
        self,
        table: str,
        schema: str,
    ):
        self.table = table
        self.schema = schema

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.table is not None:
            _rval[Y_TABLE] = self.table
        if self.schema is not None:
            _rval[Y_SCHEMA] = self.schema
        return _rval

    @staticmethod
    def from_input(obj) -> 'DBSchema | None':
        if obj:
            _table = obj.get(Y_TABLE)
            _schema = obj.get(Y_SCHEMA)
            return DBSchema(
                table=_table,
                schema=_schema,
            )
        return None  # pragma: no cover


class I18n:
    def __init__(
        self,
        path: str,
    ):
        self.path = path

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.path is not None:
            _rval[Y_PATH] = self.path
        return _rval

    @staticmethod
    def from_input(obj) -> 'I18n | None':
        if obj:
            _path = obj.get(Y_PATH)
            return I18n(
                path=_path,
            )
        return None  # pragma: no cover


class ManifestWorkflow:
    def __init__(
        self,
        image: str,
        definition: str,
    ):
        self.image = image
        self.definition = definition

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.image is not None:
            _rval[Y_IMAGE] = self.image
        if self.definition is not None:
            _rval[Y_DEFINITION] = self.definition
        return _rval

    @staticmethod
    def from_input(obj) -> 'ManifestWorkflow | None':
        if obj:
            _image = obj.get(Y_IMAGE)
            _definition = obj.get(Y_DEFINITION)
            return ManifestWorkflow(
                image=_image,
                definition=_definition,
            )
        return None  # pragma: no cover


class Panel:
    def __init__(
        self,
        path: str,
        name: str,
    ):
        self.path = path
        self.name = name

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.path is not None:
            _rval[Y_PATH] = self.path
        if self.name is not None:
            _rval[Y_NAME] = self.name
        return _rval

    @staticmethod
    def from_input(obj) -> 'Panel | None':
        if obj:
            _path = obj.get(Y_PATH)
            _name = obj.get(Y_NAME)
            return Panel(
                path=_path,
                name=_name,
            )
        return None  # pragma: no cover


class ScriptEngineTrigger:
    def __init__(
        self,
        kind: str,
    ):
        self.kind = kind

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.kind is not None:
            _rval[Y_KIND] = self.kind
        return _rval

    @staticmethod
    def from_input(obj) -> 'ScriptEngineTrigger | None':
        if obj:
            _kind = obj.get(Y_KIND)
            return ScriptEngineTrigger(
                kind=_kind,
            )
        return None  # pragma: no cover


class Script:
    def __init__(
        self,
        path: str,
        trigger: ScriptEngineTrigger,
        type: str | None = None,
    ):
        self.path = path
        self.trigger = trigger
        self.type = type

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.path is not None:
            _rval[Y_PATH] = self.path
        if self.trigger is not None:
            _rval[Y_TRIGGER] = self.trigger.to_input()
        if self.type is not None:
            _rval[Y_TYPE] = self.type
        return _rval

    @staticmethod
    def from_input(obj) -> 'Script | None':
        if obj:
            _path = obj.get(Y_PATH)
            _trigger = ScriptEngineTrigger.from_input(obj.get(Y_TRIGGER))
            _type = obj.get(Y_TYPE)
            return Script(
                path=_path,
                trigger=_trigger,
                type=_type,
            )
        return None  # pragma: no cover


class View:
    def __init__(
        self,
        path: str,
        ui: UICommon,
    ):
        self.path = path
        self.ui = ui

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.path is not None:
            _rval[Y_PATH] = self.path
        if self.ui is not None:
            _rval[Y_UI] = self.ui.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'View | None':
        if obj:
            _path = obj.get(Y_PATH)
            _ui = UICommon.from_input(obj.get(Y_UI))
            return View(
                path=_path,
                ui=_ui,
            )
        return None  # pragma: no cover


class ManifestComponent:
    def __init__(
        self,
        crd: CRD | None = None,
        cr: CR | None = None,
        bootstrapResource: CR | None = None,
        script: Script | None = None,
        view: View | None = None,
        panel: Panel | None = None,
        dbSchema: DBSchema | None = None,
        workflow: ManifestWorkflow | None = None,
        i18n: I18n | None = None,
    ):
        self.crd = crd
        self.cr = cr
        self.bootstrapResource = bootstrapResource
        self.script = script
        self.view = view
        self.panel = panel
        self.dbSchema = dbSchema
        self.workflow = workflow
        self.i18n = i18n

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.crd is not None:
            _rval[Y_CRD] = self.crd.to_input()
        if self.cr is not None:
            _rval[Y_CR] = self.cr.to_input()
        if self.bootstrapResource is not None:
            _rval[Y_BOOTSTRAPRESOURCE] = self.bootstrapResource.to_input()
        if self.script is not None:
            _rval[Y_SCRIPT] = self.script.to_input()
        if self.view is not None:
            _rval[Y_VIEW] = self.view.to_input()
        if self.panel is not None:
            _rval[Y_PANEL] = self.panel.to_input()
        if self.dbSchema is not None:
            _rval[Y_DBSCHEMA] = self.dbSchema.to_input()
        if self.workflow is not None:
            _rval[Y_WORKFLOW] = self.workflow.to_input()
        if self.i18n is not None:
            _rval[Y_I18N] = self.i18n.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'ManifestComponent | None':
        if obj:
            _crd = CRD.from_input(obj.get(Y_CRD))
            _cr = CR.from_input(obj.get(Y_CR))
            _bootstrapResource = CR.from_input(obj.get(Y_BOOTSTRAPRESOURCE))
            _script = Script.from_input(obj.get(Y_SCRIPT))
            _view = View.from_input(obj.get(Y_VIEW))
            _panel = Panel.from_input(obj.get(Y_PANEL))
            _dbSchema = DBSchema.from_input(obj.get(Y_DBSCHEMA))
            _workflow = ManifestWorkflow.from_input(obj.get(Y_WORKFLOW))
            _i18n = I18n.from_input(obj.get(Y_I18N))
            return ManifestComponent(
                crd=_crd,
                cr=_cr,
                bootstrapResource=_bootstrapResource,
                script=_script,
                view=_view,
                panel=_panel,
                dbSchema=_dbSchema,
                workflow=_workflow,
                i18n=_i18n,
            )
        return None  # pragma: no cover


class PackagedFile:
    def __init__(
        self,
        path: str,
    ):
        self.path = path

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.path is not None:
            _rval[Y_PATH] = self.path
        return _rval

    @staticmethod
    def from_input(obj) -> 'PackagedFile | None':
        if obj:
            _path = obj.get(Y_PATH)
            return PackagedFile(
                path=_path,
            )
        return None  # pragma: no cover


class ManifestDependency:
    def __init__(
        self,
        container: Container | None = None,
        artifact: Artifact | None = None,
        file: PackagedFile | None = None,
    ):
        self.container = container
        self.artifact = artifact
        self.file = file

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.container is not None:
            _rval[Y_CONTAINER] = self.container.to_input()
        if self.artifact is not None:
            _rval[Y_ARTIFACT] = self.artifact.to_input()
        if self.file is not None:
            _rval[Y_FILE] = self.file.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'ManifestDependency | None':
        if obj:
            _container = Container.from_input(obj.get(Y_CONTAINER))
            _artifact = Artifact.from_input(obj.get(Y_ARTIFACT))
            _file = PackagedFile.from_input(obj.get(Y_FILE))
            return ManifestDependency(
                container=_container,
                artifact=_artifact,
                file=_file,
            )
        return None  # pragma: no cover


class RequirementKubernetes:
    def __init__(
        self,
        imports: list[KubernetesImports] | None = None,
        exports: list[KubernetesExports] | None = None,
    ):
        self.imports = imports
        self.exports = exports

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.imports is not None:
            _rval[Y_IMPORTS] = [x.to_input() for x in self.imports]
        if self.exports is not None:
            _rval[Y_EXPORTS] = [x.to_input() for x in self.exports]
        return _rval

    @staticmethod
    def from_input(obj) -> 'RequirementKubernetes | None':
        if obj:
            _imports = []
            if obj.get(Y_IMPORTS) is not None:
                for x in obj.get(Y_IMPORTS):
                    _imports.append(KubernetesImports.from_input(x))
            _exports = []
            if obj.get(Y_EXPORTS) is not None:
                for x in obj.get(Y_EXPORTS):
                    _exports.append(KubernetesExports.from_input(x))
            return RequirementKubernetes(
                imports=_imports,
                exports=_exports,
            )
        return None  # pragma: no cover


class Requirement:
    def __init__(
        self,
        appId: str,
        appName: str,
        vendor: str,
        version: str,
        state: str | None = None,
        kubernetes: RequirementKubernetes | None = None,
    ):
        self.appId = appId
        self.appName = appName
        self.vendor = vendor
        self.version = version
        self.state = state
        self.kubernetes = kubernetes

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.appId is not None:
            _rval[Y_APPID] = self.appId
        if self.appName is not None:
            _rval[Y_APPNAME] = self.appName
        if self.vendor is not None:
            _rval[Y_VENDOR] = self.vendor
        if self.version is not None:
            _rval[Y_VERSION] = self.version
        if self.state is not None:
            _rval[Y_STATE] = self.state
        if self.kubernetes is not None:
            _rval[Y_KUBERNETES] = self.kubernetes.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'Requirement | None':
        if obj:
            _appId = obj.get(Y_APPID)
            _appName = obj.get(Y_APPNAME)
            _vendor = obj.get(Y_VENDOR)
            _version = obj.get(Y_VERSION)
            _state = obj.get(Y_STATE, "Present")
            _kubernetes = RequirementKubernetes.from_input(obj.get(Y_KUBERNETES))
            return Requirement(
                appId=_appId,
                appName=_appName,
                vendor=_vendor,
                version=_version,
                state=_state,
                kubernetes=_kubernetes,
            )
        return None  # pragma: no cover


class ManifestSpec:
    def __init__(
        self,
        group: str,
        version: str,
        title: str,
        supportedCoreVersions: list[str],
        description: str | None = None,
        supportedEndpoints: list[str] | None = None,
        requirements: list[Requirement] | None = None,
        author: str | None = None,
        appInfo: AppInfo | None = None,
        components: list[ManifestComponent] | None = None,
        dependencies: list[ManifestDependency] | None = None,
        image: str | None = None,
        gitReference: str | None = None,
        gitPathPrefix: str | None = None,
    ):
        self.group = group
        self.version = version
        self.title = title
        self.supportedCoreVersions = supportedCoreVersions
        self.description = description
        self.supportedEndpoints = supportedEndpoints
        self.requirements = requirements
        self.author = author
        self.appInfo = appInfo
        self.components = components
        self.dependencies = dependencies
        self.image = image
        self.gitReference = gitReference
        self.gitPathPrefix = gitPathPrefix

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.group is not None:
            _rval[Y_GROUP] = self.group
        if self.version is not None:
            _rval[Y_VERSION] = self.version
        if self.title is not None:
            _rval[Y_TITLE] = self.title
        if self.supportedCoreVersions is not None:
            _rval[Y_SUPPORTEDCOREVERSIONS] = self.supportedCoreVersions
        if self.description is not None:
            _rval[Y_DESCRIPTION] = self.description
        if self.supportedEndpoints is not None:
            _rval[Y_SUPPORTEDENDPOINTS] = self.supportedEndpoints
        if self.requirements is not None:
            _rval[Y_REQUIREMENTS] = [x.to_input() for x in self.requirements]
        if self.author is not None:
            _rval[Y_AUTHOR] = self.author
        if self.appInfo is not None:
            _rval[Y_APPINFO] = self.appInfo.to_input()
        if self.components is not None:
            _rval[Y_COMPONENTS] = [x.to_input() for x in self.components]
        if self.dependencies is not None:
            _rval[Y_DEPENDENCIES] = [x.to_input() for x in self.dependencies]
        if self.image is not None:
            _rval[Y_IMAGE] = self.image
        if self.gitReference is not None:
            _rval[Y_GITREFERENCE] = self.gitReference
        if self.gitPathPrefix is not None:
            _rval[Y_GITPATHPREFIX] = self.gitPathPrefix
        return _rval

    @staticmethod
    def from_input(obj) -> 'ManifestSpec | None':
        if obj:
            _group = obj.get(Y_GROUP)
            _version = obj.get(Y_VERSION)
            _title = obj.get(Y_TITLE)
            _supportedCoreVersions = obj.get(Y_SUPPORTEDCOREVERSIONS)
            _description = obj.get(Y_DESCRIPTION)
            _supportedEndpoints = obj.get(Y_SUPPORTEDENDPOINTS)
            _requirements = []
            if obj.get(Y_REQUIREMENTS) is not None:
                for x in obj.get(Y_REQUIREMENTS):
                    _requirements.append(Requirement.from_input(x))
            _author = obj.get(Y_AUTHOR)
            _appInfo = AppInfo.from_input(obj.get(Y_APPINFO))
            _components = []
            if obj.get(Y_COMPONENTS) is not None:
                for x in obj.get(Y_COMPONENTS):
                    _components.append(ManifestComponent.from_input(x))
            _dependencies = []
            if obj.get(Y_DEPENDENCIES) is not None:
                for x in obj.get(Y_DEPENDENCIES):
                    _dependencies.append(ManifestDependency.from_input(x))
            _image = obj.get(Y_IMAGE)
            _gitReference = obj.get(Y_GITREFERENCE)
            _gitPathPrefix = obj.get(Y_GITPATHPREFIX)
            return ManifestSpec(
                group=_group,
                version=_version,
                title=_title,
                supportedCoreVersions=_supportedCoreVersions,
                description=_description,
                supportedEndpoints=_supportedEndpoints,
                requirements=_requirements,
                author=_author,
                appInfo=_appInfo,
                components=_components,
                dependencies=_dependencies,
                image=_image,
                gitReference=_gitReference,
                gitPathPrefix=_gitPathPrefix,
            )
        return None  # pragma: no cover


class ManifestStatus:
    def __init__(
        self,
    ):
        pass

    def to_input(self):  # pragma: no cover
        _rval = {}
        return _rval

    @staticmethod
    def from_input(obj) -> 'ManifestStatus | None':
        if obj:
            return ManifestStatus(
            )
        return None  # pragma: no cover


class Path:
    def __init__(
        self,
        path: str,
    ):
        self.path = path

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.path is not None:
            _rval[Y_PATH] = self.path
        return _rval

    @staticmethod
    def from_input(obj) -> 'Path | None':
        if obj:
            _path = obj.get(Y_PATH)
            return Path(
                path=_path,
            )
        return None  # pragma: no cover


class RequireKubernetesExports:
    def __init__(
        self,
        kind: str,
        policy: str,
    ):
        self.kind = kind
        self.policy = policy

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.kind is not None:
            _rval[Y_KIND] = self.kind
        if self.policy is not None:
            _rval[Y_POLICY] = self.policy
        return _rval

    @staticmethod
    def from_input(obj) -> 'RequireKubernetesExports | None':
        if obj:
            _kind = obj.get(Y_KIND)
            _policy = obj.get(Y_POLICY)
            return RequireKubernetesExports(
                kind=_kind,
                policy=_policy,
            )
        return None  # pragma: no cover


class RequireKubernetesImports:
    def __init__(
        self,
        kind: str,
        policy: str,
    ):
        self.kind = kind
        self.policy = policy

    def to_input(self):  # pragma: no cover
        _rval = {}
        if self.kind is not None:
            _rval[Y_KIND] = self.kind
        if self.policy is not None:
            _rval[Y_POLICY] = self.policy
        return _rval

    @staticmethod
    def from_input(obj) -> 'RequireKubernetesImports | None':
        if obj:
            _kind = obj.get(Y_KIND)
            _policy = obj.get(Y_POLICY)
            return RequireKubernetesImports(
                kind=_kind,
                policy=_policy,
            )
        return None  # pragma: no cover


class Manifest:
    def __init__(
        self,
        metadata: Metadata | None = None,
        spec: ManifestSpec | None = None,
        status: ManifestStatus | None = None
    ):
        self.metadata = metadata
        self.spec = spec
        self.status = status

    def to_input(self):  # pragma: no cover
        _rval = {}
        _rval[Y_SCHEMA_KEY] = MANIFEST_SCHEMA
        if self.metadata is not None:
            _rval[Y_NAME] = self.metadata.name
        if self.spec is not None:
            _rval[Y_SPEC] = self.spec.to_input()
        if self.status is not None:
            _rval[Y_STATUS] = self.status.to_input()
        return _rval

    @staticmethod
    def from_input(obj) -> 'Manifest | None':
        if obj:
            _metadata = (
                Metadata.from_input(obj.get(Y_METADATA))
                if obj.get(Y_METADATA, None)
                else Metadata.from_name(obj.get(Y_NAME))
            )
            _spec = ManifestSpec.from_input(obj.get(Y_SPEC, None))
            _status = ManifestStatus.from_input(obj.get(Y_STATUS))
            return Manifest(
                metadata=_metadata,
                spec=_spec,
                status=_status,
            )
        return None  # pragma: no cover


class ManifestList:
    def __init__(
        self,
        items: list[Manifest],
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
    def from_input(obj) -> 'ManifestList | None':
        if obj:
            _items = obj.get(Y_ITEMS, [])
            _listMeta = obj.get(Y_METADATA, None)
            return ManifestList(
                items=_items,
                listMeta=_listMeta,
            )
        return None  # pragma: no cover
