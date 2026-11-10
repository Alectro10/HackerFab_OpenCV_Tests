import os
import glob
import cv2 as cv
import numpy as np

# ---------------------------------------------------------------------
# 1. SETUP PARAMETERS
# ---------------------------------------------------------------------
# If your paper has 3x5 squares: internal corners are (2, 4)
# If your paper has 3x5 internal intersections: internal corners are (3, 5)
CHECKERBOARD_CORNERS = (2, 4)  # (columns - 1, rows - 1)
square_size = 25.4             # mm per square

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare 3D object points (0,0,0), (25.4, 0, 0), etc.
num_corners = CHECKERBOARD_CORNERS[0] * CHECKERBOARD_CORNERS[1]
objp = np.zeros((num_corners, 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD_CORNERS[0], 0:CHECKERBOARD_CORNERS[1]].T.reshape(-1, 2) * square_size

objpoints = []  # 3D world points
imgpoints = []  # 2D image plane points

# Use a wildcard to process all captured calibration views, not just one file
images = glob.glob('calibration_code/*.jpg')

if not images:
    raise FileNotFoundError("No calibration images found in calibration_code/")

image_size = None

# ---------------------------------------------------------------------
# 2. DETECT CORNERS ACROSS ALL FRAMES
# ---------------------------------------------------------------------
for fname in images:
    img = cv.imread(fname)
    if img is None:
        continue

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    if image_size is None:
        image_size = gray.shape[::-1]

    # Flags help with hand-drawn contrast and uneven illumination
    flags = cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_NORMALIZE_IMAGE
    ret, corners = cv.findChessboardCorners(gray, CHECKERBOARD_CORNERS, flags)

    if ret:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Visual verification
        preview = img.copy()
        cv.drawChessboardCorners(preview, CHECKERBOARD_CORNERS, corners2, ret)
        cv.imshow('Detected Corners', preview)
        cv.waitKey(200)
    else:
        print(f"Corners NOT found in: {fname}")

cv.destroyAllWindows()

# Check minimum frame count
print(f"Successfully processed {len(objpoints)} / {len(images)} images.")
if len(objpoints) < 5:
    raise RuntimeError(
        f"Only {len(objpoints)} valid frame(s) detected. "
        "OpenCV requires multiple frames at varying angles for reliable calibration."
    )

# ---------------------------------------------------------------------
# 3. CAMERA CALIBRATION & UNDISTORTION
# ---------------------------------------------------------------------
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(
    objpoints, imgpoints, image_size, None, None
)

print("\nCamera Matrix:\n", mtx)
print("\nDistortion Coefficients:\n", dist)

# Compute reprojection error
total_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
    total_error += error

print(f"\nMean Reprojection Error: {total_error / len(objpoints):.4f} pixels")