import numpy as np
from scipy.fftpack import dct

# Import OpenCV.
import cv2
def nsf5_steganalysis(image):
  # Compute the DCT coefficients of the image.
  dct_coeffs = dct(image)
  # Compute the mean and standard deviation of the DCT coefficients.
  mean = np.mean(dct_coeffs)
  std = np.std(dct_coeffs)
  # Compute the nsF5 steganalysis score.
  score = (mean - 128) / std
  return score
images = []
for i in range(5):
  image = cv2.imread('/content/stego_image.png')
  images.append(image)
# Perform nsF5 steganalysis on each image.
steganalysis_scores = []
for image in images:
  score = nsf5_steganalysis(image)
  steganalysis_scores.append(score)
# Print the steganalysis scores for all 5 images.
print("Steganalysis scores:")
for i in range(5):
  print(f"Image {i}: {steganalysis_scores[i]}")
