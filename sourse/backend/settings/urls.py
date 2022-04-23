from django.urls import path, include
from rest_framework import routers
from settings.views.stickers import StickersListView
from settings.views.smiles import SmilesListView
from settings.views.credits import AddCreditsView
from settings.views.plan import ReplanishmentPlanView, PlanViewSet



urlpatterns = [

    path('plan/admin/list/', PlanViewSet.as_view({'get': 'list'}), name="admin-plan-get"),
    path('plan/admin/delete/bulk/', PlanViewSet.as_view({'post': 'bulkDelete'}), name="admin-plan-delete-bulk"),
    path('plan/admin/create/', PlanViewSet.as_view({'post': 'create'}), name="admin-plan-create"),
    path('plan/admin/update/<int:id>/', PlanViewSet.as_view({'put': 'update'}), name="admin-plan-update"),

    path('plan', ReplanishmentPlanView.as_view(), name="settings-plan"),
    path('add/credits', AddCreditsView.as_view(), name="settings-add-credits"),
    path('smiles', SmilesListView.as_view(), name="settings-smiles"),
    path('stickers', StickersListView.as_view(), name="settings-stickers"),

]
