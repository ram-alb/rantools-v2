from http import HTTPStatus

from django.http import JsonResponse

from toa_submit.services.utils import get_site_name


def get_site_gsm_name(request):
    """Get name for 2G by sitename."""
    sitename = request.GET.get("sitename")
    if not sitename:
        return JsonResponse({'error': 'Sitename is required'}, status=HTTPStatus.BAD_REQUEST)
    try:
        site_name = get_site_name(sitename)
        return JsonResponse({'site_name': site_name}, status=HTTPStatus.OK)
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=HTTPStatus.BAD_REQUEST)
