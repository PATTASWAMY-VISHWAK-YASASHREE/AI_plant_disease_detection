<template>
    <div class="app-container">
      <!-- Navbar -->
      <nav class="navbar">
        <div class="navbar-content">
          <h1 class="title">Plant Disease Detection</h1>
          <ul class="nav-links">
            <li><a href="#upload">Upload</a></li>
            <li><a href="#description">About</a></li>
            <li><a href="#how-to-use">How to Use</a></li>
          </ul>
        </div>
      </nav>
  
      <!-- Description Section -->
      <section id="description" class="section">
        <div class="section-content">
          <h2 class="section-title">About Our Project</h2>
          <p class="section-text">
            Our Plant Disease Detection system leverages cutting-edge AI...
          </p>
        </div>
      </section>
  
      <!-- Development Section -->
      <section id="development" class="section">
        <div class="section-content">
          <h2 class="section-title">How We Developed the Solution</h2>
          <ul class="feature-list">
            <li><strong>Cutting-Edge Machine Learning Approach:</strong> Leveraged the power of <span class="highlight">Convolutional Neural Networks (CNN)</span> ...</li>
            <li><strong>Robust Dataset Preparation:</strong> Curated a comprehensive dataset ...</li>
            <li><strong>Rigorous Model Training:</strong> Achieved optimal accuracy ...</li>
            <li><strong>Integration of AI and User Interface:</strong> Built an intuitive web interface using <span class="highlight">Flask</span> ...</li>
            <li><strong>Focus on Real-World Impact:</strong> Designed the solution to be scalable...</li>
          </ul>
        </div>
      </section>
  
      <!-- Upload Section -->
      <section id="upload" class="upload-section">
        <div class="upload-box section_1" @dragover.prevent @drop.prevent="handleDrop">
          <h2 class="upload-title">Upload Your Crop Image</h2>
          <form @submit.prevent="onSubmit">
            <div class="upload-area" @dragover.prevent @drop.prevent="handleDrop">
              <p class="upload-instructions">Drag and drop your image here</p>
              <input ref="imageInput" type="file" class="hidden-input" accept="image/*" @change="handleFileSelect" />
              <label class="upload-button" @click="browseFile">Browse File</label>
            </div>
            <div id="preview" class="preview-area">
              <img v-if="previewUrl" :src="previewUrl" alt="Uploaded Image" class="preview-image" />
            </div>
            <button type="submit" class="predict-button">Predict</button>
          </form>
          <div v-if="isLoading" class="loading-text">Loading...</div>
          <div id="result" class="result-text">{{ resultMessage }}</div>
        </div>
      </section>
  
      <!-- How to Use Section -->
      <section id="how-to-use" class="section">
        <div class="section-content">
          <h2 class="section-title">How to Use</h2>
          <div class="how-to-grid">
            <div class="how-to-card">
              <h3>Step 1</h3>
              <p>Drag and drop or upload your plant image using the upload box.</p>
            </div>
            <div class="how-to-card">
              <h3>Step 2</h3>
              <p>Click the "Predict" button to analyze the image.</p>
            </div>
            <div class="how-to-card">
              <h3>Step 3</h3>
              <p>View the results and take necessary action based on the prediction.</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  </template>
  
  <script>
  export default {
    name: "PlantDiseaseDetection",
    data() {
      return {
        previewUrl: null,
        selectedFile: null,
        isLoading: false,
        resultMessage: ""
      };
    },
    methods: {
      browseFile() {
        this.$refs.imageInput.click();
      },
      handleFileSelect(event) {
        const file = event.target.files[0];
        this.loadPreview(file);
      },
      handleDrop(event) {
        const file = event.dataTransfer.files[0];
        if (file) {
          this.$refs.imageInput.files = event.dataTransfer.files;
          this.loadPreview(file);
        }
      },
      loadPreview(file) {
        if (!file) return;
        this.selectedFile = file;
        this.resultMessage = "";
        const reader = new FileReader();
        reader.onload = (e) => {
          this.previewUrl = e.target.result;
        };
        reader.readAsDataURL(file);
      },
      async onSubmit() {
        if (!this.selectedFile) {
          this.resultMessage = "Please upload an image file.";
          return;
        }
  
        this.isLoading = true;
        this.resultMessage = "";
  
        try {
          const formData = new FormData();
          formData.append("file", this.selectedFile);
  
          const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            body: formData
          });
  
          if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
  
          const data = await response.json();
          const labels = { 0: "Healthy", 1: "Powdery", 2: "Rust" };
          this.resultMessage = data.error
            ? `Error: ${data.error}`
            : `Prediction: ${labels[data.predicted_class] || "Unknown"}`;
        } catch (error) {
          this.resultMessage = error.message;
        } finally {
          this.isLoading = false;
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .app-container {
    background-color: #f3f4f6;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }
  
  .navbar {
    background-color: #16a34a;
    padding: 1rem;
    color: white;
  }
  
  .navbar-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1100px;
    margin: 0 auto;
  }
  
  .title {
    font-size: 1.75rem;
    font-weight: bold;
  }
  
  .nav-links {
    display: flex;
    gap: 1.5rem;
    list-style: none;
  }
  
  .nav-links a {
    color: white;
    text-decoration: none;
  }
  
  .nav-links a:hover {
    text-decoration: underline;
  }
  
  .section {
    padding: 4rem 1rem;
    background-color: #fafafa;
  }
  
  .section-content {
    max-width: 1000px;
    margin: 0 auto;
  }
  
  .section-title {
    text-align: center;
    font-size: 2rem;
    margin-bottom: 1.5rem;
  }
  
  .section-text {
    text-align: center;
    font-size: 1.125rem;
    color: #4b5563;
  }
  
  .feature-list {
    list-style-type: disc;
    padding-left: 1.5rem;
    font-size: 1.125rem;
    color: #4b5563;
  }
  
  .highlight {
    color: #16a34a;
  }
  
  .upload-section {
    flex-grow: 1;
    background-color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 4rem 1rem;
  }
  
  .upload-box {
    background-color: #e5e7eb;
    padding: 2rem;
    border-radius: 0.75rem;
    width: 50%;
    text-align: center;
  }
  
  .upload-title {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    font-weight: 600;
  }
  
  .upload-area {
    border: 4px dashed #d1d5db;
    background-color: #f3f4f6;
    padding: 1.5rem;
    border-radius: 0.75rem;
  }
  
  .upload-instructions {
    color: #6b7280;
    margin-bottom: 1rem;
  }
  
  .hidden-input {
    display: none;
  }
  
  .upload-button {
    display: inline-block;
    padding: 0.5rem 1rem;
    background-color: #16a34a;
    color: white;
    border-radius: 0.5rem;
    cursor: pointer;
  }
  
  .upload-button:hover {
    background-color: #15803d;
  }
  
  .preview-area {
    margin-top: 1rem;
  }
  
  .preview-image {
    max-width: 100%;
    height: auto;
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .predict-button {
    margin-top: 1rem;
    padding: 0.5rem 1rem;
    background-color: #16a34a;
    color: white;
    border: none;
    border-radius: 0.5rem;
    cursor: pointer;
  }
  
  .predict-button:hover {
    background-color: #15803d;
  }
  
  .loading-text {
    margin-top: 1rem;
    font-weight: 600;
    color: #374151;
  }
  
  .result-text {
    margin-top: 1rem;
    font-weight: 600;
    color: #374151;
  }
  
  .section_1:hover {
    box-shadow: 0px 25px 60px 40px rgba(0, 0, 0, 0.2);
  }
  
  .how-to-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  @media (min-width: 768px) {
    .how-to-grid {
      grid-template-columns: repeat(3, 1fr);
    }
  }
  
  .how-to-card {
    background-color: #f3f4f6;
    padding: 1.5rem;
    border-radius: 0.75rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    text-align: center;
  }
  
  .how-to-card h3 {
    font-size: 1.25rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
  }
  
  .how-to-card p {
    color: #4b5563;
  }
  </style>
  