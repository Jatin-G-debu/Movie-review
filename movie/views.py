from django.shortcuts import  get_object_or_404 ,render
from django.http import HttpResponse
from .models import Movie , Review
from django.shortcuts import redirect 
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    movies=Movie.objects.all()
    return render(request,'home.html',{'movies':movies})

def detail(request, movie_id):
    movie = get_object_or_404(Movie,pk=movie_id)
    reviews = Review.objects.filter(movie = movie)
    return render(request, 'detail.html', {'movie':movie,'reviews': reviews})        

@login_required
def createreview(request, movie_id):   
    movie = get_object_or_404(Movie,pk=movie_id) 
    if request.method == 'GET':
        return render(request, 'createreview.html', {'form':ReviewForm(), 'movie': movie})            
    else:
        try:
            form = ReviewForm(request.POST)
            newReview = form.save(commit=False)
            newReview.user = request.user
            newReview.movie = movie
            #newReview.text = request.POST['text']
            #newReview.watchAgain = request.POST['watchAgain']
            #newReview.rating = request.POST['rating']// these fields autoom-populated by django!
            newReview.save()
            return redirect('detail', newReview.movie.id)            
        except ValueError:
            return render(request, 'createreview.html', {'form':ReviewForm(),'error':'bad data passed in'})      

@login_required
def updatereview(request, review_id):
    review = get_object_or_404(Review,pk=review_id,user=request.user) # other users can't access the review. only user who created this review can update/delete it.
    if request.method =='GET':
        form = ReviewForm(instance=review)
        return render(request, 'updatereview.html', {'review': review,'form':form})
    else:
        try:
            form = ReviewForm(request.POST, instance=review)
            form.save()
            return redirect('detail', review.movie.id)            
        except ValueError:
            return render(request, 'updatereview.html', {'review': review,'form':form,'error':'Bad data in form'})

@login_required
def deletereview(request, review_id):
    review = get_object_or_404(Review, pk=review_id,user=request.user)    
    review.delete()        
    return redirect('detail', review.movie.id)            
