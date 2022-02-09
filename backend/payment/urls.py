from django.urls import path, include
from rest_framework import routers
router = routers.SimpleRouter()
from payment.views.frontend import PaymentFilterListView, PaymentServicesView, PaymentListView
from payment.views.admin import AdminPaymentTypeView, AdminPaymentView, AdminAgency2Woman2PaymentTypeView

urlpatterns = [
    
    path('front/filter', PaymentFilterListView.as_view(), name="payment-front-filter"),
    path('services/use', PaymentServicesView.as_view(), name="payment-services-use"),
    path('user/list', PaymentListView.as_view(), name="payment-user-list"),
]

router.register(r'admin/type', AdminPaymentTypeView)
router.register(r'admin', AdminPaymentView)
router.register('admin/agency/commission', AdminAgency2Woman2PaymentTypeView)
urlpatterns += router.urls

