from django.http import HttpResponse
from django.shortcuts import render

from .pipeline import RagPipeline

from .models import Chat, User

from .forms import ChatInput, DocumentForm

# Create your views here.


rag = RagPipeline()
def home(request):
    return render(request,'index.html')

def upload_document(request):
    existing_docs = []
    for i in User.objects.all():
        existing_docs.append(i.document.name)
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
                if  User.objects.filter(document=document).exists():
                    return render(request, 'upload.html', {'form_submitted':True, 'show':False}) 
                user_instance = User.objects.create(name=name,document=document)
                user_instance.save()
                rag.process_doc(user_instance.id)
                return render(request, 'upload.html',{'form_submitted':True,'show':False})      

        else:
            print(form.errors)  # Print form errors to console for debugging
            return HttpResponse("Error", content_type='text/plain')
    else:
        form = DocumentForm()

        return render(request, 'upload.html',{'form':form,'form_submitted':False,'show':False, 'existing_docs':existing_docs})

def get_answer(request):
    if request.method == 'POST':

        form = ChatInput(request.POST)
        # check whether it's valid:
        # print(form.is_valid())
        # resume=request.FILES['resume']

        if form.is_valid():
            # User.objects.create()
            
            ques=request.POST['input']
            if ques is not None:  
                chat_instance = Chat.objects.create(input=ques)
                chat_instance.save()
                ans=rag.convert_query_to_vector(chat_instance.id)
                return render(request, 'chat_screen.html',{'form_submitted':True,'show':False, 'answer':ans})      

        else:
            print(form.errors)  # Print form errors to console for debugging
            return HttpResponse("Error", content_type='text/plain')
    else:
        form = ChatInput()
        return render(request, 'chat_screen.html',{'form':form,'form_submitted':False,'show':False})

def chat(request):
    form = ChatInput()
    return render(request, 'chat_screen.html', {'form':form,'form_submitted':False,'show':False})
