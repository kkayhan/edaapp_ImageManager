/*
Copyright 2026.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package v1alpha1

// ImageManagerConfigSpec defines the desired state of ImageManagerConfig.
// A single cluster-scoped instance named "default" is auto-created by the
// controller on first boot and holds operator-tunable defaults for the
// upload UI and the Artifact CRs it creates.
type ImageManagerConfigSpec struct {
	// DefaultArtifactNamespace is the namespace where new Artifact CRs are
	// created when the upload form does not specify one. The built-in EDA
	// artifact server (eda-asvr) re-hosts the file under this namespace.
	// +kubebuilder:default="eda"
	// +eda:ui:title="Default artifact namespace"
	// +eda:ui:orderpriority=100
	DefaultArtifactNamespace string `json:"defaultArtifactNamespace,omitempty"`

	// DefaultRepo is the artifact repo name pre-filled in the upload UI.
	// The repo field on an Artifact is IMMUTABLE once created; multiple
	// artifacts may share a repo.
	// +kubebuilder:default="images"
	// +eda:ui:title="Default repo"
	// +eda:ui:orderpriority=200
	DefaultRepo string `json:"defaultRepo,omitempty"`

	// MaxUploadMiB rejects direct uploads larger than this many MiB, in both
	// the browser and the server. Guards the PVC and surfaces any HTTP-proxy
	// body-size limit early.
	// +kubebuilder:default=4096
	// +kubebuilder:validation:Minimum=1
	// +kubebuilder:validation:Maximum=65536
	// +eda:ui:title="Max upload size (MiB)"
	// +eda:ui:orderpriority=300
	MaxUploadMiB int `json:"maxUploadMiB,omitempty"`

	// FilePullBaseUrl is the in-cluster HTTPS base URL that eda-asvr uses to
	// pull uploaded files from this app. Leave empty to auto-derive
	// https://eda-imagemanager.<pod-namespace>.svc:8443/ . Override only for
	// non-standard service names or ports.
	// +kubebuilder:validation:Pattern=`^(https?://.*)?$`
	// +eda:ui:title="File-pull base URL (advanced)"
	// +eda:ui:orderpriority=400
	FilePullBaseUrl string `json:"filePullBaseUrl,omitempty"`
}

// ImageManagerConfigStatus defines the observed state of ImageManagerConfig.
// The controller is the sole writer of this status.
type ImageManagerConfigStatus struct {
	// Health is the overall health: ok, degraded, or error.
	Health string `json:"health,omitempty"`

	// Message is a human-readable explanation of the current health state.
	Message string `json:"message,omitempty"`

	// LastReconcileTime is the timestamp of the last completed reconcile cycle.
	LastReconcileTime string `json:"lastReconcileTime,omitempty"`

	// UploadsStored is the number of upload files currently on the PVC.
	UploadsStored int `json:"uploadsStored,omitempty"`

	// BytesStored is the total bytes of upload files on the PVC.
	BytesStored int64 `json:"bytesStored,omitempty"`

	// Artifacts is a denormalized view of the Artifact CRs this app created,
	// with each Artifact's live download status mirrored for the UI.
	Artifacts []TrackedArtifact `json:"artifacts,omitempty"`

	// Version is the controller version string.
	Version string `json:"version,omitempty"`
}

// TrackedArtifact is a denormalized record of one Artifact CR created by this
// app, including the live download status mirrored from the Artifact.
type TrackedArtifact struct {
	// Name is the Artifact CR name (equals the upload id).
	Name string `json:"name"`

	// Namespace is the Artifact CR namespace.
	Namespace string `json:"namespace"`

	// Repo is the artifact repo.
	Repo string `json:"repo"`

	// FilePath is the destination path/filename in the artifact server.
	FilePath string `json:"filePath"`

	// DownloadStatus mirrors Artifact.status.downloadStatus
	// (InProgress, Available, Error, or Failed).
	DownloadStatus string `json:"downloadStatus,omitempty"`

	// StatusReason mirrors Artifact.status.statusReason on Error/Failed.
	StatusReason string `json:"statusReason,omitempty"`

	// ExternalUrl mirrors Artifact.status.externalUrl once Available.
	ExternalUrl string `json:"externalUrl,omitempty"`
}
