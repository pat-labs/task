from src.domain.service.ServiceUser import ServiceUser


class ApplicationAudit:
    def __init__(self, service_user: ServiceUser):
        self.service_user = service_user
