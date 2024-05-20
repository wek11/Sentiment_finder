from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import Link, Data
from sorting import get_data, strip_to_sentences
from analysis import gather_sentiment

# Create your views here.
def index(request):
    Link.reset_id(Link)
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
            print(text)
            link.save()

            return HttpResponseRedirect('/sentiment/results/' + str(link.id) + "/")
        
    else:
        return HttpResponseRedirect('/sentiment/')
    
def show_results(request, index):
    link = get_object_or_404(Link, id=index)
    text_sentiment = gather_sentiment(link.text)
    return render(request, 'url-display.html', {'link_url': link.link_url, 
    'link_data': strip_to_sentences(link.text, link.link_url), "text_sentiment": text_sentiment})

@csrf_exempt
def delete_link(request, pk):
    link = get_object_or_404(Link, pk=pk)

    if request.method == 'POST':
        link.delete()
        Link.reset_id(Link)
        return JsonResponse({"name": 'worked'})
    
    return render(request, 'index.html')