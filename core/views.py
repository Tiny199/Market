from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()
    return render(request,'core/index.html',{
        'categories': categories,
        'items':items,
    })


def contact(request):
    return render(request,'core/contact.html')

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    return render(request, 'core/detail1.html',{
        'item': item,
        'related_items':related_items,
    })

def signupview(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')

    else:
        form = SignUpForm()

    return render(request, 'core/signup.html',{
        'form':form,
          })

@login_required
def newItemview(request):
    form = NewItemForm()

    return render(request, 'core/form.html',{
        'form': form,
        'title': 'New item',
    })