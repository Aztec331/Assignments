from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
# Listing here means a particular item with all its details
from . models import User,Category,Service


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        # Which means the user exists in the database
        # and if present the user is logged in  
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "gas_utility/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "gas_utility/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "gas_utility/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "gas_utility/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "gas_utility/register.html")
    
def index(request):
    context= {"beginning":"Hello aztec"}
    return render(request,"gas_utility/index.html",context)


def create_service(request):
    if request.method=="GET":
        all_Categories= Category.objects.all()
        context={"categories":all_Categories}
        return render(request,"gas_utility/create_service.html",context)
    else:
        #This is the post method

        #Get the data from the form
        category= request.POST.get('category')
        details= request.POST.get('details')
        file= request.FILES.get('file')
        user= request.user

        #get the specific category name from the form, store it in categoryName field of
        #Category model , save this data into  category_data variable and save this variable
        #as category=category_data. 
        category_data= Category.objects.get(categoryName=category)


        new_service= Service(
            category= category_data,
            details=details,
            file=file,
            user=user
        )

        new_service.save()
        # file_path= new_service.file.path

        return HttpResponseRedirect(reverse('index'))


# def create_service(request):
#     if request.method == 'POST':
#         category_name = request.POST.get('category')
#         details = request.POST.get('details')
#         file = request.FILES.get('file')

#         # Get or create the category based on the name provided
#         category, created = Category.objects.get_or_create(categoryName=category_name)

#         # Create the service instance with the category, details, and file
#         service = Service.objects.create(category=category, details=details, file=file)
        
#         # Redirect to a success page or another view
#         return HttpResponseRedirect(reverse('upload_success'))  # Assuming 'upload_success' is a valid URL name
#     else:
#         # Fetch all categories for the form select options
#         categories = Category.objects.all()
#         return render(request, 'create_service.html', {'categories': categories})

