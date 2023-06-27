from utils.validations import no_cache_render


def main_panel(request):
    return no_cache_render(request, 'app_main_panel/main.html', {})
    # return render(request, 'app_main_panel/main.html', {})