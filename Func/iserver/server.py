import cv2
from utils.iworker import IWorker

wo = IWorker(onnx_path="../temp/case2/onnx/modified.onnx", npy_path="../temp/case2/onnx/dense.npy")
im = cv2.imread("../temp/dataset/test/1_def/def_7724.jpeg")
result = wo.inference(im)

cv2.imshow("concat", cv2.hconcat((result.cam / 255, result.merged)))
cv2.waitKey()
