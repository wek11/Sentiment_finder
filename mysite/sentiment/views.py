from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from .models import Link, Data
from sorting import get_data
from analysis import gather_sentiment
import sorting

# Create your views here.
def index(request):
    link_list = Link.objects.order_by('id')
    context = {
        'link_list': link_list,
    }

    # return HttpResponse(template.render(context, request))

    return render(request, 'index.html', context)

def url_display(request):
    if (request.method == "POST"):
        
        if (request.POST['link-url'] == ""):
            return render(request, "index.html")
        
        else:
            length = Link.objects.all().count()
            link = Link(link_url=request.POST['link-url'], text="")
            link.id = length + 1

            text = get_data(link.link_url)
            link.text = text

            link.save()

            return HttpResponseRedirect('/sentiment/results/' + str(link.id) + "/")
        
    else:
        return HttpResponseRedirect('/sentiment/')
    
def show_results(request, index):
    link = get_object_or_404(Link, id=index)
    link_data = get_object_or_404(Data, id=index)
    text_sentiment = gather_sentiment(link_data.text)
    return render(request, 'url-display.html', {'link_url': link.link_url, 'link_data': sorting.strip_to_sentences(link_data.text.split("',")), "text_sentiment": text_sentiment})

def delete_link(request, pk):
    link = get_object_or_404(Link, pk=pk)

    if request.method == 'POST':
        link.delete()
        Link.reset_id()
        return render(request, 'index.html')
    
    return render(request, 'index.html')