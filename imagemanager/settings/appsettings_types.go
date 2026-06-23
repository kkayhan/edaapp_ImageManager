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

	// Memory limit for the Image Manager controller pod (Kubernetes quantity, e.g. "256Mi").
	// +kubebuilder:default="256Mi"
	// +eda:ui:title="Controller memory limit"
	ControllerMemoryLimit string `json:"controllerMemoryLimit,omitempty"`

	// Size of the persistent volume that stores uploaded images before eda-asvr
	// re-hosts them (Kubernetes quantity, e.g. "20Gi"). Set this large enough to
	// hold the images you intend to upload concurrently.
	// +kubebuilder:default="20Gi"
	// +eda:ui:title="Upload storage size"
	UploadStorageSize string `json:"uploadStorageSize,omitempty"`
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
