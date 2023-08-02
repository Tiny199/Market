from django.shortcuts import render,get_object_or_404,redirect
from core.models import Item
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

# Create your views here.
@login_required
def newConversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)
    if item.created_by == request.user:
        return redirect('dashboard')

    conversations = ConversationModel.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        return redirect('detailll',pk=conversations.first().id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = ConversationModel.objects.filter.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('detail',pk=item_pk)
        else:
            form = ConversationMessageForm()

        return render(request, 'conversation/newcon.html',{
            'form':form
        })


@login_required
def inbox(request):
    conversations = ConversationModel.objects.filter(members__in=[request.user.id])

    return render(request, 'conversation/inbox.html',{
        'conversations':conversations
    })


@login_required
def detail(request,pk):
    conversation = ConversationModel.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form= ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.convesation = conversation
            conversation_message.created_by =request.user
            conversation_message.save()

            conversation.save()

            return redirect('detailll', pk=pk)
    return render(request, 'conversation/detail.html',{
        'conversation':conversation,
        'form': form
    })