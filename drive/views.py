from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Folder, File
from django.contrib import messages
from django.http import Http404


# Create your views here.

@login_required
def dashboard(request):
    parent_id = request.GET.get('parent_id')
    parent_folder = Folder.objects.filter(id=parent_id, owner=request.user).first() if parent_id else None
    folders = Folder.objects.filter(owner=request.user, parent=parent_folder)
    files = File.objects.filter(owner=request.user, folder=parent_folder)

    return render(request, 'dashboard.html', {
        'folders': folders,
        'files': files,
        'parent_folder': parent_folder,
    })

@login_required
def create_folder(request):
    if request.method == 'POST':
        folder_name = request.POST.get('folder_name')
        parent_folder_id = request.POST.get('parent_folder')  
        
        parent_folder = None
        if parent_folder_id:
            parent_folder = get_object_or_404(Folder, id=parent_folder_id)

        Folder.objects.create(
            name=folder_name,
            parent=parent_folder,
            owner=request.user
        )
        return redirect('dashboard') 
    return redirect('dashboard') 

@login_required
def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        folder_id = request.POST.get('parent_folder')  
        if folder_id:
            try:
                parent_folder = Folder.objects.get(id=folder_id, owner=request.user)
            except Folder.DoesNotExist:
                raise Http404("Folder does not exist or does not belong to the user.")
        else:
            parent_folder = None  

        file_name = uploaded_file.name
        new_file = File.objects.create(
            name=file_name,
            file=uploaded_file,
            folder=parent_folder,
            owner=request.user
        )

        return redirect('dashboard')
    return render(request, 'dashboard.html')

@login_required
def delete(request, item_type, item_id):
    if item_type == 'folder':
        Folder.objects.filter(id=item_id, owner=request.user).delete()
    else:
        File.objects.filter(id=item_id, owner=request.user).delete()
    return redirect('dashboard')

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
