!git clone https://github.com/ultralytics/yolov5  # clone
%cd yolov5
%pip install -qr requirements.txt  # install

import torch
from yolov5 import utils
display = utils.notebook_init()  # checks


!python detect.py --weights yolov5s.pt --img 640 --conf 0.25 --source data/images --save-txt --save-conf --name='boss' --nosave --agnostic-nms
#display.Image(filename='runs/detect/exp/zidane.jpg', width=600)

###############################################################################################
# PyTorch Hub
import torch

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Images
dir = 'https://ultralytics.com/images/'
imgs = [dir + f for f in ('zidane.jpg', 'bus.jpg')]  # batch of images

# Inference
print(imgs)
results = model(imgs, size=640)
#results.show() #.print()  # or .show(), .save()
results.xyxy[0]

print(len(imgs))
print(len(results.pandas().xyxy))
print(results.pandas().xyxy)

#######################################################################################################
# PyTorch Hub
import torch

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Images
dir = 'https://ultralytics.com/images/'
imgs = [dir + f for f in ('zidane.jpg', 'bus.jpg')]  # batch of images

# Inference
print(imgs)
results = model(imgs, size=640)
#results.show() #.print()  # or .show(), .save()
results.xyxy[0]

print(len(imgs))
print(len(results.pandas().xyxy))
print(results.pandas().xyxy)

###################################################################################################""""

import os
import requests
import base64
import io
from PIL import Image
import torch

path= "/content/yolov5/data/images"

def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

imgs_path = listdir_fullpath(path)
#print(imgs_path)
#print(os.path.basename(imgs_path[0]))

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
results = model(imgs_path, size=640)
#results.save() #.print()  # or .show(), .save()
#results.xyxy[0]
print(results.pandas().xyxy)

#print(imgs_path)
#for imgs in imgs_path:
#annotation_filename = os.path.splitext(filename)[0]+'.xml'
#print(annotation_filename)
#  print(imgs)

for x in range(len(imgs_path)):
    print(x)
    print(os.path.basename(imgs_path[0]))

###################################################################################################""""

import torch
import cv2
model = torch.hub.load('ultralytics/yolov5', 'yolov5l6', pretrained=True)

# Images
dir = 'https://ultralytics.com/images/'
imgs = [dir + f for f in ('zidane.jpg')]  # batch of images


path = 'https://raw.githubusercontent.com/ultralytics/yolov5/master/data/images/zidane.jpg'
frame = cv2.imread(path)
detections = model(path)
results = detections.pandas().xyxy[0].to_dict(orient="records")
for result in results:
                con = result['confidence']
                cs = result['class']
                x1 = int(result['xmin'])
                y1 = int(result['ymin'])
                x2 = int(result['xmax'])
                y2 = int(result['ymax'])
                # Do whatever you want
                cv2.rectangle(path, (x1, y1), (x2, y2), (0,255,0), 3)

###################################################################################################""""

def drawBoundingBox(self,imgcv,result):
        for box in result:
            # print(box)
            x1,y1,x2,y2 = (box['topleft']['x'],box['topleft']['y'],box['bottomright']['x'],box['bottomright']['y'])
            conf = box['confidence']
            # print(conf)
            label = box['label']
            if conf < self.predictThresh:
                continue
            # print(x1,y1,x2,y2,conf,label)
            cv2.rectangle(imgcv,(x1,y1),(x2,y2),(0,255,0),6)
            labelSize=cv2.getTextSize(label,cv2.FONT_HERSHEY_COMPLEX,0.5,2)
            # print('labelSize>>',labelSize)
            _x1 = x1
            _y1 = y1#+int(labelSize[0][1]/2)
            _x2 = _x1+labelSize[0][0]
            _y2 = y1-int(labelSize[0][1])
            cv2.rectangle(imgcv,(_x1,_y1),(_x2,_y2),(0,255,0),cv2.FILLED)
            cv2.putText(imgcv,label,(x1,y1),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,0),1)
        return imgcv 

###################################################################################################""""

import os
import requests
import numpy as np
import base64
import io
from PIL import Image
import torch

path= "/content/yolov5/data/images"

def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

imgs_path_tmp = imgs_path = listdir_fullpath(path)
print(imgs_path)
#print(os.path.basename(imgs_path[0]))
print(type(imgs_path[1]))

