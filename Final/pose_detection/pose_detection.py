from tflite_runtime.interpreter import Interpreter
import numpy as np
import cv2

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


def _keypoints_and_edges_for_display(keypoints_with_scores,
                                     height,
                                     width,
                                     keypoint_threshold=0.11):
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
  keypoints_all = []
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
    keypoints_all.append(kpts_above_thresh_absolute)

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
  if keypoints_all:
    keypoints_xy = np.concatenate(keypoints_all, axis=0)
  else:
    keypoints_xy = np.zeros((0, 17, 2))

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


# Load model
interpreter = Interpreter("lite-model_movenet_singlepose_lightning_tflite_int8_4.tflite")
interpreter.allocate_tensors()
_, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']

# Open webcam
cap = cv2.VideoCapture(0)
while(True):
    # Inference the model by input frame
    ret, img = cap.read()
    output = inference_model(interpreter, cv2.resize(img, (input_width, input_height)))
    (keypoint_locs, keypoint_edges, edge_colors) = _keypoints_and_edges_for_display(output, img.shape[0], img.shape[1])

    # Draw the result on the frame
    for edge, color in zip(keypoint_edges, edge_colors):
        img = cv2.line(img, tuple(edge[0]), tuple(edge[1]), COLOR_DICT[color], thickness=3)
    for loc in keypoint_locs:
        img = cv2.circle(img, tuple(loc), radius=3, color=(0, 0, 0), thickness=-1)
    cv2.imshow('detected (press q to quit)',img)

    # Press 'q' to leave
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        break

cv2.destroyAllWindows()

