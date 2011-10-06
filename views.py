from django import forms
from django.utils import simplejson
from django.http import HttpResponse
from django.shortcuts import render
from settings import PROJECT_PATH
import os

class UploadFileForm(forms.Form):
    head = forms.CharField(max_length=500,required=False)
    body = forms.CharField(max_length=50,required=False)
    file = forms.FileField()


def upload_file(request):
    """

    """
    STATIC_ROOT = PROJECT_PATH + '/static/'
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f = open(STATIC_ROOT+'img/test1.jpg','wb+')
            for chunk in request.FILES['file'].chunks():
                f.write(chunk)
            f.close()
            os.popen(u"bash dem.sh -i %s -o %s -h '%s' -t '%s'" % (f.name,f.name+'.jpg',
                                                                   unicode(form.cleaned_data.get('head')),
                unicode(form.cleaned_data.get('body'))))
        return HttpResponse("<textarea>%s</textarea>" % simplejson.dumps({'success':form.is_valid(),
               'value':1,'errors':form.errors,'img':f.name.split('/')[-1]}))
    else:

        form = UploadFileForm()
    return render(request,'upload.html',{'form':form})