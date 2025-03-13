import requests
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

from .models import RefundRequest
from .forms import RefundRequestForm


class CreateRefundRequestView(CreateView):
    model = RefundRequest
    form_class = RefundRequestForm
    template_name = 'refunds/create.html'
    success_url = reverse_lazy('refund_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        # API call for IBAN validation can be added here before saving
        return super().form_valid(form)


class RefundRequestListView(LoginRequiredMixin, ListView):
    model = RefundRequest
    template_name = 'refunds/list.html'
    context_object_name = 'refunds'

    paginate_by = 10  # Pagination setting

    def get_queryset(self):
        # Only fetch requests belonging to the authenticated user
        return RefundRequest.objects.filter(user=self.request.user)


class RefundRequestDetailView(DetailView):
    model = RefundRequest
    template_name = 'refunds/detail.html'
    context_object_name = 'refund'


class ValidateIBANView(View):
    def get(self, request, *args, **kwargs):
        iban = request.GET.get('iban')
        if not iban:
            return JsonResponse({'error': 'IBAN not provided'}, status=400)

        api_url = f'https://api.api-ninjas.com/v1/iban?iban={iban}'
        headers = {'X-Api-Key': settings.NINJAS_API_KEY}

        response = requests.get(api_url, headers=headers)
        if response.status_code == requests.codes.ok:
            data = response.json()
            return JsonResponse(data)

        return JsonResponse({
            'error': 'Unable to validate IBAN',
            'status_code': response.status_code,
            'response': response.text
        }, status=response.status_code)
