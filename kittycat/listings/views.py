
from django.contrib.auth import login, logout
from .forms import RegisterForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CatForm, SearchForm, UserProfileForm, AdoptionRequestForm
from .models import Cat, UserProfile, AdoptionRequest
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

# View to handle custom logout functionality.
def custom_logout(request):
    if request.method == 'GET':
        logout(request)
        return redirect(reverse_lazy('home'))  # Redirect to the home page or any other page after logout
    return redirect(reverse_lazy('home'))

# View to handle custom login functionality.
class CustomLoginView(LoginView):
    template_name = 'listings/sign_in.html'
    success_url = reverse_lazy('home')  # Redirect to profile page after login

    def form_valid(self, form):
        response = super().form_valid(form)
        # Redirect to user profile page upon successful login
        return redirect('home')

# View displays available cats for adoption.
def available_cats(request):
    if request.user.is_authenticated:
        # If the user is logged in, exclude cats posted by the user (using the owner field)
        cats = Cat.objects.exclude(owner=request.user)
    else:
        # If the user is not logged in, show all cats
        cats = Cat.objects.all()
    return render(request, 'listings/available_cats.html', {'cats': cats})

# View displays cat profile
def cat_profile(request, cat_id):
    cat = Cat.objects.get(cat_id=cat_id)
    return render(request, 'listings/cat_profile.html', {'cat': cat})

# View to fill an adoption request
@login_required
def ask_for_adoption(request, cat_id):
    cat = get_object_or_404(Cat, cat_id=cat_id)  # Fetch the specific cat using the cat_id
    if request.method == 'POST':
        form = AdoptionRequestForm(request.POST)
        if form.is_valid():
            adoption_request = form.save(commit=False)
            adoption_request.cat = cat  # Associate the cat with the adoption request
            adoption_request.user = request.user  # Optionally associate the request with the logged-in user
            adoption_request.save()
            return redirect('available_cats')
    else:
        form = AdoptionRequestForm()

    return render(request, 'listings/ask_for_adoption.html', {'form': form, 'cat': cat})

# View to put a cat for adoption
@login_required
def put_cat_for_adoption(request):
    if request.method == 'POST':
        form = CatForm(request.POST, request.FILES)
        if form.is_valid():
            cat = form.save(commit=False)  # Don't save to the database yet
            cat.owner = request.user  # Assign the logged-in user as the owner
            cat.save()  # Now save the cat instance
            return redirect('my_posted_cats')  # Redirect to cat detail page
    else:
        form = CatForm()

    return render(request, 'listings/put_cat_for_adoption.html', {'form': form})

# View to edit cat profile
def edit_cat(request, cat_id):
    cat = get_object_or_404(Cat, pk=cat_id)
    if request.method == 'POST':
        form = CatForm(request.POST, request.FILES, instance=cat)
        if form.is_valid():
            form.save()
            return redirect('cat_list')
    else:
        form = CatForm(instance=cat)
    return render(request, 'listings/edit_cat.html', {'form': form})

# View to handle cat deletion
def delete_cat(request, cat_id):
    cat = get_object_or_404(Cat, pk=cat_id)
    if request.method == 'POST':
        cat.delete()
        return redirect('cat_list')
    return render(request, 'listings/delete_cat.html', {'cat': cat})

# View to display search form and handle cat search
def search(request):
    query = request.GET.get('query')
    cats = Cat.objects.filter(name__icontains=query)
    return render(request, 'listings/search_results.html', {'cats': cats, 'query': query})

# View to handle user profile
@login_required
def user_profile(request):
    cats = Cat.objects.filter(available=True)

    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'listings/profile.html', {'form': form, 'cats': cats})

# View to submit an adoption request
def submit_adoption_request(request, cat_id):
    cat = get_object_or_404(Cat, pk=cat_id)
    if request.method == 'POST':
        form = AdoptionRequestForm(request.POST)
        if form.is_valid():
            adoption_request = form.save(commit=False)
            adoption_request.user = request.user
            adoption_request.cat = cat
            adoption_request.save()

            owner_email = cat.owner.email
            requester_email = request.user.email
            send_mail(
                'New Adoption Request for Your Cat',
                f'You have received a new adoption request for {cat.name}. The requester\'s email is {requester_email}.',
                settings.DEFAULT_FROM_EMAIL,
                [owner_email],
            )

            return redirect('available_cats')
    else:
        form = AdoptionRequestForm()
    return render(request, 'listings/submit_request.html', {'form': form, 'cat': cat})

