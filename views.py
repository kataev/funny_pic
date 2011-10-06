from django import forms
from django.utils import simplejson
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from settings import PROJECT_PATH
from subprocess import call
import datetime

class UploadFileForm(forms.Form):
    head = forms.CharField(max_length=500,required=False)
    text = forms.CharField(max_length=50,required=False)
    file = forms.FileField()

#    ajax = forms.BooleanField(required=False)


def upload_file(request):
    """

    """
    STATIC_ROOT = PROJECT_PATH + '/static/'
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            f = open(STATIC_ROOT+'img/%s.jpg' % datetime.datetime.now().isoformat(),'wb+')
            for chunk in request.FILES['file'].chunks():
                f.write(chunk)
            f.close()
            head = form.cleaned_data.get('head')
            text = form.cleaned_data.get('text')
            font = PROJECT_PATH+"/fonts/PT_Sans/PT_Sans-Web-Bold.ttf"
            out = f.name+'out.jpg'
            call(['convert','-scale','640',f.name,out])
            call(['mogrify', '-bordercolor','black','-border','2','-bordercolor','white',
                  '-border','2','-bordercolor','black','-border','70x0',out])
            if head: call(['montage','-geometry','+0+0','-background','black','-fill','white',
                  '-font',font,'-pointsize', '64',
                  '-label',head,out,out])
            if text: call(['montage','-geometry','+0+0','-background','black','-fill','white',
                  '-font',font,'-pointsize', '32',
                  '-label',text,out,out])
            if head or text: call(['mogrify','-bordercolor','black','-border','5x45',out])
            call(['convert',out,out])
        if request.POST.get('ajax'):
            return HttpResponse("<textarea>%s</textarea>" % simplejson.dumps({'success':form.is_valid(),
               'value':1,'errors':form.errors,'img':out.split('/')[-1]}))
        else:
            return HttpResponseRedirect('/static/img/%s' % out.split('/')[-1])
    else:

        form = UploadFileForm()
    return render(request,'index.html',{'form':form})