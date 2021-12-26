class BasePermission(object):
    def __init__(self):
        self.has_permission()

    def has_permission(self) -> bool:
        # Base class has_permission() will always return True
        return True
