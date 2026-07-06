package settings

import (
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// AppSettingsSpec defines the desired state of AppSettings.
type AppSettingsSpec struct {
	// CPU limit for the Image Manager controller pod (Kubernetes quantity, e.g. "500m").
	// +kubebuilder:default="500m"
	// +eda:ui:title="Controller CPU limit"
	ControllerCpuLimit string `json:"controllerCpuLimit,omitempty"`

	// Memory limit for the Image Manager controller pod (Kubernetes quantity, e.g. "512Mi").
	// Default 512Mi: uploads stream to disk, but a fast push to CephFS can hold up to
	// ~32Mi of not-yet-flushed page cache per concurrent upload (cgroup-charged).
	// +kubebuilder:default="512Mi"
	// +eda:ui:title="Controller memory limit"
	ControllerMemoryLimit string `json:"controllerMemoryLimit,omitempty"`

	// Size of the persistent volume that stores uploaded images before eda-asvr
	// re-hosts them (Kubernetes quantity, e.g. "20Gi"). Set this large enough to
	// hold the images you intend to upload concurrently.
	// +kubebuilder:default="20Gi"
	// +eda:ui:title="Upload storage size"
	UploadStorageSize string `json:"uploadStorageSize,omitempty"`

	// EDA role(s) allowed to use Image Manager, comma-separated (a user is allowed
	// if they hold ANY listed role). Names match EDA's Roles screen; the internal
	// "edarole_" prefix is handled automatically. Defaults to the system
	// administrator role. The whole UI (view, upload, delete) requires one of these.
	// +kubebuilder:default="system-administrator"
	// +eda:ui:title="Allowed EDA role(s)"
	AllowedRoles string `json:"allowedRoles,omitempty"`

	// NodeAgentEnabled deploys the per-node DaemonSet that writes containerd
	// registry-hosts redirects for SR-SIM image pulls. Set false for labs that
	// only upload SR Linux / SR OS hardware images (DaemonSet stays running but
	// skips hosts.toml writes; scale to 0 for zero node pods). On Talos the agent
	// cannot write the immutable containerd config anyway, so false is sensible there.
	// +kubebuilder:default="true"
	// +eda:ui:title="Enable SR-SIM node agent"
	NodeAgentEnabled string `json:"nodeAgentEnabled,omitempty"`
}

// +kubebuilder:object:root=true
// +kubebuilder:subresource:status

// AppSettings is the Schema for the appsettings API.
type AppSettings struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec AppSettingsSpec `json:"spec,omitempty"`
}

// +kubebuilder:object:root=true

// AppSettingsList contains a list of AppSettings.
type AppSettingsList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []AppSettings `json:"items"`
}
