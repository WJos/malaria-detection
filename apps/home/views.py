# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
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
import torch


from django.conf import settings
from django import template
from django.contrib.auth.decorators import login_required
from .models import Patient
from .models import Diagnostic
from .models import Images
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .forms import PatientForm
from .forms import DiagnosticForm
from .forms import ImageForm
from django.shortcuts import get_object_or_404
from django.core.files.storage import FileSystemStorage


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def patients(request):
    form = PatientForm(request.POST or None)
    context = {}

    msg = None
    #load_template = request.path.split('/')[-1]

    if request.method == "POST":

        if form.is_valid():
            #form.save()
            pt = Patient(
                nom = form.cleaned_data.get("nom"),
                prenom = form.cleaned_data.get("prenom"),
                sexe = form.cleaned_data.get("sexe"),
                age = form.cleaned_data.get("age"),
                tel = form.cleaned_data.get("tel")
                )
            pt.save()
            return HttpResponseRedirect("/")
        else:
            msg = 'Error validating the form'

    html_template = loader.get_template('home/patients.html')
    context['segment'] = 'patients'
    context['patient_list'] = Patient.objects.all()
    context['form'] = form
    context['msg'] = msg

    #pprint(Patient.objects.all())

    return HttpResponse(html_template.render(context, request))





@login_required(login_url="/login/")
def diagnostics(request, id):
    form = DiagnosticForm(request.POST or None)
    context = {}

    msg = None
    #load_template = request.path.split('/')[-1]
    patient = get_object_or_404(Patient, pk=id)

    if request.method == "POST":

        if form.is_valid():
            #form.save()
            dgnt = Diagnostic(
                libelle = form.cleaned_data.get("libelle"),
                date = form.cleaned_data.get("date"),
                parasitemie = 0,
                patient = patient,
                )
            dgnt.save()
            return HttpResponseRedirect("/")
        else:
            msg = 'Error validating the form'

    html_template = loader.get_template('home/diagnostics.html')
    context['segment'] = 'diagnostics'
    context['diagnostic_list'] = Diagnostic.objects.filter(patient=patient)
    context['form'] = form
    context['msg'] = msg

    #pprint(Patient.objects.all())

    return HttpResponse(html_template.render(context, request))


def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d) if not os.path.isdir(os.path.join(d, f)) and not f.endswith('.json')]

@login_required(login_url="/login/")
def resultatsss(request, id):

    path= settings.MEDIA_ROOT+'images_2/3/'
    weigth_path = settings.MEDIA_ROOT+'/malaria_best.pt'

    imgs_path = listdir_fullpath(path)

    # Model
    model = torch.hub.load('/home/josh/django-adminlte/yolov5', 'custom', weigth_path, force_reload=True, source='local')
    results = model(imgs_path, size=640)

    for i in range(len(results.files)):
      filname = os.path.splitext(os.path.basename(results.files[i]))[0]
      data = results.pandas().xyxy[i].to_json(orient='records')
      with open(settings.MEDIA_ROOT+'images_2/3/'+filname+'.json', 'w') as f:
        f.writelines(data)


@login_required(login_url="/login/")
def resultatss(request, id):

    path= settings.MEDIA_ROOT+'images_2/3/'
    weigth_path = settings.MEDIA_ROOT+'/malaria_best.pt'

    imgs_path_tmp = imgs_path = listdir_fullpath(path)
    print(imgs_path)
    print(type(imgs_path[1]))

    for x in range(len(imgs_path)):
        print(len(imgs_path))
        print(os.path.basename(imgs_path[x]))
        print(os.path.splitext(os.path.basename(imgs_path[x]))[0])
        filname = os.path.splitext(os.path.basename(imgs_path[x]))[0]
        # Model
        #model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
        model = torch.hub.load('/home/josh/django-adminlte/yolov5', 'custom', weigth_path, force_reload=True, source='local')
        results = model(imgs_path[x], size=640)
        #results.save(settings.MEDIA_ROOT+'/images_2/3') #.print()  # or .show(), .save()
        data = results.pandas().xyxy[0].to_json(orient='records')
        #print(results.xyxy)
        #print(results.pandas().xyxy)
        #np.savetxt('/content/yolov5/runs/detect/expp/'+filname+'.txt', data, delimiter='\n')
        with open(settings.MEDIA_ROOT+'images_2/3/'+filname+'.json', 'w') as f:
          f.writelines(data)
        #print(results.pandas().xyxy[0].to_json(orient='records'))
    #'{"xmin":{"0":57.0689697266,"1":667.6612548828,"2":222.8783874512,"3":4.2053861618,"4":0.0},"ymin":{"0":391.7705993652,"1":399.3035888672,"2":414.774230957,"3":234.4476776123,"4":550.5960083008},"xmax":{"0":241.3835449219,"1":810.0,"2":343.804473877,"3":803.7391357422,"4":76.6811904907},"ymax":{"0":905.7978515625,"1":881.3966674805,"2":857.8250732422,"3":750.0233764648,"4":878.669921875},"confidence":{"0":0.8689641356,"1":0.8518877029,"2":0.8383761048,"3":0.6580058336,"4":0.4505961835},"class":{"0":0.0,"1":0.0,"2":0.0,"3":5.0,"4":0.0},"name":{"0":"person","1":"person","2":"person","3":"bus","4":"person"}}'
        
    # or probably better:
    #results.pandas().xyxy[0].to_json(orient='records')
    #'[{"xmin":57.0689697266,"ymin":391.7705993652,"xmax":241.3835449219,"ymax":905.7978515625,"confidence":0.8689641356,"class":0.0,"name":"person"},{"xmin":667.6612548828,"ymin":399.3035888672,"xmax":810.0,"ymax":881.3966674805,"confidence":0.8518877029,"class":0.0,"name":"person"},{"xmin":222.8783874512,"ymin":414.774230957,"xmax":343.804473877,"ymax":857.8250732422,"confidence":0.8383761048,"class":0.0,"name":"person"},{"xmin":4.2053861618,"ymin":234.4476776123,"xmax":803.7391357422,"ymax":750.0233764648,"confidence":0.6580058336,"class":5.0,"name":"bus"},{"xmin":0.0,"ymin":550.5960083008,"xmax":76.6811904907,"ymax":878.669921875,"confidence":0.4505961835,"class":0.0,"name":"person"}]'







