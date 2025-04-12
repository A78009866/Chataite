from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.db import IntegrityError, models
from django.utils import timezone
import json
import pytz
from django.utils.html import strip_tags
from django.http import Http404
from .models import Message, Notification, CustomUser as User

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def login_view(request):
    if request.user.is_authenticated:
        return redirect('chat_list')
        
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('chat_list')
        else:
            return render(request, 'login.html', {'error': 'اسم المستخدم أو كلمة المرور غير صحيحة'})
    return render(request, 'login.html')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('chat_list')
        
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']

        if password != password_confirmation:
            return render(request, 'signup.html', {'error': 'كلمة المرور غير متطابقة.'})

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'اسم المستخدم مستخدم بالفعل.'})

        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            login(request, user)
            return redirect('chat_list')
        except IntegrityError:
            return render(request, 'signup.html', {'error': 'حدث خطأ أثناء التسجيل.'})
    return render(request, 'signup.html')

@login_required
def chat_list(request, username=None):
    try:
        current_user = request.user
        users = User.objects.exclude(id=current_user.id)
        
        if username:
            users = users.filter(username=username)

        query = request.GET.get('q', '')
        if query:
            users = users.filter(username__icontains=strip_tags(query))

        user_data = []
        for user in users:
            last_sent = Message.objects.filter(
                sender=current_user,
                receiver=user
            ).order_by('-timestamp').first()
            
            last_received = Message.objects.filter(
                sender=user,
                receiver=current_user
            ).order_by('-timestamp').first()

            last_message = last_sent if (last_sent and last_received and last_sent.timestamp > last_received.timestamp) else last_received or last_sent

            is_new = False
            if last_message and last_message.receiver == current_user and not last_message.is_read:
                is_new = True
                last_message.is_read = True
                last_message.save()

            user_data.append({
                'user': user,
                'last_message': strip_tags(last_message.content) if last_message else "لا توجد رسائل",
                'last_time': last_message.timestamp if last_message else None,
                'is_new': is_new
            })

        user_data.sort(key=lambda x: x['last_time'] or timezone.datetime.min.replace(tzinfo=pytz.UTC), reverse=True)
        
        return render(request, 'chat_list.html', {
            'all_users': user_data,
            'current_user': current_user,
            'focused_user': username
        })

    except Exception as e:
        raise Http404(f"حدث خطأ: {str(e)}")
@login_required
def chat_view(request, username):
    other_user = get_object_or_404(User, username=username)
    
    unread_messages = Message.objects.filter(
        sender=other_user,
        receiver=request.user,
        is_read=False
    )
    
    for msg in unread_messages:
        msg.mark_as_seen()
    
    messages = Message.objects.filter(
        sender__in=[request.user, other_user], 
        receiver__in=[request.user, other_user]
    ).order_by("timestamp")

    return render(request, "chat.html", {
        "messages": messages, 
        "other_user": other_user
    })

@login_required
def send_message(request):
    if request.method == "POST":
        data = json.loads(request.body)
        receiver = get_object_or_404(User, username=data["receiver"])
        content = data["content"].strip()

        if not content:
            return JsonResponse({"error": "لا يمكن إرسال رسالة فارغة"}, status=400)

        message = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
            is_read=False,
            seen_at=None
        )
        
        Notification.objects.create(
            recipient=receiver,
            sender=request.user,
            notification_type='message',
            content=content
        )

        return JsonResponse({
            "id": message.id,
            "sender": message.sender.username,
            "receiver": receiver.username,
            "content": message.content,
            "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "is_read": message.is_read,
            "seen_at": None
        })

@login_required
def get_messages(request, username):
    other_user = get_object_or_404(User, username=username)
    
    messages = Message.objects.filter(
        (models.Q(sender=request.user, receiver=other_user) | 
        models.Q(sender=other_user, receiver=request.user))
    ).order_by("timestamp")

    return JsonResponse([
        {
            "id": msg.id,
            "sender": msg.sender.username,
            "receiver": msg.receiver.username,
            "content": msg.content,
            "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "is_read": msg.is_read,
            "seen_at": msg.seen_at.strftime("%Y-%m-%d %H:%M:%S") if msg.seen_at else None
        }
        for msg in messages
    ], safe=False)