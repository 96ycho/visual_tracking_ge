import json
import csv
from numpy import *

with open('result.json') as bbox_file:
	bbox = json.load(bbox_file)
bbox = bbox["res"]

with open('groundtruth_rect.txt') as gt_file:
	gt = list(csv.reader(gt_file))\

m = len(gt)
tx, ty, tw, th = [], [], [], []
for step in range(m):
	tx.append(float(gt[step][0]))
	ty.append(float(gt[step][1]))
	tw.append(float(gt[step][2]))
	th.append(float(gt[step][3]))

bbox = array(bbox)
x = bbox[:,0].tolist()
y = bbox[:,1].tolist()
w = bbox[:,2].tolist()
h = bbox[:,3].tolist()

iou_li = []
for step in range(m):
	intersect_ul_x = max(x[step], tx[step])
	intersect_ul_y = max(y[step], ty[step])
	area = w[step] * h[step]
	tarea = tw[step] * th[step]
	ceil_x = x[step] + w[step]
	ceil_y = y[step] + h[step]
	tceil_x = tx[step] + tw[step]
	tceil_y = ty[step] + th[step]
	intersect_br_x = min(ceil_x, tceil_x)
	intersect_br_y = min(ceil_y, tceil_y)
	intersect_w = intersect_br_x - intersect_ul_x
	intersect_h = intersect_br_y - intersect_ul_y
	intersect_area = intersect_w * intersect_h
	iou_li.append(float(intersect_area)/(area + tarea - intersect_area))

auc = 0.0
th = 0.0
while th <= 1.0:
	success = 0
	for iou in iou_li:
		if iou >= th:
			success = success + 1
	sr = float(success)/m
	auc = auc + sr
	th = th + 0.0001
	#print(sr)
print(auc/10001)
