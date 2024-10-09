from shop.utils import menu

def get_shop_context(request):
    return {'mainmenu': menu}