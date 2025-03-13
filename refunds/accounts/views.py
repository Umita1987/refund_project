import requests
from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.views.generic.edit import CreateView
from django.contrib.auth import login

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('refund_list')  # redirect after registration

    def form_valid(self, form):
        # Create a user and immediately authorize him
        result = super().form_valid(form)
        login(self.request, self.object)
        return result


class ValidateIBANView(View):
    def get(self, request, *args, **kwargs):
        iban = request.GET.get('iban')
        if not iban:
            return JsonResponse({'error': 'IBAN not provided'}, status=400)

        # First, let's check if the result is in the cache
        cached_result = cache.get(iban)
        if cached_result is not None:
            return JsonResponse({'valid': cached_result})

        # Preparing headers and parameters for the request
        headers = {
            'X-Api-Key': settings.NINJAS_API_KEY
        }
        api_url = "https://api.api-ninjas.com/v1/ibanvalidator"

        params = {'iban': iban}

        ## Make a request to an external API
        response = requests.get(api_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            valid = data.get('valid', False)  # The API is expected to return a "valid" key

            # Cache the result for 86400 seconds (1 day)
            cache.set(iban, valid, 86400)

            return JsonResponse({'valid': valid})

        return JsonResponse({'error': 'Unable to validate IBAN'}, status=400)