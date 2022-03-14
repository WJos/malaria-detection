

import os
import urllib, base64
import io
from PIL import Image
import torch
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import pathlib
from pathlib import Path

from django import template
from django.conf import settings

register = template.Library()
    
@register.simple_tag
def images_with_bbox(url):
    
    ###########################################################
    url1 = pathlib.Path(os.path.join(settings.MEDIA_ROOT, Path(url.path).with_suffix('.json')))
    url2 = pathlib.Path(settings.MEDIA_ROOT+url.name)
    if url1.exists() and url2.exists():
      path_abs = Path(url.name)
      df = pd.read_json(os.path.join(settings.MEDIA_ROOT, Path(url.path).with_suffix('.json')),dtype={"xmin": pd.to_numeric, "ymin": pd.to_numeric, "xmax": pd.to_numeric, "ymax": pd.to_numeric, "confidence": pd.to_numeric, "class": pd.to_numeric})

      fig = plt.figure()

      #add axes to the image
      ax = fig.add_axes([0,0,1,1])

      # read and plot the image

      ## Location of the input image which is sent to model's prediction ##
      image = plt.imread(url2)
      plt.imshow(image)

      # iterating over the image for different objects
      for x in range(len(df)):
        conff_ = df['confidence'][x]
        if conff_ >= 0.7:
          class_ = int(df['class'][x])
          conf_ = df['confidence'][x]
          name_ = df['name'][x]
          #print(class_) 
          xmin = df['xmin'][x]
          ymin = df['ymin'][x]
          xmax = df['xmax'][x]
          ymax = df['ymax'][x]
          width = xmax-xmin
          height = ymax-ymin
            
            # assign different color to different classes of objects
          if class_ == 0:
            edgecolor = 'r'
            ax.annotate(name_+' '+str(round(conf_, 2)), xy=(xmin,ymin))
          elif class_ == 1:
            edgecolor = 'b'
            ax.annotate(name_+' '+str(round(conf_, 2)), xy=(xmin,ymin))
          elif class_ == 2:
            edgecolor = 'g'
            ax.annotate(name_+' '+str(round(conf_, 2)), xy=(xmin,ymin))
                
            # add bounding boxes to the image
          rect = patches.Rectangle((xmin,ymin), width, height, edgecolor = edgecolor, facecolor = 'none')
          ax.add_patch(rect)

      buf = io.BytesIO()
      fig.savefig(buf, format='png')
      buf.seek(0)
      string = base64.b64encode(buf.read())
      
      uri = 'data:image/png;base64,' + urllib.parse.quote(string)

      ###########################################################

      return uri
    else:
      return 'jos'



@register.simple_tag
def count_rbc(url):
    
    ###########################################################
    # url1 = pathlib.Path(os.path.join(settings.MEDIA_ROOT, Path(url.path).with_suffix('.json')))
    # rbc = 0
    # if url1.exists():
    #   df = pd.read_json(os.path.join(settings.MEDIA_ROOT, Path(url.path).with_suffix('.json')),dtype={"xmin": pd.to_numeric, "ymin": pd.to_numeric, "xmax": pd.to_numeric, "ymax": pd.to_numeric, "confidence": pd.to_numeric, "class": pd.to_numeric})

    #   # iterating over the image for different objects
    #   for x in range(len(df)):
    #     name_ = df['name'][x]
    #     if name_ == 'RBC':
    #       rbc = rbc + 1
      ###########################################################

  #return os.path.dirname(url)
  return [Path(os.path.join(url, f)).isfile() for f in os.listdir(url) if not os.path.isdir(os.path.join(url, f)) and f.endswith('.json') and os.path.isfile(os.path.join(url, f))]
    # else:
    #   return 0




@register.simple_tag
def images_with_bbox_exist(url):
  url1 = pathlib.Path(os.path.join(settings.MEDIA_ROOT, Path(url.path).with_suffix('.json')))
  url2 = pathlib.Path(settings.MEDIA_ROOT+url.name)
  if url1.exists() and url2.exists():
    return True
  else:
    return False


@register.simple_tag
def images_with_bboxx(url):
  path_abs = Path(url.name)
  #print(path.parent.absolute())
  #df = pd.read_json(str(path_abs.parent.absolute())+'/'+os.path.splitext(os.path.basename(url.name))[0]+'.json',dtype={"xmin": pd.to_numeric, "ymin": pd.to_numeric, "xmax": pd.to_numeric, "ymax": pd.to_numeric, "confidence": pd.to_numeric, "class": pd.to_numeric})
  return pathlib.Path(settings.MEDIA_ROOT+url.name) #os.path.join(settings.MEDIA_ROOT, Path(url.path).with_suffix('.json'))
  #return settings.MEDIA_ROOT+str(path_abs.parent.absolute())+'/'+os.path.splitext(os.path.basename(url.name))[0]+'.json'
  #return settings.MEDIA_ROOT+url.path+os.path.splitext(os.path.basename(url.name))[0]+'.json'
#settings.MEDIA_ROOT+os.path.splitext(os.path.basename(url.name))[0]+'.json'
