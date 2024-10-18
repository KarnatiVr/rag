from django.http import HttpResponse
from django.shortcuts import render

from .models import User

from .forms import DocumentForm

# Create your views here.

def home(request):
    return render(request,'index.html')

def upload_document(request):
    if request.method == 'POST':

        form = DocumentForm(request.POST,request.FILES)
        # check whether it's valid:
        # print(form.is_valid())
        # resume=request.FILES['resume']

        if form.is_valid():
            # User.objects.create()
            document=request.FILES['document']
            name=request.POST['name']
            if document is not None:  
                user_instance = User.objects.create(name=name,document=document)
                user_instance.save()
                # extract_text_from_pdf.delay(user_instance.id) 
                return render(request, 'upload.html',{'form_submitted':True,'show':False})      

        else:
            print(form.errors)  # Print form errors to console for debugging
            return HttpResponse("Error", content_type='text/plain')
    else:
        form = DocumentForm()
        return render(request, 'upload.html',{'form':form,'form_submitted':False,'show':False})
    


def chat(request):
    return render(request, 'chat_screen.html')
