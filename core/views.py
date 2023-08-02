from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q

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
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'core/form.html', {
        'form': form,
        'title': 'New item',
    })


@login_required
def dashboardView(request):
    items= Item.objects.filter(created_by=request.user)
    return render(request, 'core/dashboard.html', {
        'items': items,
    })


@login_required
def deleteView(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard')


@login_required
def editItemview(request,pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES,instance=item)

        if form.is_valid():
            form.save()

            return redirect('detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'core/form1.html',{
        'form': form,
        'title': 'Edit item',
    })

def searchView(request):
    query = request.GET.get('query','')
    category_id = request.GET.get('category',0)
    categories = Category.objects.all()
    items= Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)
    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'core/search.html',{
        'items':items,
        'query': query,
        'categories':categories,
        'category_id':category_id,
    })
