from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    """
    Доступ разрешён только пользователям из группы 'Managers'.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Manager').exists()


class IsClient(BasePermission):
    """
    Доступ разрешён только пользователям из группы 'Client'.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Client').exists()
