from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView, FormView, ListView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.db.models import Q, Count, Prefetch
from django.http import HttpResponse
from django.urls import reverse_lazy
from .models import User, Topic, Room, Message
from .forms import MyUserCreationForm, UserForm, RoomForm


class BaseViewMixin:
    """Mixin to share common methods like fetching topics and query params."""

    def get_query_params(self, request):
        q = request.GET.get('q', '')
        page = max(int(request.GET.get('page', 1)), 1)
        size = max(int(request.GET.get('size', 9)), 9)
        return q, page, size

    def get_topics(self):
        topics = Topic.objects.annotate(room_count=Count('room')).all()[:5]
        topics.count = Topic.objects.count()
        return topics


class HomeView(BaseViewMixin, TemplateView):
    template_name = 'base/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q, page, size = self.get_query_params(self.request)
        rooms_query = Room.objects.select_related('host', 'topic').filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
        ) if q else Room.objects.select_related('host', 'topic').all()
        paginator = Paginator(rooms_query, size)
        context.update({
            'rooms': paginator.get_page(page),
            'page_range': paginator.get_elided_page_range(page),
            'room_count': paginator.count,
            'topics': self.get_topics(),
            'room_messages': Message.objects.select_related('user', 'room').filter(Q(room__topic__name__icontains=q))[:3],
            'q': q,
        })
        return context


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        """Redirect to the next page if available, otherwise to 'home'."""
        next_url = self.request.GET.get('next')
        return next_url if next_url else reverse_lazy('home')

    def form_invalid(self, form):
        """Override to add custom messages on invalid login."""
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)


class UserLogoutView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, 'User logged out successfully!')
        return super().get(request, *args, **kwargs)


class UserRegisterView(FormView):
    template_name = 'base/register.html'
    form_class = MyUserCreationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = user.username.lower()
        user.save()
        login(self.request, user)
        return super().form_valid(form)


class UserProfileView(BaseViewMixin, TemplateView):
    template_name = 'base/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        q, page, size = self.get_query_params(self.request)
        rooms_query = user.room_set.select_related('host', 'topic').all()
        paginator = Paginator(rooms_query, size)
        context.update({
            'user': user,
            'rooms': paginator.get_page(page),
            'page_range': paginator.get_elided_page_range(page),
            'room_messages': user.message_set.select_related('user', 'room').all()[:3],
            'topics': self.get_topics(),
        })
        return context


class EditUserView(LoginRequiredMixin, FormView):
    template_name = 'base/edit-user.html'
    form_class = UserForm
    success_url = reverse_lazy('user-profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instance': self.request.user})
        return kwargs

    def form_valid(self, form):
        form.save()
        return redirect('user-profile', pk=self.request.user.id)


class RoomListView(BaseViewMixin, ListView):
    model = Room
    context_object_name = 'rooms'
    template_name = 'base/room_list.html'

    def get_queryset(self):
        q, _, _ = self.get_query_params(self.request)
        return Room.objects.select_related('host', 'topic').filter(
            Q(topic__name__icontains=q) | Q(
                name__icontains=q) | Q(description__icontains=q)
        ) if q else Room.objects.select_related('host', 'topic').all()


class RoomDetailView(View):
    def get(self, request, pk):
        room = get_object_or_404(
            Room.objects.prefetch_related(
                Prefetch('message_set',
                         queryset=Message.objects.select_related('user')),
                'participants'
            ).select_related('host', 'topic'), id=pk
        )
        context = {
            'room': room,
            'room_messages': room.message_set.all(),
            'participants': room.participants.all()
        }
        return render(request, 'base/room.html', context)

    def post(self, request, pk):
        room = get_object_or_404(Room, id=pk)
        Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        room.joined_count = room.participants.count()
        room.save()
        return redirect('get-room', pk=room.id)


class CreateRoomView(LoginRequiredMixin, FormView):
    template_name = 'base/room_form.html'
    form_class = RoomForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        topic_name = self.request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=self.request.user,
            topic=topic,
            name=form.cleaned_data['name'],
            description=form.cleaned_data['description']
        )
        return super().form_valid(form)


class UpdateRoomView(LoginRequiredMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'base/room_form.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        room = self.get_object()
        if room.host != request.user:
            return HttpResponse('You are not allowed here!')
        return super().dispatch(request, *args, **kwargs)


class DeleteRoomView(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = 'base/delete.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        room = self.get_object()
        if room.host != request.user:
            return HttpResponse('You are not allowed here!')
        return super().dispatch(request, *args, **kwargs)
