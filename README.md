# PPE Detection System using YOLOv5, Flask, and SQLite

## Overview

The **PPE (Personal Protective Equipment) Detection System** is an AI-powered computer vision application designed to monitor workplace safety compliance in real time. The system automatically detects and classifies PPE items such as **Hard Hats, Safety Vests, Face Masks, and Persons** using a custom-trained **YOLOv5** object detection model.

This solution helps industries improve safety compliance, reduce manual monitoring efforts, and generate automated alerts when workers are not wearing the required protective equipment.

---

## Key Features

* Real-time PPE detection using YOLOv5
* Detection and classification of:

  * Person
  * Hard Hat
  * Safety Vest
  * Face Mask
* Custom dataset training using images collected from Kaggle
* Video and image-based inference
* Object tracking with unique IDs using SORT algorithm
* Web-based user interface built with Flask
* User authentication (Login/Register)
* SQLite database integration for user management
* Safety compliance monitoring and alert generation
* NVIDIA API integration for enhanced inference capabilities

---

## Project Architecture

The project consists of three major components:

### 1. AI Model Training

* Custom PPE dataset preparation
* YOLOv5 model training on Google Colab
* Model evaluation and optimization
* Multiple training experiments and hyperparameter tuning

### 2. Inference Engine

* Real-time image and video processing
* PPE detection and classification
* Object tracking using SORT
* Alert generation for PPE violations

### 3. Web Application

* Flask-based frontend
* User authentication system
* Video upload and monitoring interface
* Model selection and inference execution
* Result visualization through web browser

---

## PPE Categories

The model is trained to detect the following classes:

| Class ID | Category    |
| -------- | ----------- |
| 0        | Person      |
| 1        | Hard Hat    |
| 2        | Safety Vest |
| 3        | Face Mask   |

---

## Industrial Applications

This system can be deployed in:

* Construction Sites
* Manufacturing Plants
* Chemical Industries
* Food Processing Industries
* Warehouses
* Mining Operations
* Industrial Facilities
* Safety Compliance Monitoring Systems

---

## Project Structure

```text
PPE-Detection/
│
├── PPE_Image/
│   ├── P1.jpg
│   ├── P2.jpg
│   ├── P3.jpg
│   └── ...
│
├── PPE_Video/
│   ├── PPE_Input.mp4
│   ├── Video1.mp4
│   ├── Video2.mp4
│   └── Video3.mp4
│
├── static/
│   └── images/
│       └── login_background.jpg
│
├── templates/
│   ├── about.html
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── model.html
│   ├── inference.html
│   └── register.html
│
├── PPE.ipynb
├── Final_Inference.py
├── sort.py
├── database.db
├── requirements.txt
└── README.md
```

---

## File Descriptions

### PPE.ipynb

Jupyter Notebook used for:

* Dataset preparation
* Model training
* Performance evaluation
* Exporting trained YOLOv5 weights

### Final_Inference.py

Main inference script responsible for:

* Loading trained models
* Processing images and videos
* Running PPE detection
* Displaying detection results

### sort.py

Implements the **SORT (Simple Online and Realtime Tracking)** algorithm:

* Calculates Intersection over Union (IoU)
* Assigns unique IDs to detected objects
* Tracks workers across video frames

### database.db

SQLite database used for:

* User registration
* Login authentication
* Storing user information

### requirements.txt

Contains all required Python libraries and dependencies.

---

## Technologies Used

### Artificial Intelligence & Computer Vision

* Python
* YOLOv5
* OpenCV
* NumPy
* Pandas

### Deep Learning

* PyTorch
* Torchvision

### Web Development

* Flask
* HTML5
* CSS3
* JavaScript

### Database

* SQLite

### Object Tracking

* SORT Algorithm
* IoU (Intersection over Union)

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/PPE-Detection.git

cd PPE-Detection
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Model Training

Open the notebook:

```bash
PPE.ipynb
```

Train the YOLOv5 model using the custom PPE dataset and export the trained weights.

---

## Running Inference

```bash
python Final_Inference.py
```

The system will:

1. Load the trained YOLOv5 model
2. Process images or videos
3. Detect PPE equipment
4. Track detected individuals
5. Generate compliance results

---

## Running the Flask Application

```bash
python app.py
```

Open your browser and navigate to:

```text
http://127.0.0.1:5000
```

Features available through the web interface:

* User Login & Registration
* Model Upload
* Video Upload
* PPE Detection
* Result Visualization
* Compliance Monitoring

---

## Workflow

1. Collect PPE dataset from Kaggle.
2. Annotate and prepare training data.
3. Train custom YOLOv5 model.
4. Export trained weights.
5. Upload image/video through Flask application.
6. Run real-time inference.
7. Detect PPE violations.
8. Generate alerts and monitoring reports.

---

## Future Enhancements

* Helmet color detection
* Safety gloves detection
* Safety shoes detection
* Real-time CCTV integration
* Email/SMS alert notifications
* Cloud deployment
* Multi-camera monitoring
* Dashboard analytics
* Employee attendance integration

---

## Results

The trained YOLOv5 model successfully detects:

* Persons
* Hard Hats
* Safety Vests
* Face Masks

The system provides real-time monitoring and can assist organizations in maintaining workplace safety standards and regulatory compliance.

---

## Conclusion

The PPE Detection System demonstrates how Artificial Intelligence and Computer Vision can be utilized to automate workplace safety monitoring. By leveraging YOLOv5, SORT tracking, Flask, and SQLite, the solution provides a scalable and efficient approach to ensuring PPE compliance across various industrial environments.

---

## Author

Developed as part of a Computer Vision and Deep Learning project focusing on industrial safety compliance using AI-powered object detection and tracking technologies.
