from twisted.application import service


class Services:
    parent_service = service.MultiService()
    just_sock = None
    just_rest = None
    just_process = None
