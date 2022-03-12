# Face-Recognition-using-Flask-API
Build a REST API for face recognition.So you can use it to develop your own face recognition applications without the need to learn complicated machine learning. 

**API Endpoints:**
* face_match : return if two images are matched for the same person and face count
* face_count : return a face is found and the number faces found.
# Installation
Install cMake before installing [dlib](http://dlib.net/).

Then run: pip install -r requirements.txt

# How to Run

              
## Run API Server
python flask_server.py

## Run API client - Web
Simply open a web browser and enter:

http://127.0.0.1:5001/face_count

http://127.0.0.1:5001/face_match

upload image files and get results.

# Notes
Many open source face recognition projects are easy to install in or only for Linux / POSIX systems. Building a REST API for them is a much easier solution than trying to convert and deploy them for mobile devices.