# Home page view
def home(request):
    form = SearchForm()
    return render(request, 'listings/home.html', {'search_form': form})

# View to handle user registration.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            UserProfile.objects.create(user=user)
            return redirect('profile')  # Redirect to the home page after successful registration
    else:
        form = RegisterForm()
    return render(request, 'listings/join_us.html', {'form': form})

# View handles the form submission for the 'join us' page.
def submit_join_us(request):
    # Handle submission logic or redirect as needed
    return redirect('home')

# View to handle the form submission for the sign-up process.
def submit_sign_up(request):
    return redirect('home')

# View to search for cats
def search(request):
    form = SearchForm()
    results = Cat.objects.all()  # Display all cats by default

    if request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data.get('query', '')
            castrated = form.cleaned_data.get('castrated', False)
            min_age = form.cleaned_data.get('min_age')
            max_age = form.cleaned_data.get('max_age')

            # Filter by name or breed
            if query:
                results = results.filter(
                    name__icontains=query
                ) | results.filter(breed__icontains=query)

            # Filter by castrated status
            if castrated:
                results = results.filter(castrated=True)

            # Filter by age range
            if min_age is not None:
                results = results.filter(age__gte=min_age)
            if max_age is not None:
                results = results.filter(age__lte=max_age)

    return render(request, 'listings/search.html', {'form': form, 'results': results})

# View to delete posted cats
@login_required
def delete_cat(request, cat_id):
    cat = get_object_or_404(Cat, pk=cat_id)

    # Check if the logged-in user is the owner of the cat
    if cat.owner != request.user:
        messages.error(request, "You don't have permission to delete this cat.")
        return redirect('my_posted_cats')

    if request.method == 'POST':
        cat.delete()
        messages.success(request, 'The cat has been deleted successfully.')
        return redirect('my_posted_cats')

    return render(request, 'listings/delete_cat.html', {'cat': cat})

# View to display user's posted cats
@login_required
def my_posted_cats(request):
    cats = Cat.objects.filter(owner=request.user)
    return render(request, 'listings/my_posted_cats.html', {'cats': cats})

# View renders the website's landing page
def landing_page(request):
    return render(request, 'listings/landing_page.html')

# View displays user's filled requests with status
@login_required
def my_cat_requests(request):
    # Get the logged-in user's requests
    user_requests = AdoptionRequest.objects.filter(user=request.user)
    
    return render(request, 'listings/my_cat_requests.html', {'user_requests': user_requests})

# View displays reveived cat requests
@login_required
def received_requests(request):
    # Get the logged-in user's cats
    user_cats = Cat.objects.filter(owner=request.user)
    
    # Get all adoption requests related to those cats
    received_requests = AdoptionRequest.objects.filter(cat__in=user_cats)
    
    return render(request, 'listings/received_requests.html', {'received_requests': received_requests})

# View to update request status
@login_required
def update_request_status(request, request_id):
    adoption_request = get_object_or_404(AdoptionRequest, id=request_id)

    # Ensure only the cat owner can update the status
    if adoption_request.cat.owner != request.user:
        return redirect('received_requests')

    if request.method == "POST":
        adoption_request.status = request.POST['status']
        adoption_request.save()

        # If the request is approved, remove the cat from available listings
        if adoption_request.status == 'Approved':
            adoption_request.cat.available = False
            adoption_request.cat.save()

        # If the request is declined, the cat remains available
        if adoption_request.status == 'Declined':
            adoption_request.cat.available = True
            adoption_request.cat.save()

    return redirect('received_requests')

# View to handle adoption request
def handle_adoption_request(request, request_id, action):
    adoption_request = get_object_or_404(AdoptionRequest, id=request_id)
    
    # Ensure that the logged-in user is the owner of the cat
    if adoption_request.cat.owner == request.user:
        if action == 'approve':
            # Approve the request and delete the cat
            adoption_request.status = 'Approved'
            adoption_request.save()
            send_mail(
                f'Your adoption request for {adoption_request.cat.name} (ID: {adoption_request.cat.cat_id}) was accepted!',
                f'Congratulations! Your request for {adoption_request.cat.name} has been approved. '
                f'Please contact the owner at {adoption_request.cat.owner.email} to proceed with the adoption.',
                settings.DEFAULT_FROM_EMAIL,
                [adoption_request.user.email],
                fail_silently=True,
            )
            adoption_request.cat.delete()  # Delete the cat after approval
        elif action == 'decline':
            # Decline the request, keep the cat available
            adoption_request.status = 'Declined'
            adoption_request.save()
    
    return redirect('received_requests')