for x in range(len(imgs_path)):
    print(len(imgs_path))
    print(os.path.basename(imgs_path[x]))
    # Model
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    results = model(imgs_path[x], size=640)
    results.save('/content/yolov5/runs/detect/expp') #.print()  # or .show(), .save()
    #print(results.xyxy)
    print(results.pandas().xyxy)
    np.savetxt(r'/content/yolov5/runs/detect/expp/j.txt', results.pandas().xyxy, delimiter='\n')

results.pandas().xyxy[0].to_json()
'{"xmin":{"0":57.0689697266,"1":667.6612548828,"2":222.8783874512,"3":4.2053861618,"4":0.0},"ymin":{"0":391.7705993652,"1":399.3035888672,"2":414.774230957,"3":234.4476776123,"4":550.5960083008},"xmax":{"0":241.3835449219,"1":810.0,"2":343.804473877,"3":803.7391357422,"4":76.6811904907},"ymax":{"0":905.7978515625,"1":881.3966674805,"2":857.8250732422,"3":750.0233764648,"4":878.669921875},"confidence":{"0":0.8689641356,"1":0.8518877029,"2":0.8383761048,"3":0.6580058336,"4":0.4505961835},"class":{"0":0.0,"1":0.0,"2":0.0,"3":5.0,"4":0.0},"name":{"0":"person","1":"person","2":"person","3":"bus","4":"person"}}'
    
# or probably better:
results.pandas().xyxy[0].to_json(orient='records')
'[{"xmin":57.0689697266,"ymin":391.7705993652,"xmax":241.3835449219,"ymax":905.7978515625,"confidence":0.8689641356,"class":0.0,"name":"person"},{"xmin":667.6612548828,"ymin":399.3035888672,"xmax":810.0,"ymax":881.3966674805,"confidence":0.8518877029,"class":0.0,"name":"person"},{"xmin":222.8783874512,"ymin":414.774230957,"xmax":343.804473877,"ymax":857.8250732422,"confidence":0.8383761048,"class":0.0,"name":"person"},{"xmin":4.2053861618,"ymin":234.4476776123,"xmax":803.7391357422,"ymax":750.0233764648,"confidence":0.6580058336,"class":5.0,"name":"bus"},{"xmin":0.0,"ymin":550.5960083008,"xmax":76.6811904907,"ymax":878.669921875,"confidence":0.4505961835,"class":0.0,"name":"person"}]'


###################################################################################################""""


###################################################################################################""""

def plot_data_example(df: pd.DataFrame,
                      root_dir: str,
                      img_path: str, 
                      colors: dict):

    image = cv2.imread(os.path.join(root_dir, img_path)).astype("uint8")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = np.zeros(image.shape, dtype="uint8")

    fig, ax = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(25, 8))
    ax[1].imshow(image, aspect="auto")
    ax[1].set_title("Original Image", fontsize=22, fontweight='bold', y=1.07)
    ax[0].set_title("Image with Bounding Boxes", fontsize=22, fontweight='bold', y=1.07)


    bb_info = df.loc[df["pathname"] == img_path, ["x_min", "x_max", "y_min", "y_max", "category"]].values
    for i_bb in bb_info:

        cmin, cmax, rmin, rmax = i_bb[:-1].astype('int')
        label = i_bb[-1]
        bbox = patches.Rectangle((cmin,rmin),cmax-cmin,rmax-rmin,linewidth=1, 
                                 edgecolor=label2hex[label], facecolor='none')
        boxes[rmin:rmax, cmin:cmax] = label2rgb[label]

        ax[0].add_patch(bbox)
        ax[0].text(cmin, rmin, label, bbox=dict(fill=True, color=label2hex[label]))
        ax[0].imshow(image, aspect="auto")
        ax[0].imshow(boxes,  alpha=0.3, aspect="auto")
        ax[0].text(cmin, rmin, label, bbox=dict(fill=True, color=label2hex[label]))

    plt.tight_layout()
    fig.savefig("data_exemple1.svg", format='svg', bbox_inches='tight', pad_inches=0.2)
    fig.savefig("data_exemple1.png", format='png', bbox_inches='tight', pad_inches=0.2)
    plt.show()
###################################################################################################""""


###################################################################################################""""


###################################################################################################""""


###################################################################################################""""


###################################################################################################""""


###################################################################################################""""


###################################################################################################""""


###################################################################################################""""


###################################################################################################""""


###################################################################################################""""


