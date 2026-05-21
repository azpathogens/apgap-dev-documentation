class PathogenViewSet(viewsets.ModelViewSet):
    """CRUD for the Pathogen registry + CSV upsert and a candidates list"""

    @action(detail=False, methods=["get"], url_path="candidates")
    def candidates(self, request):
        """Pathogen metadata options that aren't in the registry yet"""


class PathogenReportabilityRuleViewSet(viewsets.ModelViewSet):
    """CRUD for conditional reportability rules attached to a Pathogen

    Filter by ``?pathogen=<id>`` to get a single pathogen's rules
    """
