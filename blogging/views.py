from django.http import Http404
from django.shortcuts import render, redirect
from django.utils import timezone
from rest_framework import viewsets, permissions
from blogging.serializers import CategorySerializer, PostSerializer
from blogging.models import Post, Category
from blogging.forms import MyPostForm


def list_view(request, *args, **kwargs):
    published = Post.objects.exclude(published_date__exact=None)
    posts = published.order_by("-published_date")
    context = {"posts": posts}

    return render(request, "blogging/list.html", context)


def detail_view(request, post_id):
    published = Post.objects.exclude(published_date__exact=None)
    try:
        post = published.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404
    context = {"post": post}
    return render(request, "blogging/detail.html", context)


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Post.objects.all().order_by("-published_date")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


def add_model(request):
    if request.method == "POST":
        try:
            form = MyPostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect("/")
        except ValueError:
            return render(request, "blogging/error-login.html")
    else:  # GET
        form = MyPostForm()
        context = {"form": form}
        return render(request, "blogging/add.html", context)
