from django import forms
from django.utils import simplejson
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from settings import PROJECT_PATH
import datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps

fonts = [('Andika.ttf', 'Andika'),
 ('EBGaramond.ttf', 'EBGaramond'),
 ('KellySlab.ttf', 'KellySlab'),
 ('PT_Sans-Caption.ttf', 'PT_Sans-Caption'),
 ('AnonymousPro.ttf', 'AnonymousPro'),
 ('Forum.ttf', 'Forum'),
 ('Lobster.ttf', 'Lobster'),
 ('PT_Sans-Web.ttf', 'PT_Sans-Web'),
 ('Cuprum.ttf', 'Cuprum'),
 ('IstokWeb.ttf', 'IstokWeb'),
 ('Neucha.ttf', 'Neucha'),
 ('DidactGothic.ttf', 'DidactGothic'),
 ('Jura.ttf', 'Jura'),
 ('OpenSans.ttf', 'OpenSans')]



class UploadFileForm(forms.Form):
    head = forms.CharField(max_length=500,required=False)
    text = forms.CharField(max_length=50,required=False)
    file = forms.FileField()
    font = forms.ChoiceField(choices=fonts,required=False)

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
            if form.cleaned_data.get('font'):
                font_path = PROJECT_PATH+"/fonts/%s" % form.cleaned_data.get('font')
            else:
                font_path = PROJECT_PATH+"/fonts/PT_Sans-Web.ttf"
	    print request.POST
            out = f.name.split('.')
            out.insert(-1, 'out')
            if out[-1].lower() not in ['jpeg', 'jpg']:
                out[-1] = 'jpg'
            out = '.'.join(out)

            top = 40
            right = 40
            bottom = 40
            left = 40
            head_font_size = 36
            text_font_size = 18

            head_font = ImageFont.truetype(font_path, head_font_size, encoding='utf-8')
            text_font = ImageFont.truetype(font_path, text_font_size, encoding='utf-8')

            img_upload = Image.open(f.name)
            img_upload_brd = ImageOps.expand(img_upload, border=2, fill='white')

            img_new = Image.new(
                img_upload_brd.mode, (
                    img_upload_brd.size[0] + left + right,
                    img_upload_brd.size[1] + top + bottom + head_font.getsize(head)[1] + text_font.getsize(text)[1]
                )
            )
            img_new.paste(
                img_upload_brd, (
                    top,
                    right,
                    img_upload_brd.size[0]+bottom,
                    img_upload_brd.size[1]+left
                )
            )

            draw = ImageDraw.Draw(img_new)
            x = (img_new.size[0] / 2) - (head_font.getsize(head)[0] / 2)
            draw.text((x, img_upload_brd.size[1]+top+10), head, fill='white', font=head_font)

            x = (img_new.size[0] / 2) - (text_font.getsize(text)[0] / 2)
            draw.text((x, img_upload_brd.size[1]+top+head_font.getsize(head)[1]+10), text, fill='white', font=text_font)

            img_new.save(out, 'JPEG')

        if request.POST.get('ajax'):
            return HttpResponse("<textarea>%s</textarea>" % simplejson.dumps({'success':form.is_valid(),
               'value':1,'errors':form.errors,'img':out.split('/')[-1]}))
        else:
            return HttpResponseRedirect('/static/img/%s' % out.split('/')[-1])
    else:

        form = UploadFileForm()
    return render(request,'index.html',{'form':form})
