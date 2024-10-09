from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.contrib import messages

from recommend.forms import ReviewForm
from recommend.models import Reviews
from shop.models import Item


# Create your views here.
class AddReview(View):
    success_message = f"Thank you for your feedback"

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        item = Item.objects.get(id=pk)
        star_rating = request.POST.get('rating')
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            else:
                messages.success(self.request, self.success_message)
                form.rating = star_rating
                item.total_rating += int(star_rating)
                item.num_rating += 1
                item.calculate_avg_rating()
                item.save()

            form.item = item
            form.save()
        else:
            print(form.errors)

        return redirect(item.get_absolute_url())

    def get(self, request, pk):
        return redirect('home')


def delete_review(request, item_id, review_id):
    item = Item.objects.get(id=item_id)

    if request.method == 'POST':
        review = get_object_or_404(Reviews, id=review_id, user=request.user)
        item.num_rating -= 1
        item.total_rating -= review.rating
        item.calculate_avg_rating()

        review.delete()

    return redirect(item.get_absolute_url())