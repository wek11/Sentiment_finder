from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import Link
from sorting import get_data, strip_to_sentences
from analysis import gather_sentiment

# Displays index.html
def index(request):
    Link.reset_id(Link)
    link_list = Link.objects.order_by('id')
    context = {
        'link_list': link_list,
    }
    return render(request, 'index.html', context)

# Gets the data from a submitted link and stores it in the Link model
def url_display(request):
    if (request.method == "POST"): # If post, run these things
        
        if (request.POST['link-url'] == ""):
            return render(request, "index.html", {'link_list': Link.objects.order_by('id')})
        
        else:
            length = Link.objects.all().count()
            link = Link(link_url=request.POST['link-url'], text="", id=length+1)

            text = get_data(link.link_url)
            link.text = strip_to_sentences(text, link.link_url)

            link.save()

            return HttpResponseRedirect('/sentiment/results/' + str(link.id) + "/")
        
    else: #If get, does this
        return HttpResponseRedirect('/sentiment/')
    
# Method to shwo the results of a link, ran after the data is retrieved or when
# a link is clicked on in the Navbar
def show_results(request, index):
    link_list = Link.objects.order_by('id')
    link = get_object_or_404(Link, id=index)
    text_sentiment, smiley = gather_sentiment(link.text)
    context = {
        'link_url': link.link_url, 
        'link_data': link.text.split("|"), 
        "text_sentiment": text_sentiment, 
        "link_list": link_list,
        "smiley" : smiley}
    return render(request, 'url-display.html', context)

# Method used when deleting a link, called from the 
# ajax requests in the JS files
@csrf_exempt
def delete_link(request, pk):
    link = get_object_or_404(Link, pk=pk)

    if request.method == 'POST':
        link.delete()
        i = 1
        for i in range(1, Link.objects.all().count()):
             if i >= pk:
                url = get_object_or_404(Link, id=i + 1)
                url.id = url.id - 1
                url.save()
    
        return JsonResponse({"name": 'worked'})
    
    return render(request, 'index.html')