class AgencyFilterMixin:
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if hasattr(request.user, 'agencyprofile'):
            return queryset.filter(agency=request.user.agencyprofile.agency)
        return queryset
