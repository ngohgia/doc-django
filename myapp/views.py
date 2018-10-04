import csv

from django.shortcuts import render

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse

from myapp.models import Document
from myapp.forms import DocumentForm

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

import datetime
import random


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

    plot(request)

    return render(request, 'show.html', {'text': text, 'form': form, 'graphic': ""})

def process_document(doc):
    data = []
    if doc != None:
        reader = csv.reader(open(doc.docfile.path,'r'))
        for row in reader:
            data.append(row)

    return data

def plot(request):
    # dummy data
    fig = Figure()

    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()

    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')

    canvas.print_png(response)
    return response
