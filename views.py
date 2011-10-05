from django import forms
from django.utils import simplejson
from django.http import HttpResponse
from django.shortcuts import render

class UploadFileForm(forms.Form):
#    title = forms.CharField(max_length=50)
    file = forms.FileField()


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f = open('/home/bteam/test.jpg','wb+')
            for chunk in request.FILES['file'].chunks():
                f.write(chunk)
        return HttpResponse("<textarea>%s</textarea>" % simplejson.dumps({'success':form.is_valid(),'value':1,'errors':form.errors}))
    else:
        form = UploadFileForm()
    return render(request,'upload.html',{'form':form})