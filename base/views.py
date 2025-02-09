from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import User, Topic, Room, Message
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, MyUserCreationForm, RoomForm
from django.db.models import Q, Prefetch, Count
from django.core.paginator import Paginator
from .utils import CustomPaginator


def get_query_params(request):
    """
    Helper function to get query parameters
    """
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    page = max(int(request.GET.get('page', 1)), 1)
    size = max(int(request.GET.get('size', 9)), 9)
    return q, page, size


def get_paginated_rooms(q, page, size):
    """
    Helper function to fetch rooms based on search query
    """
    if q:
        # Filter rooms based on the search query
        rooms_query = Room.objects.only(
            'name', 'joined_count', 'created', 'topic', 'host__username', 'host__avatar'
        ).select_related('host', 'topic').filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )
    else:
        # Fetch all rooms without filtering
        rooms_query = Room.objects.only(
            'name', 'joined_count', 'created', 'topic', 'host__username', 'host__avatar'
        ).select_related('host', 'topic').all()

    p = Paginator(rooms_query, size)
    rooms = p.get_page(page)
    page_range = p.get_elided_page_range(page)
    rooms_count = p.count
    return rooms, page_range, rooms_count


def get_topics():
    """Helper function to fetch topics"""
    topics = Topic.objects.annotate(room_count=Count('room')).all()[:5]
    topics.count = Topic.objects.count()
    return topics


def get_room_messages(q):
    """Helper function to fetch recent room messages"""
    room_messages = Message.objects.only(
        'body', 'created', 'room__name', 'user__username', 'user__avatar'
    ).select_related('user', 'room').filter(
        Q(room__topic__name__icontains=q)
    )[:3]
    return room_messages


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username dose not exist')
            return redirect('login')

        user = authenticate(request, email=user.email, password=password)

        if user is not None:
            login(request, user)

            return redirect(request.GET['next'] if 'next' in request.GET else 'home')
        else:
            messages.error(request, "Password is incorrect")

    return render(request, 'base/login.html')


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    messages.info(request, "User is successful logout!")
    return redirect('login')


def user_register(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            # Log the user in and redirect to the home page
            login(request, user)
            return redirect('home')

    return render(request, 'base/register.html', {'form': form})


@login_required(login_url='login')
def edit_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/edit-user.html', {'form': form})


def user_profile(request, pk):
    user = User.objects.get(id=pk)

    page = max(int(request.GET.get('page', 1)), 1)
    size = max(int(request.GET.get('size', 6)), 6)

    rooms_query = user.room_set.only('name', 'joined_count', 'created', 'topic', 'host__username',
                                     'host__avatar').select_related('host', 'topic').all()
    p = Paginator(rooms_query, size)
    rooms = p.get_page(page)
    page_range = p.get_elided_page_range(page)

    room_messages = user.message_set.only(
        'body', 'created', 'room__name', 'user__username', 'user__avatar').select_related('user', 'room').all()[:3]
    topics = get_topics()

    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics, 'page_range': page_range}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    topics = Topic.objects.all()[0:30]
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    topics = Topic.objects.all()[0:30]
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


def get_room(request, pk):
    room = Room.objects.prefetch_related(
        Prefetch('message_set', queryset=Message.objects.select_related('user')),
        'participants').select_related('host', 'topic').get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if not request.user.is_anonymous and request.method == 'POST':
        Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        room.joined_count = room.participants.all().count()
        room.save()
        return redirect('get-room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})


def home(request):
    # Step 1: Get query parameters (q, page, size)
    q, page, size = get_query_params(request)

    # Step 2: Fetch rooms and apply pagination logic
    rooms, page_range, room_count = get_paginated_rooms(q, page, size)

    # Step 3: Fetch additional data (topics and recent messages)
    topics = get_topics()
    room_messages = get_room_messages(q)

    # Step 4: Prepare context data
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages,
        'page_range': page_range,
        'q': q,
    }

    # Step 5: Render template
    return render(request, 'base/home.html', context)


def topics_page(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    page = max(int(request.GET.get('page', 1)), 1)
    size = max(int(request.GET.get('size', 6)), 6)

    topics_query = Topic.objects.annotate(
        room_count=Count('room')).filter(name__icontains=q)
    p = Paginator(topics_query, size)
    topics = p.get_page(page)
    page_range = p.get_elided_page_range(page)

    topics.count = Topic.objects.count()
    return render(request, 'base/topics.html', {'topics': topics, 'q': q, 'page_range': page_range})


def activity_page(request):
    room_messages = Message.objects.all()[:20]
    return render(request, 'base/activity.html', {'room_messages': room_messages})
