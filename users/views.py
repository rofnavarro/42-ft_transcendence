from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Friendship
from .forms import EditNicknameForm, ProfilePictureForm

@login_required
def	user_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    friends = user.friends.all()
    is_friend = request.user.friends.filter(username=user.username).exists()

    if request.method == 'POST' and 'nickname' in request.POST:
        form = EditNicknameForm(request.POST, instance=request.user)
        if form.is_valid():
            request.user.nickname = form.cleaned_data['nickname'] or request.user.username
            request.user.save()
            return redirect('users:profile', username=username)
    else:
        form = EditNicknameForm(instance=request.user)

    if request.method == 'POST' and 'profile_picture' in request.FILES:
        picture_form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
        if picture_form.is_valid():
            picture_form.save()
            return redirect('users:profile', username=username)
    else:
        picture_form = ProfilePictureForm(instance=request.user)

    context = {
        'user_info': user,
        'friends': friends,
        'is_friend': is_friend,
        'form': form,
        'picture_form': picture_form,
    }
    return render(request, 'users/profile.html', context)

@login_required
def	send_friend_request(request, username):
	to_user = get_object_or_404(CustomUser, username=username)
		
	if request.user != to_user:
		friendship, created = Friendship.objects.get_or_create(user1=request.user, user2=to_user)
		if created:
			Friendship.objects.get_or_create(user1=to_user, user2=request.user)
	return redirect('users:profile', username=username)

@login_required
def	view_friends(request):
	friends = request.user.friends.all()
	return render(request, 'users/friends_list.html', {'friends': friends})

@login_required
def wanna_play(request, username):
    user = get_object_or_404(CustomUser, username=username)
    return render(request, 'users/wanna_play.html', {'user': user})

@login_required
def local_play(request, username):
    user = get_object_or_404(CustomUser, username=username)
    return render(request, 'users/local_play.html', {'user': user})
