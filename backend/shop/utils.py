menu = [
    {'title': 'About us', 'url_name': 'about'},
    {'title': 'Vacancies', 'url_name': 'vacancies'},
    {'title': 'Our contacts', 'url_name': 'contacts'},
    {'title': 'Add item', 'url_name': 'add_item'},
    {'title': 'Cart', 'url_name': 'cart:cart_detail'},
]


class DataMixin:
    paginate_by = 8
    title_page = None
    cat_selected = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if self.cat_selected is not None:
            self.extra_context['cat_selected'] = self.cat_selected

        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu

    def get_mixin_context(self, context, **kwargs):
        context['menu'] = menu
        context['cat_selected'] = None
        context.update(kwargs)
        return context