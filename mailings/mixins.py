from django.http import Http404


class OwnerOrManagerMixin:
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user and not self.request.user.groups.filter(name="Managers").exists():
            raise Http404("У вас нет доступа к этой рассылке.")
        return obj


class OwnerMixin:
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise Http404("У вас нет доступа к этой рассылке.")
        return obj