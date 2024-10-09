from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from cart.forms import CartAddItemForm
from .forms import AddItemForm
from .models import Item, ItemImage
from .utils import DataMixin

class ShopHome(DataMixin, ListView):
    model = Item
    template_name = 'shop/index.html'
    context_object_name = 'items'
    title_page = 'Home page'
    cat_selected = 0

    def get_queryset(self):
        ordering = self.request.GET.get('ordering', 'price')
        allowed_ordering = ['price', '-price', 'avg_rating', '-avg_rating', 'time_create', '-time_create']

        if ordering not in allowed_ordering:
            ordering = 'price'

        return Item.is_selling.all().select_related('category').order_by(ordering)


class ItemCategory(DataMixin, ListView):
    template_name = 'shop/index.html'
    context_object_name = 'items'
    allow_empty = False

    def get_queryset(self):
        return Item.is_selling.filter(category__slug=self.kwargs['cat_slug']).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['items'][0].category
        return self.get_mixin_context(context, title='Category - ' + cat.name, cat_selected=cat.pk)


class ItemDetail(DataMixin, DetailView):
    model = Item
    template_name = 'shop/item.html'
    slug_url_kwarg = 'item_slug'
    context_object_name = 'item'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_item_form'] = CartAddItemForm()
        return self.get_mixin_context(context, title=context['item'].title)


class AddItem(SuccessMessageMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddItemForm
    template_name = 'shop/additem.html'
    title_page = 'Add Item'
    success_message = 'You have successfully added a product'

    def form_valid(self, form):
        item = form.save(commit=False)
        item.author = self.request.user
        item.save()

        photos = self.request.FILES.getlist('photos')
        for photo in photos:
            print(photo)
            item_image = ItemImage.objects.create(photo=photo)
            item.photos.add(item_image)
            item.save()

        return super().form_valid(form)


class UpdateItem(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = AddItemForm
    template_name = 'shop/edititem.html'
    success_url = reverse_lazy('users:profile_items')
    title_page = 'Editing Items'

    def dispatch(self, request, *args, **kwargs):
        item = self.get_object()
        if item.author != request.user:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        item = form.save(commit=False)
        item.author = self.request.user
        item.save()

        new_photos = self.request.FILES.getlist('new_photos')
        for photo in new_photos:
            item_image = ItemImage.objects.create(photo=photo)
            item.photos.add(item_image)

        delete_images = self.request.POST.getlist('delete_images')
        for image_id in delete_images:
            try:
                item_image = item.photos.get(id=image_id)
                item.photos.remove(item_image)
                item_image.photo.delete()
                item_image.delete()
            except ItemImage.DoesNotExist:
                continue

        return super().form_valid(form)


class DeleteItem(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = 'shop/confirm_delete.html'  # Шаблон для подтверждения удаления
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        item = self.get_object()
        if item.author != request.user:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class Search(DataMixin, ListView):
    template_name = 'shop/index.html'
    context_object_name = 'items'
    extra_context = {'title': "Home Page"}

    def get_queryset(self):
        print(self.request.GET.get('search'))
        return Item.objects.filter(title__iregex=self.request.GET.get('search')).order_by('title')

    def get_context_data(self, object_list=None, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search'] = f'{self.request.GET.get('search')}&'
        return context


def about(request):
    return render(request, 'shop/about.html', {'title': 'About us'})


def vacancies(request):
    return render(request, 'shop/about.html', {'title': 'Vacancies'})


def contacts(request):
    return render(request, 'shop/about.html', {'title': 'Our contacts'})


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1")
