import face_recognition as fr
from PIL import Image

def compare_faces(file1, file2):
    """
    Compare two images and return True / False for matching.
    """
    # Load the jpg files into numpy arrays
    image1 = fr.load_image_file(file1)
    image2 = fr.load_image_file(file2)
    
    # Get the face encodings for each face in each image file
    # Assume there is only 1 face in each image, so get 1st face of an image.
    image1_encoding = fr.face_encodings(image1)[0]
    image2_encoding = fr.face_encodings(image2)[0]
    
    # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
    results = fr.compare_faces([image1_encoding], image2_encoding)    
    return results[0]


def face_count_check(file1):
    #load a image
    image1=fr.load_image_file(file1)
    face_locations = fr.face_locations(image1)
    if face_locations==[]:
        face=False
    else:
        face=True
    #face_locations = fr.face_locations(image1)
    return face

def face_count(file1):
    image1=fr.load_image_file(file1)
    face_locations = fr.face_locations(image1, number_of_times_to_upsample=0, model="cnn")
    return len(face_locations)

            
    


