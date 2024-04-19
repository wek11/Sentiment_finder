from django.shortcuts import render, get_object_or_404
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

        link = get_object_or_404(Link, id=1)
        link_data = get_object_or_404(Data, id=1)

        if (request.POST['link-url'] == ""):
            return render(request, "index.html")
        
        else:
            link.link_url = request.POST['link-url']
            link.save()
            
            text = get_data(link.link_url)
            link_data.text = text
            link_data.save()

            return HttpResponseRedirect('/sentiment/results')
        
    else:
        return HttpResponseRedirect('/sentiment/')
    
def show_results(request):
    link = get_object_or_404(Link, id=1)
    link_data = get_object_or_404(Data, id=1)
    text_sentiment = gather_sentiment(link_data.text)
    return render(request, 'url-display.html', {'link_url': link.link_url, 'link_data': sorting.strip_to_sentences(link_data.text.split("',")), "text_sentiment": text_sentiment})