from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from users.forms import UserForm
from .forms import UpdateForm, ImageForm
from django.contrib.auth.hashers import check_password
from django.contrib import messages, auth
# from django.views.decorators.csrf import csrf_exempt

from users.models import Mlike, Slike, Ugenres, Members
from entmt_info.models import Movies, Series, Genres
from django.db.models import Q


# csrf token의 다른 방법
# @csrf_exempt


# 회원가입
def signup(request):
    # 현재 페이지 url
    url = request.META.get('HTTP_REFERER')

    # POST 방식의 request일 경우
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            # 입력받은 username, password로 로그인하기
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            # 회원가입 후 로그인 상태로 메인 페이지 돌아가기
            return redirect('home')
            # 회원가입 후 선호 장르 선택
            # return redirect('users:edit_genre')

            # return redirect(url)
    # else:
    #     form = UserForm()
    return render(request, 'users/signup.html', {'form': form})


def mypage(request):
    user_id = request.user.id
    mlike_list = Mlike.objects.filter(ml_member=user_id)
    slike_list = Slike.objects.filter(sl_member=user_id)
    movie_list = []
    series_list = []

    for mlike in mlike_list:
        # mlike_code_list.append(mlike.ml_movie_id)
        movie_list.append(Movies.objects.get(movie_id=mlike.ml_movie_id))
        # print(f'--{mlike}({mlike.ml_movie_id})={movie_list}')
    for slike in slike_list:
        series_list.append(Series.objects.get(series_id=slike.sl_series_id))

    content = {
        'movie_list': movie_list,
        'series_list': series_list
    }
    # return render(request, 'users/mypage2.html', content)
    return render(request, 'users/userprofile.html', content)


def my_favorite(request):
    print('----------으에에에ㅔ엥------------')
    user_id = request.user.id
    mlike_list = Mlike.objects.filter(ml_member=user_id)
    slike_list = Slike.objects.filter(sl_member=user_id)
    movie_list = []
    series_list = []

    for mlike in mlike_list:
        # mlike_code_list.append(mlike.ml_movie_id)
        movie_list.append(Movies.objects.get(movie_id=mlike.ml_movie_id))
        # print(f'--{mlike}({mlike.ml_movie_id})={movie_list}')
    for slike in slike_list:
        series_list.append(Series.objects.get(series_id=slike.sl_series_id))
    # print(f'-----------{len(movie_list) + len(series_list)}')
    content = {
        'movie_list': movie_list,
        'series_list': series_list,
        # 'list_length': len(movie_list) + len(series_list)
    }
    return render(request, 'users/favorite.html', content)
    # return render(request, 'users/userprofile.html', content)


def change_password(request):
    if request.method == "POST":
        user = request.user
        origin_password = request.POST["origin_password"]
        if check_password(origin_password, user.password):
            new_password = request.POST["new_password"]
            confirm_password = request.POST["confirm_password"]
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, '비밀번호가 변경되었습니다!')
                return redirect('users:change_password')
            else:
                print('비번 다름!!!')
                messages.error(request, '비밀번호가 다릅니다!')
        else:
            messages.error(request, '비밀번호를 잘못 입력하셨습니다.')
        # return render(request, 'users/change_password.html')
        return render(request, 'users/userprofile.html')

    else:
        # return render(request, 'users/change_password.html')
        return render(request, 'users/userprofile.html')


def update(request):
    # 현재 url
    url = request.META.get('HTTP_REFERER')
    member = get_object_or_404(Members, pk=request.user.id)

    if request.method == 'POST':
        my_form = UpdateForm(request.POST, instance=member)

        if my_form.is_valid():
            my_form.save()

            messages.success(request, '회원정보가 변경되었습니다!')
            # return redirect('users:update')
            return redirect(url)

        else:
            print('무효한 폼 ㅜㅜ')

    else:
        my_form = UpdateForm(instance=member)

    context = {
        'update_form': my_form
    }
    # return render(request, 'users/update.html', context)
    return render(request, 'users/userprofile.html', context)


def genre(request):
    genres = Genres.objects.all()
    genre_list = []
    for genre in genres:
        if Ugenres.objects.filter(Q(ug_genre=genre) & Q(ug_member=request.user)).exists():
            genre_list.append({'genre': genre, 'status': True})
        else: genre_list.append({'genre': genre, 'status': False})
    print(genre_list)
    context = {
            'genres': genre_list
        }
    return render(request, 'users/genre.html', context)


def edit_genre(request):

    if request.method == 'POST':
        selected = request.POST.getlist('selected')
        ugenres = Ugenres.objects.filter(ug_member=request.user)
        selected_ug = [str(ugenre.ug_genre.genre_id) for ugenre in ugenres]
        code_list = list(set(selected + selected_ug))
        print(selected)
        print(selected_ug)
        print(code_list)

        # selected, selected_ug 둘다있는거 pass
        # selected 에는 있고, selected_ug에는 없는거 save()
        # selected 에는 없고, selected_ug에는 있는거 delete()

        for code in code_list:
            genre = Genres.objects.get(pk=code)
            if (code in selected) and (code not in selected_ug):
                ugenre = Ugenres()
                ugenre.ug_genre = genre
                ugenre.ug_member = request.user
                ugenre.save()

            elif (code not in selected) and (code in selected_ug):
                ugenre = Ugenres.objects.get(Q(ug_genre=genre) & Q(ug_member=request.user))
                ugenre.delete()
            else: pass

        messages.success(request, '선호 장르가 업데이트되었습니다!')
        print('ok')

    return redirect('users:genre')


def change_image(request):
    # 현재 url
    url = request.META.get('HTTP_REFERER')
    member = get_object_or_404(Members, pk=request.user.id)

    if request.method == 'POST':
        print('post 방식===')
        my_form = ImageForm(request.FILES, instance=member)

        if my_form.is_valid():
            my_form.save()
            print('이미지 변경 완료~~~')

            messages.success(request, '프로필 이미지가 변경되었습니다!')
            # return redirect('users:update')
            return redirect(url)

        else:
            print('무효한 폼 ㅜㅜ')

    else:
        my_form = ImageForm(instance=member)

    context = {
        'update_form': my_form
    }
    # return render(request, 'users/update.html', context)
    return render(request, 'users/userprofile.html', context)


def profile(request):
    # user_id = request.user.id
    # mlike_list = Mlike.objects.filter(ml_member=user_id)
    # slike_list = Slike.objects.filter(sl_member=user_id)
    # movie_list = []
    # series_list = []
    #
    # for mlike in mlike_list:
    #     # mlike_code_list.append(mlike.ml_movie_id)
    #     movie_list.append(Movies.objects.get(movie_id=mlike.ml_movie_id))
    #     # print(f'--{mlike}({mlike.ml_movie_id})={movie_list}')
    # for slike in slike_list:
    #     series_list.append(Series.objects.get(series_id=slike.sl_series_id))
    #
    # content = {
    #     'movie_list': movie_list,
    #     'series_list': series_list
    # }
    # # return render(request, 'users/mypage2.html', content)
    return render(request, 'users/userprofile.html')


# 찜한 영화 목록
def favorite(request):
    pass


# 사용자가 별점 매긴 영화 목록
def ratings(request):
    pass


# 선호 장르 선택
def preference(request):
    pass
