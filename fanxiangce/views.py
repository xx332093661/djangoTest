# coding: utf-8
from .models import Album, Message, Photo, Comment
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, reverse, render_to_response
from django.core.paginator import Paginator
from django.conf import settings
from .forms import LoginForm, CommentForm, RegisterForm
from django.contrib import messages, auth
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer  # 生成令牌用
from django.contrib.auth.hashers import make_password   # 注册用户时候保存密码加密问题
from django.template import loader
from django.core.mail import EmailMultiAlternatives


def page_not_found2(request, exception):
    return render_to_response('fanxiangce/404.html')


def page_error(request):
    return render_to_response('fanxiangce/500.html')


def album(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    placeholder = 'http://p1.bpimg.com/567591/15110c0119201359.png'
    photo_amount = len(album.photos)
    if photo_amount == 0:
        album.cover = placeholder
    elif photo_amount != 0 and album.cover == placeholder:
        album.cover = album.photos[0].path
    if request.user != album.author and album.no_public:
        raise Http404('相册未公开')
    page = request.GET.get('page', 1)
    if album.asc_order:
        order_by = 'id'
    else:
        order_by = '-id'
    pagination = Paginator(album.photos.all().order_by(order_by), per_page=settings.FANXIANGCE_PHOTOS_PER_PAGE)
    photos = pagination.get_page(page)
    if len(photos) == 0:
        no_pic = True
    else:
        no_pic = False

    if request.user.is_authenticated:
        likes = request.user.photo_likes.all().order_by('id')
        likes = [{'id': like.like_photo, 'timestamp': like.timestamp, 'url_t': like.like_photo.url_t} for like in likes]
    else:
        likes = ""

    return render(request, 'fanxiangce/album.html', {
        'album': album,
        'photos': photos,
        'likes': likes,
        'no_pic': no_pic,
    })


def albums(request, username):
    user = get_object_or_404(User, username=username)
    page = request.GET.get('page', 1)

    album_paginator = Paginator(user.albums.all().order_by('-id'), settings.FANXIANGCE_ALBUMS_PER_PAGE)
    albums = album_paginator.get_page(page)
    photo_count = sum([len(album.photos.all()) for album in albums])
    album_count = len(albums)

    about_me = user.profile.about_me

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                body = form.cleaned_data['body']
                message = Message(body=body, author=request.user.id, user=user)
                message.save()
                messages.success(request, '你的评论已经发表')
                return HttpResponseRedirect(reverse('fanxiangce:albums', args=(username,)))
            else:
                messages.error(request, '请先登陆')
    else:
        form = CommentForm()

    comments = user.messages.all().order_by('id')

    return render(request, 'fanxiangce/albums.html', {
        'form': form,
        'comments': comments,
        'user': user,
        'albums': albums,
        'album_count': album_count,
        'photo_count': photo_count,
        'about_me': about_me,
    })


def unconfirmed(request):
    return render(request, 'fanxiangce/unconfirmed.html')


@login_required
def resend_confirmation(request):
    token = request.user.profile.generate_confirmation_token()
    text_content = ''
    confirm_url = request.build_absolute_uri(reverse('fanxiangce:confirm', args=[token]))
    html_content = loader.render_to_string('fanxiangce/confirm.html',
                                           {'user': request.user, 'token': token, 'confirm_url': confirm_url})
    msg = EmailMultiAlternatives('账户邮件确认', text_content, settings.DEFAULT_FROM_EMAIL, [request.user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    messages.info(request, '确认邮件已发送到你的邮箱，请查收')
    return HttpResponseRedirect(reverse('fanxiangce:index'))


@login_required()
def confirm(request, token):
    def do_confirm():
        s = Serializer(settings.SECRET_KEY)
        try:
            data = s.loads(token)
        except Exception:
            return False

        if data.get('confirm') != request.user.id:
            return False

        request.user.profile.confirmed = True
        request.user.profile.save()
        return True

    if do_confirm():
        messages.success(request, '你的账户已经确认')
    else:
        messages.warning(request, '抱歉，验证链接无效或已经过期')

    return HttpResponseRedirect(reverse('fanxiangce:index'))


def explore(request):
    photos = Photo.objects.all().order_by('-id')
    photos = [photo for photo in photos if not photo.album.no_public and photo.author != request.user]
    photo_type = "new"
    return render(request, 'fanxiangce/explore.html', {
        'photos': photos,
        'photo_type': photo_type,
    })


def index(request):
    if request.user.is_authenticated and request.user.username != 'admin':
        photos = request.user.profile.followed_photos
    else:
        photos = Photo.objects.all()[:20]
    context = {
        'photos': photos
    }
    return render(request, 'fanxiangce/index.html', context)


def login(request):
    res = True
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                auth.login(request, user)
                messages.success(request, '登陆成功')
                return HttpResponseRedirect(reverse('fanxiangce:index'))
            else:
                res = False
                messages.error(request, '用户名或者密码错误')
        else:
            res = False
            messages.error(request, '输入错误')
    if res:
        return render(request, 'fanxiangce/login.html', {'form': form})
    else:
        return HttpResponseRedirect(reverse('fanxiangce:login'))


def photo(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)

    album = photo.album
    if not album:
        raise Http404('异常相片')
    if request.user != album.author and album.no_public:
        raise Http404('相册未公开')

    photo_index = [p.id for p in album.photos.all().order_by('order')].index(photo.id) + 1

    if request.user.is_authenticated and request.user.username != 'admin':
        likes = request.user.photo_likes.all().order_by('-id')
    else:
        likes = None

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                body = form.cleaned_data['body']
                comment = Comment(body=body, author=request.user.id, photo=photo_id)
                comment.save()
                messages.success(request, '你的评论已经发表')
                return HttpResponseRedirect(reverse('fanxiangce:photo', args=(photo_id,)))
            else:
                messages.error(request, '请先登陆')
    else:
        form = CommentForm()

    page = request.GET.get('page', 1)

    paginator = Paginator(photo.comments.all().order_by('id'), settings.FANXIANGCE_COMMENTS_PER_PAGE)
    comments = paginator.get_page(page)
    amount = len(comments)

    return render(request, 'fanxiangce/photos.html', {
        'form': form,
        'album': album,
        'amount': amount,
        'photo': photo,
        'comments': comments,
        'photo_index': photo_index,
        'photo_sum': paginator.count
    })


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']):
                messages.error(request, '用户已存在')
            else:
                if form.cleaned_data['password'] != form.cleaned_data['password2']:
                    messages.error(request, '两次密码输入不一致')
                else:
                    user = User.objects.create(
                        username=form.cleaned_data['username'],
                        password=make_password(form.cleaned_data['password']),
                        email=form.cleaned_data['email']
                    )
                    user.save()
                    user.profile.name = form.cleaned_data['name']
                    token = user.profile.generate_confirmation_token()

                    # text_content = '账户邮件确认.'
                    text_content = ''
                    confirm_url = request.build_absolute_uri(reverse('fanxiangce:confirm', args=[token]))
                    html_content = loader.render_to_string('fanxiangce/confirm.html', {'user': user, 'token': token, 'confirm_url': confirm_url})
                    msg = EmailMultiAlternatives('账户邮件确认', text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                    messages.info(request, '确认邮件已发送到你的邮箱，请查收')
                    return HttpResponseRedirect(reverse('fanxiangce:login'))

    return render(request, 'fanxiangce/register.html', {'form': form})
