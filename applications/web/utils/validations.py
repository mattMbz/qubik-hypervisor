import uuid, random, string

from django.shortcuts import render

def no_cache_render(request, template, context={}):
    response = render(request, template, context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response
#End_def


def uuid_letter_prefix():
    # Generar un carácter aleatorio entre 'a' y 'f'
    first_char = random.choice(string.ascii_lowercase[0:6])
    # Generar el resto del UUID en formato hexadecimal
    rest_of_uuid = uuid.uuid4().hex[1:]

    # Combinar el carácter aleatorio y el resto del UUID
    generated_uuid = f"{first_char}{rest_of_uuid}"

    return generated_uuid
#End_def