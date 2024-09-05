from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import CustomUser, Friendship
from .forms import EditNicknameForm

@login_required
def	user_profile(request, username):
	try:
		user = get_object_or_404(CustomUser, username=username)
	except CustomUser.DoesNotExist:
		raise Http404("Usuário não existe")
	friends = user.friends.all()
	is_friend = request.user.friends.filter(username=user.username).exists()

	if request.method == 'POST':
		form = EditNicknameForm(request.POST, instance=request.user)
		if form.is_valid():
			if 'nickname' in form.cleaned_data and form.cleaned_data['nickname']:
				user.nickname = form.cleaned_data['nickname']
			else:
				user.nickname = user.username
			user.save()
			return redirect('users:profile', username=username)
	else:
		form = EditNicknameForm(instance=request.user)

	context = {
		'user_info': user,
		'friends': friends,
		'is_friend': is_friend,
		'form': form
		}
	return render(request, 'users/profile.html', context)

@login_required
def	send_friend_request(request, username):
	to_user = get_object_or_404(CustomUser, username=username)
	if request.user != to_user:
		Friendship.objects.get_or_create(user1=request.user, user2=to_user)
	return redirect('users:profile', username=username)

@login_required
def	view_friends(request):
	friends = request.user.friends.all()
	return render(request, 'users/friends_list.html', {'friends':friends})