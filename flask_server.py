from flask import Flask, request, redirect
from werkzeug.utils import secure_filename
import os
import json
from face_util import compare_faces, face_count,face_count_check
import re


app = Flask(__name__)

UPLOAD_FOLDER = 'received_files'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def print_request(request):
    # Print request url
    print(request.url)
    # print relative headers
    print('content-type: "%s"' % request.headers.get('content-type'))
    print('content-length: %s' % request.headers.get('content-length'))
    # print body content
    if request.is_json:
        json_data = request.get_json(cache=True)
        # replace image_data with '<image base64 data>'
        if json_data.get('image_data', None) is not None:
            json_data['image_data'] = '<image base64 data>'
        else: 
            print('request image_data is None.')
        print(json.dumps(json_data,indent=4))
    else: # form data
        body_data=request.get_data()
        # replace image raw data with string '<image raw data>'
        body_sub_image_data=re.sub(b'(\r\n\r\n)(.*?)(\r\n--)',br'\1<image raw data>\3', body_data,flags=re.DOTALL)
        print(body_sub_image_data.decode('utf-8'))
    # print(body_data[0:500] + b'...' + body_data[-500:]) # raw binary



@app.route('/face_match', methods=['POST', 'GET'])
def face_match():
    if request.method == 'POST':
        # check if the post request has the file part
        if ('file1' not in request.files) or ('file2' not in request.files):
            print('No file part')
            return redirect(request.url)

        file1 = request.files.get('file1')
        file2 = request.files.get('file2')
        # if user does not select file, browser also submit an empty part without filename
        if file1.filename == '' or file2.filename == '':
            print('No selected file')
            return redirect(request.url)

        if allowed_file(file1.filename) and allowed_file(file2.filename):
            #file1.save( os.path.join(UPLOAD_FOLDER, secure_filename(file1.filename)) )
            #file2.save( os.path.join(UPLOAD_FOLDER, secure_filename(file2.filename)) )
            ret = compare_faces(file1, file2)
            ret2=face_count(file1)+face_count(file2)
            resp_data = {"FaceMatched": bool(ret),"Count":int(ret2)} # convert ret (numpy._bool) to bool for json.dumps
            return json.dumps(resp_data)

    # Return a demo page for GET request
    return '''
    <!doctype html>
    <title>Face Match</title>
    <h1>Upload two images</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file1>
      <input type=file name=file2>
      <input type=submit value=Upload>
    </form>
    '''
@app.route('/face_count', methods=['POST', 'GET'])
def face_total():
    if request.method == 'POST':
        # check if the post request has the file part
        if ('file1' not in request.files):
            print('No file part')
            return redirect(request.url)

        file1 = request.files.get('file1')
        # if user does not select file, browser also submit an empty part without filename
        if file1.filename == '':
            print('No selected file')
            return redirect(request.url)

        if allowed_file(file1.filename):
            #file1.save( os.path.join(UPLOAD_FOLDER, secure_filename(file1.filename)) )
            #file2.save( os.path.join(UPLOAD_FOLDER, secure_filename(file2.filename)) )
            ret =face_count_check(file1)
            ret2=face_count(file1)            
            resp_data = {"Faces":(ret),"Count":(ret2)} # convert ret (numpy._bool) to bool for json.dumps
            #resp_data2={"face":(ret2)}
            return json.dumps(resp_data)
             

    # Return a demo page for GET request
    return '''
    <!doctype html>
    <title>Face count</title>
    <h1>Upload one images</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file1>
      <input type=submit value=Upload>
    </form>
    '''   



@app.route('/')
def hello_world():
    return 'Hello, World!'

# Run in HTTP
# When debug = True, code is reloaded on the fly while saved
app.run(host='0.0.0.0', port='5001', debug=True)
