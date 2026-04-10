import re
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for,session,Response,Request
from flask_cors import CORS
import cv2
from flask_wtf.csrf import CSRFProtect
import numpy as np
from ultralytics import YOLO
import cvzone
import sqlite3
from sort import *
import ast
import requests, base64
import threading

app = Flask(__name__)
CORS(app)

 # Set a secret key for sessions
app.config['SECRET_KEY'] = 'a' 

# Path to store the JSON file
JSON_FILE = "contact_data.json"

invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"

stream = False

@app.route("/", methods=["GET", "POST"])
def project():
    return render_template("index.html")

@app.route("/hero")
def home():
    return render_template("index.html")

@app.route("/model")
def model():
    return render_template("model.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Connect to the SQLite database
        conn = sqlite3.connect('projectDatabase.db')
        c = conn.cursor()

        # Drop the existing table if it exists
        c.execute("DROP TABLE IF EXISTS userDetails")

        # Create the table with the 'email' column
        c.execute('''CREATE TABLE IF NOT EXISTS userDetails(
                    firstName TEXT,
                    lastName TEXT,
                    email TEXT UNIQUE,
                    password TEXT)''')

        # Get form data
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")

        # Insert data into the database
        try:
            c.execute("INSERT INTO userDetails (firstName, lastName, email, password) VALUES (?, ?, ?, ?)",
                      (firstname, lastname, email, password))
            # Commit changes and close the connection
            conn.commit()
            message = "Registration successful!"
            status = "success"
        except sqlite3.IntegrityError:
            # If the email already exists, handle the error
            message = "Email already exists!"
            status = "error"
        
        conn.close()

        # Render the registration page and pass the status and message to be shown in the popup
        return render_template("login.html", message=message, status=status)
    else:
        # Render the registration page for GET requests
        return render_template("register.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/submit_contact", methods=["POST"])
def submit_contact():
    # Get form data
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    # Create a new entry
    contact_entry = {"name": name, "email": email, "message": message}

    # Read existing data from JSON file
    try:
        with open(JSON_FILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    # Append new entry to the data
    data.append(contact_entry)

    # Write updated data back to JSON file
    with open(JSON_FILE, "w") as file:
        json.dump(data, file, indent=4)

    return jsonify({"status": "success", "message": "Contact details saved!"}), 200

@app.route("/login", methods=["POST"])
def log_in():
    # Connect to the SQLite database
    conn = sqlite3.connect('projectDatabase.db')
    c = conn.cursor()

    # Get the values from the form
    firstname = request.form.get('firstname')  
    password = request.form.get('password')

    # Use parameterized queries to prevent SQL injection
    c.execute("SELECT EXISTS(SELECT 1 FROM userDetails WHERE firstname=? AND password=?)", (firstname, password))
    flag = c.fetchone()[0]

    conn.commit()
    conn.close()

    if flag == 1:
        session['user'] = firstname  # Store user's first name in session
        return render_template("model.html")
    else:
        return render_template('login.html', error="Invalid credentials, please try again.")
    
# Allowed extensions
IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "bmp"}
VIDEO_EXTENSIONS = {"mp4", "avi", "mov", "mkv"}

def allowed_file(filename, allowed_extensions):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


outputFrame = None
lock = threading.Lock()

@app.route("/")
def video_feed_template():
    # return the rendered template
    return render_template("video_feed.html")

@app.route("/predict", methods=["POST","GET"])
def predict():
    global outputFrame

    if "file" not in request.files:
        return jsonify({"error": "File is required"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = file.filename.lower()
    print(filename)

    # Check if it's an image
    if file and allowed_file(filename, IMAGE_EXTENSIONS):
        image_path = os.path.join("ppe_image", filename)
        file.save(image_path)
        # print("Saved Image:", image_path)
        print(image_path)

        with open(f"{image_path}", "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode()
            
            headers = {
            "Authorization": "Bearer REMOVED_API_KEYq63EvXdo8o5eagg9rRRj3EI0iX7U7Sn3a6TR2It0HEw7cJLUiCzE9PsAyFFx-EAI",
            "Accept": "text/event-stream" if stream else "application/json"
            }

            prompt = "Analyse the image and fill up the json format. Json format.Strongly check If anything is not visible It should return that part is not visible like if foot is visible in the image it should return yes in wearing shoes or no else wearing shoes should return Legs_Not_visible  .json format: {'Wearing_Helmet': 'Yes/No/Head_Not_Visible', 'Wearing_Goggles': 'Yes/No/Face_Not_Visible', 'Wearing_Mask': 'Yes/No/Face_Not_Visible','Wearing_Vest': 'Yes/No/Body_Not_Visible', 'Wearing_Gloves': 'Yes/No/Hands_Not_Visible', 'Wearing_Shoes': 'Yes/No/Legs_Not_Visible',            }   "

            payload = {
            "model": 'microsoft/phi-3.5-vision-instruct',
            "messages": [
                {
                "role": "user",
                "content": f' {prompt}  <img src="data:image/jpeg;base64,{image_b64}" />'
                }
            ],
            "max_tokens": 512,
            "temperature": 0.20,
            "top_p": 0.70,
            "stream": stream
            }

            response = requests.post(invoke_url, headers=headers, json=payload)

            if stream:
                for line in response.iter_lines():
                    if line:
                        print(line.decode("utf-8"))
            else:
                # print(response.json()['choices'][0]['message'][ 'content'])
                data = response.json()

                # print("Full API Response:", data)  # Debugging

                if "choices" in data and len(data["choices"]) > 0:
                    message = data["choices"][0].get("message", {})
                    content = message.get("content", "").strip()
                    
                    # print("Raw Content:", repr(content))  # Debugging

                    if content:
                        try:
                            # Remove Markdown if needed
                            if content.startswith("```json"):
                                content = content.strip("```json").strip("```")

                            ppe_data = json.loads(content)
                            print(ppe_data['Wearing_Helmet'],ppe_data['Wearing_Goggles'],ppe_data['Wearing_Mask'],ppe_data['Wearing_Vest'],ppe_data['Wearing_Shoes'])
                            print("Parsed JSON:", ppe_data)
        
                            return jsonify({'predictions': ppe_data})
                        except json.JSONDecodeError as e:
                            print("JSON Decode Error:", e)
                    else:
                        print("Error: 'content' is empty")
                else:
                    print("Error: Unexpected API response structure")


        return jsonify({"message": "Image uploaded successfully", "image_path": image_path}), 200

    elif file and allowed_file(filename, VIDEO_EXTENSIONS):
        video_path = os.path.join("ppe_video", filename)
        file.save(video_path)
        print("Saved Video:", video_path)

        # Ensure the file exists after saving
        if not os.path.exists(video_path):
            return jsonify({"error": "Video upload failed"}), 400
        
        cap = cv2.VideoCapture(r"{}".format(video_path))

        # Initialize SORT tracker
        tracker = Sort(max_age=30)

        # Load class names
        classnames = []
        with open('classes.txt', 'r') as f:
            classnames = f.read().splitlines()

        model = YOLO('best.pt')
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            detections = np.empty((0, 5))
            results = model(frame)

            for info in results:
                boxes = info.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    print(x1, y1, x2, y2)
                    conf = box.conf[0]
                    classindex = box.cls[0].item()
                    object_detected = classnames[int(classindex)]

                    # Detect with high confidence
                    if object_detected and conf > 0.1:
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        new_detections = np.array([x1, y1, x2, y2, conf])

                        # Track only persons
                        if object_detected == "Person":
                            detections = np.vstack((detections, new_detections))
                        else:
                            # Draw bounding box for non-person objects
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                            cvzone.putTextRect(frame, f'{object_detected}', [x1 + 5, y1 - 10], thickness=1, colorT=(0, 0, 0), scale=1.2)

            # Update tracker only for persons
            track_result = tracker.update(detections)

            # Draw bounding boxes only for tracked persons
            for result in track_result:
                x1, y1, x2, y2, obj_id = map(int, result)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Blue for person tracking
                cvzone.putTextRect(frame, f'Person {obj_id}', [x1 + 5, y1 - 10], thickness=1, colorT=(255, 255, 255), scale=1.2)

            # Show the frame
            # cv2.imshow('PPE Detection', cv2.resize(frame, (1020, 500)))

            with lock:
                outputFrame = frame.copy()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        return jsonify({"data":True, "video_path": video_path}), 200

    else:
        return jsonify({"error": "Invalid file type"}), 400
    
    
def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock

    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue

            # encode the frame in JPEG format
            print("outputframe",outputFrame.shape)
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')
        
@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
