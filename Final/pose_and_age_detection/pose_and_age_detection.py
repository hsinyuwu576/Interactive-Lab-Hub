from tflite_runtime.interpreter import Interpreter
import numpy as np
import cv2
from time import time
import paho.mqtt.client as mqtt
import uuid
import subprocess

# Dictionary that maps from joint names to keypoint indices.
KEYPOINT_DICT = {
    'nose': 0,
    'left_eye': 1,
    'right_eye': 2,
    'left_ear': 3,
    'right_ear': 4,
    'left_shoulder': 5,
    'right_shoulder': 6,
    'left_elbow': 7,
    'right_elbow': 8,
    'left_wrist': 9,
    'right_wrist': 10,
    'left_hip': 11,
    'right_hip': 12,
    'left_knee': 13,
    'right_knee': 14,
    'left_ankle': 15,
    'right_ankle': 16
}

# Maps bones to a matplotlib color name.
KEYPOINT_EDGE_INDS_TO_COLOR = {
    (0, 1): 'r',
    (0, 2): 'b',
    (1, 3): 'r',
    (2, 4): 'b',
    (0, 5): 'r',
    (0, 6): 'b',
    (5, 7): 'r',
    (7, 9): 'r',
    (6, 8): 'b',
    (8, 10): 'b',
    (5, 6): 'g',
    (5, 11): 'r',
    (6, 12): 'b',
    (11, 12): 'g',
    (11, 13): 'r',
    (13, 15): 'r',
    (12, 14): 'b',
    (14, 16): 'b'
}

COLOR_DICT = {
    'r': (255, 0, 0),
    'g': (0, 255, 0),
    'b': (0, 0, 255)
}

# Load models

# Face Detection
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Age Detection
interpreter_age = Interpreter(model_path="AgeClass_best_06_02-16-02.tflite")
interpreter_age.allocate_tensors()

# Pose Detection
interpreter_pose = Interpreter("lite-model_movenet_singlepose_lightning_tflite_int8_4.tflite")
interpreter_pose.allocate_tensors()
_, input_height, input_width, _ = interpreter_pose.get_input_details()[0]['shape']


def keypoints_and_edges_for_display(keypoints_with_scores,
                                     height,
                                     width,
                                     keypoint_threshold=0.3):
  """Returns high confidence keypoints and edges for visualization.

  Args:
    keypoints_with_scores: A numpy array with shape [1, 1, 17, 3] representing
      the keypoint coordinates and scores returned from the MoveNet model.
    height: height of the image in pixels.
    width: width of the image in pixels.
    keypoint_threshold: minimum confidence score for a keypoint to be
      visualized.

  Returns:
    A (keypoints_xy, edges_xy, edge_colors) containing:
      * the coordinates of all keypoints of all detected entities;
      * the coordinates of all skeleton edges of all detected entities;
      * the colors in which the edges should be plotted.
  """
  keypoints_xy = {}
  keypoint_edges_all = []
  edge_colors = []
  num_instances, _, _, _ = keypoints_with_scores.shape
  for idx in range(num_instances):
    kpts_x = keypoints_with_scores[0, idx, :, 1]
    kpts_y = keypoints_with_scores[0, idx, :, 0]
    kpts_scores = keypoints_with_scores[0, idx, :, 2]
    kpts_absolute_xy = np.stack(
        [width * np.array(kpts_x), height * np.array(kpts_y)], axis=-1)
    kpts_above_thresh_absolute = kpts_absolute_xy[
        kpts_scores > keypoint_threshold, :]
    for point_idx in range(17):
      if kpts_scores[point_idx] > keypoint_threshold:
        keypoints_xy[point_idx] = kpts_absolute_xy[point_idx]

    for edge_pair, color in KEYPOINT_EDGE_INDS_TO_COLOR.items():
      if (kpts_scores[edge_pair[0]] > keypoint_threshold and
          kpts_scores[edge_pair[1]] > keypoint_threshold):
        x_start = kpts_absolute_xy[edge_pair[0], 0]
        y_start = kpts_absolute_xy[edge_pair[0], 1]
        x_end = kpts_absolute_xy[edge_pair[1], 0]
        y_end = kpts_absolute_xy[edge_pair[1], 1]
        line_seg = np.array([[x_start, y_start], [x_end, y_end]])
        keypoint_edges_all.append(line_seg)
        edge_colors.append(color)

  if keypoint_edges_all:
    edges_xy = np.stack(keypoint_edges_all, axis=0)
  else:
    edges_xy = np.zeros((0, 2, 2))
  return keypoints_xy, edges_xy, edge_colors


def set_input_tensor(interpreter, image):
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = image

def inference_model(interpreter, image):
  set_input_tensor(interpreter, image)
  interpreter.invoke()
  output_details = interpreter.get_output_details()[0]
  output = interpreter.get_tensor(output_details['index'])
  return output


