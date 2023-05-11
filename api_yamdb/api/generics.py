from rest_framework import viewsets, mixins


class CreateListDestroyGeneric(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pass
