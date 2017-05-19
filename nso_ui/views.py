from django.shortcuts import redirect


def default_site(request):
    return redirect('/web/')
