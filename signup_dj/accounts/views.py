import cloudinary
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .forms import SignUpForm, LoginForm
from .models import CustomUser
from .forms import BlogForm
from .models import Blog


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("role_based_dashboard")  # Redirect after signup
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.info(request, f"You are logged in as {username}.")
                return redirect("role_based_dashboard")  # Redirect after login
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


@login_required
def role_based_dashboard_view(request):
    categories = ["Mental Health", "Heart Disease", "Covid-19", "Immunization"]
    if request.user.register_as == "Doctor":
        blogs_by_category = {
            category: Blog.objects.filter(category=category, is_published=True)
            for category in categories
        }
        return render(
            request,
            "doc_blogpage.html",
            {
                "user": request.user,
                "categories": categories,
                "blogs_by_category": blogs_by_category,
            },
        )
    else:
        return render(request, "patient_blogpage.html", {"user": request.user})


# @login_required
# def dashboard_view(request):
#     user = request.user
#     context = {
#         'user': user,
#         'house_no_name': user.house_no_name,
#         'area': user.area,
#         'landmark': user.landmark,
#         'pincode': user.pincode,
#         'city': user.city,
#         'state': user.get_state_display(),
#         'profile_image': user.profile_image,
#         'register_as': user.register_as,
#     }
#     return render(request, 'dashboard.html', context)


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")


@login_required
def delete_account_view(request):
    user = request.user
    logout(request)
    user.delete()
    messages.success(request, "Your account has been deleted.")
    return redirect("signup")


def check_username(request):
    username = request.GET.get("username", "")
    exists = CustomUser.objects.filter(username__iexact=username).exists()
    return JsonResponse({"exists": exists})


# For testing Cloudinary image URL
def debug_profile_image(request):
    user = CustomUser.objects.first()
    if user and user.profile_image:
        return HttpResponse(f"Profile Image URL: {user.profile_image.url}")
    return HttpResponse("No user or profile image found")


import cloudinary.uploader

@login_required
def add_blog_view(request):
    form = BlogForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            image = request.FILES.get('image')

            if 'publish' in request.POST:
                blog = form.save(commit=False)
                blog.created_by = request.user
                blog.is_published = True

                if image:
                    blog.image = image
                blog.save()
                messages.success(request, "Blog published successfully!")
                return redirect('role_based_dashboard')

            elif 'draft' in request.POST:
                image_url = ""
                if image:
                    # Upload to Cloudinary
                    uploaded = cloudinary.uploader.upload(image)
                    image_url = uploaded.get("secure_url")

                draft = {
                    'title': form.cleaned_data['title'],
                    'category': form.cleaned_data['category'],
                    'summary': form.cleaned_data['summary'],
                    'content': form.cleaned_data['content'],
                    'image_url': image_url,
                }

                draft_list = request.session.get('draft_blogs', [])
                draft_list.append(draft)
                request.session['draft_blogs'] = draft_list
                request.session.modified = True

                messages.info(request, "Blog saved as draft.")
                return redirect('drafts')
        else:
            messages.error(request, "Please correct the errors in the form.")

    return render(request, 'add_blog.html', {'form': form})




from cloudinary.uploader import upload as cloudinary_upload
from cloudinary.uploader import upload_resource

@login_required
def drafts_view(request):
    draft_list = request.session.get('draft_blogs', [])

    if request.method == 'POST':
        index = int(request.POST.get('index'))

        if 'publish' in request.POST:
            draft = draft_list[index]

            blog = Blog(
                title=draft['title'],
                category=draft['category'],
                summary=draft['summary'],
                content=draft['content'],
                created_by=request.user,
                is_published=True,
                image_url=draft.get('image_url', '')
            )

            # If image_url exists, re-upload it to CloudinaryField
            image_url = draft.get('image_url')
            if image_url:
                uploaded = cloudinary.uploader.upload(image_url)
                blog.image = uploaded.get('public_id')  # Set CloudinaryField from public ID

            blog.save()
            messages.success(request, "Draft published!")

        elif 'delete' in request.POST:
            messages.success(request, "Draft deleted.")

        draft_list.pop(index)
        request.session['draft_blogs'] = draft_list
        request.session.modified = True
        return redirect('drafts')

    return render(request, 'drafts.html', {'drafts': draft_list})



from django.views.decorators.http import require_GET
from django.core import serializers
from django.utils.timezone import localtime


@login_required
@require_GET
def get_blogs_by_category(request):
    category = request.GET.get("category")
    blogs = Blog.objects.filter(category=category, is_published=True).order_by(
        "-created_at"
    )

    blog_data = [
        {
            "title": blog.title,
            "summary": blog.summary,
            "content": blog.content,
            "created_at": localtime(blog.created_at).isoformat(),
            "image": blog.image.url if blog.image else "",
        }
        for blog in blogs
    ]
    return JsonResponse(blog_data, safe=False)