### Dance detection
def is_dance_helper(keypoint_locs):
  left_wrist = KEYPOINT_DICT['left_wrist']
  left_elbow = KEYPOINT_DICT['left_elbow']
  left_shoulder = KEYPOINT_DICT['left_shoulder']
  right_wrist = KEYPOINT_DICT['right_wrist']
  right_elbow = KEYPOINT_DICT['right_elbow']
  right_shoulder = KEYPOINT_DICT['right_shoulder']
  if left_shoulder in keypoint_locs:
    if left_wrist in keypoint_locs and keypoint_locs[left_wrist][1] < keypoint_locs[left_shoulder][1]:
      return True
    if left_elbow in keypoint_locs and keypoint_locs[left_elbow][1] < keypoint_locs[left_shoulder][1]:
      return True
  if right_shoulder in keypoint_locs:
    if right_wrist in keypoint_locs and keypoint_locs[right_wrist][1] < keypoint_locs[right_shoulder][1]:
      return True
    if right_elbow in keypoint_locs and keypoint_locs[right_elbow][1] < keypoint_locs[right_shoulder][1]:
      return True
  return False


MAX_LENGTH = 6
THRESHOLD = 3
is_dance_ls = []
def is_dance(img, output_img):
  output = inference_model(interpreter_pose, cv2.resize(img, (input_width, input_height)))
  (keypoint_locs, keypoint_edges, edge_colors) = keypoints_and_edges_for_display(output, img.shape[0], img.shape[1])

  # Draw the result on the frame
  for edge, color in zip(keypoint_edges, edge_colors):
    output_img = cv2.line(output_img, tuple(edge[0]), tuple(edge[1]), COLOR_DICT[color], thickness=3)
  for idx, loc in keypoint_locs.items():
    output_img = cv2.circle(output_img, tuple(loc), radius=3, color=(0, 0, 0), thickness=-1)

  # Determine if a person is dacing
  is_dance_ls.append(is_dance_helper(keypoint_locs))
  if len(is_dance_ls) > MAX_LENGTH:
    is_dance_ls.pop(0)
  cnt = 0
  for val in is_dance_ls:
    if val:
      cnt += 1
  if cnt >= THRESHOLD:
    output_img = cv2.putText(output_img, 'detect dance', org=(500,30), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                             fontScale=1, color=(0,0,0), thickness=2)
    return True
  else:
    return False


### Age Detection
has_child_ls = []
string_pred_age = ['04 - 06', '07 - 08','09 - 11','12 - 19','20 - 27','28 - 35','36 - 45','46 - 60','61 - 75']
def has_child(frame, output_image):
    font = cv2.FONT_HERSHEY_PLAIN

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor = 1.2, minNeighbors=5)
    tmp = False
    for x,y,w,h in faces:
        saved_image = frame
        input_im = saved_image[y:y+h, x:x+w]

        if input_im is None:
            print("Falied to detect the face")
        else:
            input_im = cv2.resize(input_im, (224,224))
            input_im = input_im.astype('float')
            input_im = input_im / 255.0

            output_data_age = inference_model(interpreter_age, input_im)
            index_pred_age = int(np.argmax(output_data_age))
            if index_pred_age == 0 or index_pred_age == 1:
                tmp = True
            prezic_age = string_pred_age[index_pred_age]

            output_image = cv2.putText(output_image, prezic_age, (x,y), font, 1, (255,255,255), 1, cv2.LINE_AA)
            output_image = cv2.rectangle(output_image, (x,y), (x+w,y+h), (255,255,255), 1)

    # Determine if there is child
    has_child_ls.append(tmp)
    if len(has_child_ls) > MAX_LENGTH:
        has_child_ls.pop(0)
    cnt = 0
    for val in has_child_ls:
        if val:
            cnt += 1
    if cnt >= THRESHOLD:
        output_image = cv2.putText(output_image, 'detect child', org=(500,60), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                             fontScale=1, color=(0,0,0), thickness=2)
        return True
    else:
        return False


### Set MQTT

# Every client needs a random ID
client = mqtt.Client(str(uuid.uuid1()))
# configure network encryption etc
client.tls_set()
# this is the username and pw we have setup for the class
client.username_pw_set('idd', 'device@theFarm')
#connect to the broker
client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)



### main

# Open webcam
cap = cv2.VideoCapture(0)
while(True):
    time_start = time()

    ret, img = cap.read()
    output_img = img.copy()
    if is_dance(img, output_img):
        client.publish("IDD/party/", "dance")
        # subprocess.run(['python', 'final_image1.py'])
    elif has_child(img, output_img):
        client.publish("IDD/party/", "child")
        # subprocess.run(['python', 'tired.py'])
    else:
        client.publish("IDD/party/", "none")
        # subprocess.run(['python', 'eye-icon.py'])

    fps = "FPS: " + str(round(1.0 / (time() - time_start), 2))
    cv2.putText(output_img, fps, (20,20), cv2.FONT_HERSHEY_PLAIN, 1, (250,250,250), 1, cv2.LINE_AA)
    cv2.imshow('detected (press q to quit)',output_img)

    # Press 'q' to leave
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        break

cv2.destroyAllWindows()

