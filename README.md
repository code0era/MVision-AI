

# Indian Army AI Object Detection System

[![YOLOv8](https://img.shields.io/badge/Model-YOLOv8-FF6600.svg)](https://ultralytics.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An advanced, AI-powered computer vision application designed for the **Indian Armed Forces** to detect military vehicles, aircraft, and equipment in real-time. Built with **Streamlit** and **YOLOv8**.

---
# Screenshots:

<img width="1920" height="1020" alt="Screenshot 2026-01-09 033512" src="https://github.com/user-attachments/assets/58306732-06c4-4c9b-9344-e82f53210e60" />


<img width="1920" height="1020" alt="Screenshot 2026-01-09 033521" src="https://github.com/user-attachments/assets/ec5789b8-d0fc-4623-9510-b1aff9a8574e" />
<img width="1920" height="1020" alt="Screenshot 2026-01-09 033528" src="https://github.com/user-attachments/assets/65b7149e-8f67-46a3-9762-d8bd4334b26d" />

<img width="1920" height="1020" alt="Screenshot 2026-01-09 033538" src="https://github.com/user-attachments/assets/da2ce589-9f66-470b-835d-ae11b11dbb66" />

<img width="1920" height="1020" alt="Screenshot 2026-01-09 033549" src="https://github.com/user-attachments/assets/231ce7a9-8213-4695-a0df-973618306558" />

<img width="1920" height="1020" alt="Screenshot 2026-01-09 033559" src="https://github.com/user-attachments/assets/c3eedab6-20f9-45c7-a929-cb664eada3e3" />

# FINAL REPORT

<img width="619" height="798" alt="image" src="https://github.com/user-attachments/assets/10503308-fee7-4843-97bb-7282219ff981" />


## 🎖️ Key Features

- **🎯 Precision Detection**: Optimized for military-specific objects using YOLOv8 architectures.
- **🌗 Dual-Theme Interface**: Military-themed UI with Dark and Light mode toggles.
- **📄 Professional Reporting**: Automatically generates downloadable PDF reports with detection statistics and visualizations.
- **📥 Multiple Export Options**: Download annotated images (PNG) and structured surveillance reports (PDF).
- **📊 Real-time Metrics**: Track object counts, model confidence, and IOU thresholds on the fly.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 to 3.11 (Recommended)
- [Git](https://git-scm.com/)

### Local Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/military-object-detection.git
   cd military-object-detection
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Mac/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add Your Model**
   Place your trained `best.pt` file in the root directory.

5. **Run the Application**
   ```bash
   streamlit run app.py
   ```

---

## 📦 Project Structure

```text
├── app.py              # Main Streamlit application
├── best.pt             # Trained YOLOv8 model weights
├── requirements.txt    # Python dependencies
├── .gitignore          # Files to exclude from Git
└── README.md           # Project documentation
```

---

## 🛠️ Technology Stack

- **Computer Vision**: [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- **Web Framework**: [Streamlit](https://streamlit.io/)
- **Image Processing**: OpenCV & PIL
- **Report Generation**: ReportLab
- **Deep Learning**: PyTorch

---

## ☁️ Deployment

This app is designed to be deployed on **Streamlit Community Cloud**:

1. Push your code to a GitHub repository.
2. Connect your GitHub account to [Streamlit Cloud](https://share.streamlit.io/).
3. Select your repository and the `app.py` file to deploy.

---

## 🎖️ Honor & Valor
> *"The safety, honour and welfare of your country come first, always and every time."*
> — **Field Marshal Philip Chetwode**

### Jai Hind! 🇮🇳

---
**Disclaimer**: This is a proof-of-concept application for educational and research purposes.
```

### Tips for your README:
*   **Screenshot**: After you deploy, take a screenshot of your app and add it to the top of the README using `![App Screenshot](screenshot.png)`.
*   **Customization**: Change `your-username` and `military-object-detection` in the URLs to match your actual GitHub details.
