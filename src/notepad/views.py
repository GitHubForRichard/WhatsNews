from django.shortcuts import render, redirect, get_object_or_404
from .forms import NoteModelForm
from .models import Note

# Create your views here.

# CRUD
# create, update, retrieve, delete

def create_view(request):
    form = NoteModelForm(request.POST or None, request.FILES or None)

    # make the user that submit the request to the owner of this form
    if form.is_valid():
        form.instance.user = request.user
        form.save()
        return redirect('/notes/list')
    context = {
        'form': form
    }
    return render(request, "notepad/templates/notepad/create.html",context)

def list_view(request):
    notes = Note.objects.all()
    context = {
        'object_list': notes
    }
    return render(request, "notepad/templates/notepad/list.html", context)

def delete_view(request, id):
    item_to_delete = Note.objects.filter(pk=id) # pk means primary keu, it will return a list
    if item_to_delete.exists():
        if request.user == item_to_delete[0].user: # check if the user to delete is the owner of the note
            item_to_delete[0].delete()
    return redirect('/notes/list')

def update_view(request, id):
    unique_note = get_object_or_404(Note, id=id)
    form = NoteModelForm(request.POST or None, request.FILES or None, instance=unique_note)

    # make the user that submit the request to the owner of this form
    if form.is_valid():
        form.instance.user = request.user
        form.save()
        return redirect('/notes/list')
    context = {
        'form': form
    }
    return render(request, "notepad/templates/notepad/create.html",context)