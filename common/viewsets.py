# Forked: https://gist.github.com/prudnikov/3a968a1ee1cf9b02730cc40bc1d3d9f2
import json
from django.db import transaction
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from typing import NamedTuple


__all__ = ['AtomicCreateModelMixin', 'AtomicUpdateModelMixin', 'AtomicDestroyModelMixin',
           'AtomicModelViewSetMixin', 'AtomicModelViewSet']


class AtomicCreateModelMixin(mixins.CreateModelMixin):
    serialize_warning: NamedTuple = None

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        result = super().perform_create(serializer=serializer)
        self.serialize_warning = serializer.warn
        return result

    def get_success_headers(self, data):
        headers = super().get_success_headers(data)
        try:
            if hasattr(self, 'serialize_warning') \
                    and self.serialize_warning is not None \
                    and len(self.serialize_warning) > 0:

                headers['Warning'] = json.dumps(
                    self.serialize_warning._asdict(),
                )
        except (TypeError, KeyError):
            return headers
        return headers


class AtomicUpdateModelMixin(mixins.UpdateModelMixin):
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class AtomicDestroyModelMixin(mixins.DestroyModelMixin):
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class AtomicModelViewSetMixin(AtomicUpdateModelMixin, AtomicCreateModelMixin, AtomicDestroyModelMixin):
    pass


class AtomicModelViewSet(AtomicCreateModelMixin,
                         mixins.RetrieveModelMixin,
                         AtomicUpdateModelMixin,
                         AtomicDestroyModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):

    serializer_classes = {}

    def get_serializer_class(self):
        if self.serializer_classes.get(self.action):
            self.serializer_class = self.serializer_classes.get(self.action)

        return super().get_serializer_class()
