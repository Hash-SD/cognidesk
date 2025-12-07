# Requirements Document

## Introduction

Sistem aplikasi Streamlit untuk klasifikasi gambar Alat Tulis Kantor (ATK) dengan fitur MLOps sederhana. Aplikasi menggunakan Custom CNN untuk klasifikasi 8 jenis ATK dengan interface yang clean dan mudah digunakan. Gambar diproses langsung tanpa penyimpanan permanen.

## Glossary

- **ATK (Alat Tulis Kantor)**: Kategori produk yang diklasifikasi (Spidol, Pensil, Pulpen, Penggaris, Penghapus, Correction Tape, Pensil Mekanik, Tipe X)
- **CNN (Convolutional Neural Network)**: Arsitektur deep learning untuk klasifikasi gambar
- **MLOps**: Praktik Machine Learning Operations untuk mengelola model ML
- **Confidence Score**: Nilai probabilitas prediksi model (0-1)
- **Preprocessing**: Proses transformasi gambar sebelum inferensi

## Requirements

### Requirement 1

**User Story:** As a user, I want to upload or capture images of office stationery, so that I can get instant classification.

#### Acceptance Criteria

1. WHEN a user uploads an image THEN the System SHALL accept .jpg, .jpeg, .png, or .bmp files up to 5MB
2. WHEN a user captures from camera THEN the System SHALL process the image immediately without storage
3. WHEN a valid image is provided THEN the System SHALL display a preview with basic info (dimensions, format)


### Requirement 2

**User Story:** As a user, I want to see classification results with confidence scores, so that I can understand the prediction quality.

#### Acceptance Criteria

1. WHEN prediction completes THEN the System SHALL display the predicted class name and confidence percentage
2. WHEN showing results THEN the System SHALL display top-3 predictions with confidence scores
3. WHEN confidence is below 50% THEN the System SHALL display a low-confidence warning

### Requirement 3

**User Story:** As a developer, I want consistent image preprocessing, so that the model receives standardized input.

#### Acceptance Criteria

1. WHEN preprocessing an image THEN the System SHALL resize to 224x224 pixels
2. WHEN preprocessing an image THEN the System SHALL normalize pixel values to [0, 1] range
3. WHEN preprocessing an image THEN the System SHALL convert to RGB format

### Requirement 4

**User Story:** As a data scientist, I want to view model metrics on a dashboard, so that I can monitor model performance.

#### Acceptance Criteria

1. WHEN viewing dashboard THEN the System SHALL display model accuracy and loss metrics
2. WHEN viewing dashboard THEN the System SHALL show class distribution chart
3. WHEN viewing dashboard THEN the System SHALL display model version information

### Requirement 5

**User Story:** As a ML engineer, I want to manage model versions, so that I can track different model iterations.

#### Acceptance Criteria

1. WHEN viewing model management THEN the System SHALL display available model versions with metrics
2. WHEN comparing models THEN the System SHALL show side-by-side performance comparison
3. WHEN a model is selected THEN the System SHALL allow switching active model version

### Requirement 6

**User Story:** As a user, I want a clean multi-page interface, so that I can navigate easily between features.

#### Acceptance Criteria

1. WHEN the app loads THEN the System SHALL display a sidebar with navigation menu
2. WHEN navigating THEN the System SHALL provide Home, Predict, Dashboard, and Model Management pages
3. WHEN on any page THEN the System SHALL maintain consistent styling and layout

### Requirement 7

**User Story:** As a developer, I want Streamlit-native implementation, so that the app works on Streamlit Cloud.

#### Acceptance Criteria

1. WHEN caching models THEN the System SHALL use st.cache_resource decorator
2. WHEN managing state THEN the System SHALL use st.session_state
3. WHEN configuring theme THEN the System SHALL use .streamlit/config.toml

### Requirement 8

**User Story:** As a developer, I want GitHub-ready structure, so that the project can be easily deployed.

#### Acceptance Criteria

1. WHEN cloning the repo THEN the System SHALL include README.md with setup instructions
2. WHEN setting up THEN the System SHALL provide requirements.txt with dependencies
3. WHEN deploying THEN the System SHALL work with Streamlit Cloud standard process

### Requirement 9

**User Story:** As a user, I want demo mode when no model exists, so that I can explore the interface.

#### Acceptance Criteria

1. WHEN no model file exists THEN the System SHALL run in demo mode with simulated predictions
2. WHEN in demo mode THEN the System SHALL clearly indicate predictions are simulated
3. WHEN model is available THEN the System SHALL automatically use real predictions