@login_required(login_url="/login/")
def resultats(request, id):
    form = ImageForm(request.POST, request.FILES or None)
    context = {}

    msg = None
    #load_template = request.path.split('/')[-1]
    diagnostic = get_object_or_404(Diagnostic, pk=id)

    if request.method == "POST":

        if form.is_valid():
            #form.save()
            # image = request.FILES['image']
            # fs = FileSystemStorage()
            # filename = fs.save(image.name, image)
            # uploaded_file_url = fs.url(filename)
            files = request.FILES.getlist('image')
            for f in files:
                img = Images(
                    image = f,
                    #image = form.cleaned_data.get("image"),
                    diagnostic = diagnostic
                    )
                img.save()

            return HttpResponseRedirect("./")
        else:
            msg = 'Error validating the form'

    images = Images.objects.filter(diagnostic=diagnostic)
    html_template = loader.get_template('home/resultats.html')
    context['segment'] = 'resultats'
    context['img_path'] = images[0].image.path
    context['image_list'] = images
    context['form'] = form
    context['msg'] = msg

    return HttpResponse(html_template.render(context, request))




@login_required(login_url="/login/")
def getImage(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # get the nick name from the client side.
        image_id = request.GET.get("image_id", None)
        # check for the nick name in the database.
        instance = Images.objects.filter(id=image_id)
        if instance:
            # if nick_name found return not valid new friend
            ser_instance = serializers.serialize('json', [ instance, ])
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # if nick_name not found, then user can create a new friend.
            return JsonResponse({"valid":True}, status = 200)

    return JsonResponse({}, status = 400)


@login_required(login_url="/login/")
def imageView(request):
    a_file = open("/content/gdrive/MyDrive/Colab Notebooks/bbox_data/BloodImage_00007.txt", "r")

    # Stripping data from the txt file into a list #
    list_of_lists = []
    for line in a_file:
      stripped_line = line.strip()
      line_list = stripped_line.split()
      list_of_lists.append(line_list)
    a_file.close()

    # Conversion of str to int #
    stage1 = []
    for i in range(0, len(list_of_lists)):
      test_list = list(map(float, list_of_lists[i])) 
      stage1.append(test_list)

    #print(stage1)


    # Denormalizing # 
    stage2 = []
    mul = [1,640,480,640,480] #[constant, image_width, image_height, image_width, image_height]
    for x in stage1:
      c,xx,yy,w,h = x[0]*mul[0], x[1]*mul[1], x[2]*mul[2], x[3]*mul[3], x[4]*mul[4]    
      stage2.append([c,xx,yy,w,h])

    #print(stage2)


    # Convert (x_center, y_center, width, height) --> (x_min, y_min, width, height) #
    stage_final = []
    for x in stage2:
      c,xx,yy,w,h = x[0]*1, (x[1]-(x[3]/2)) , (x[2]-(x[4]/2)), x[3]*1, x[4]*1  
      stage_final.append([c,xx,yy,w,h])

    fig = plt.figure()

    #print(stage_final)


    #add axes to the image
    ax = fig.add_axes([0,0,1,1])

    # read and plot the image

    ## Location of the input image which is sent to model's prediction ##
    image = plt.imread('/content/gdrive/MyDrive/Colab Notebooks/bbox_data/BloodImage_00007.jpg')
    plt.imshow(image)

    # iterating over the image for different objects
    for x in stage_final:
      class_ = int(x[0])
      xmin = x[1]
      ymin = x[2]
      width = x[3]
      height = x[4]
      xmax = width + xmin
      ymax = height + ymin
        
        # assign different color to different classes of objects
      if class_ == 1:
        edgecolor = 'r'
        ax.annotate('RBC', xy=(xmax-40,ymin+20))
      elif class_ == 2:
        edgecolor = 'b'
        ax.annotate('WBC', xy=(xmax-40,ymin+20))
      elif class_ == 0:
        edgecolor = 'g'
        ax.annotate('Platelets', xy=(xmax-40,ymin+20))
            
        # add bounding boxes to the image
      rect = patches.Rectangle((xmin,ymin), width, height, edgecolor = edgecolor, facecolor = 'none')
        
      ax.add_patch(rect)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    
    html_template = loader.get_template('home/imageview.html')
    context['segment'] = 'imageview'
    context['uri'] = 'data:image/png;base64,' + urllib.parse.quote(string)

    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))

        # if load_template == 'patient1':
        #     context['segment'] = load_template
        #     context['patients'] = Patient.objects
        #     html_template = loader.get_template('home/' + load_template)

        #     if request.method == "POST":

        #         if form.is_valid():
        #             username = form.cleaned_data.get("username")
        #             password = form.cleaned_data.get("password")
        #             user = authenticate(username=username, password=password)
        #             if user is not None:
        #                 login(request, user)
        #                 return redirect("/")
        #             else:
        #                 msg = 'Invalid credentials'
        #         else:
        #             msg = 'Error validating the form'

        #     return HttpResponse(html_template.render(context, request))
            

        context['segment'] = load_template
        html_template = loader.get_template('home/' + load_templat)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

