from django.http import HttpResponseForbidden


class PermissionSameAuthorMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user == self.get_object().Author:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise HttpResponseForbidden("Вы не имеете доступа к этой странице.")
