from django.shortcuts import render

def no_cache_render(request, template, context={}):
    response = render(request, template, context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response
