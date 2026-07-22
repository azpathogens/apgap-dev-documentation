class DjangoModelPermissionsForGET(DjangoModelPermissions):
    """
    Workaround for DjangoModelPermissions (DRF <= 3.15.2), which maps GET to []
    (no view permissions required). DRF 3.15.0 briefly added view permission
    enforcement but reverted it in 3.15.1 for backward compatibility

    If a future DRF release enforces view permissions on GET by default,
    this class can be safely removed — it is not currently referenced elsewhere.
    """
