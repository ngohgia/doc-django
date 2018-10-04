import csv

from django.shortcuts import render

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse

from myapp.models import Document
from myapp.forms import DocumentForm


def show(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            return HttpResponseRedirect(reverse('show'))
    else:
        form = DocumentForm() # A empty, unbound form

    data = process_document(Document.objects.last())
    text = " | ".join([", ".join(row) for row in data])

    return render(request, 'show.html', {'text': text, 'form': form, 'graphic': ""})

def process_document(doc):
    reader = csv.reader(open(doc.docfile.path,'r'))
    data = []
    for row in reader:
        data.append(row)

    return data
