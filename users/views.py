from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.urls import reverse
from .models import Client
from .forms import MyUserCreationForm, EditClientData


def edit_client(request):
    if request.user.is_authenticated:
        client_data = Client.objects.filter(username_id=request.user)
        if request.method == "GET":
            form = EditClientData(instance=client_data[0] if client_data else None)
            return render(request, "registration/edit_client.html", {"form": form})
        elif request.method == "POST":
            form = EditClientData(request.POST, instance=client_data[0] if client_data else None)
            if form.is_valid():
                if client_data:
                    if form.has_changed():
                        if client_data[0].order_set.all():
                            client_data[0].username_id = None
                            client_data[0].save()
                            form = EditClientData(request.POST)
                    else:
                        request.session['message'] = "No new data was entered."
                        return redirect('home')
                new_client = form.save()
                request.user.client = new_client
                new_client.save()
                request.session['message'] = "Address changed successfully."
                return redirect('home')
            return render(request, "registration/edit_client.html", {"form": form})
    else:
        return redirect('home')


def register(request):
    if request.method == "GET":
        return render(request, "registration/registration.html", {"form": MyUserCreationForm})
    elif request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("home"))
        return render(request, "registration/registration.html", {"form": MyUserCreationForm(request.POST)})
