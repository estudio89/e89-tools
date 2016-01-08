from django.db import models

class CachedModelMixin(object):
    ''' A mixin class that makes a model always store the old values of all of its attributes.
        Remember to call the method "_update_attrs_cache" inside the model's save method.'''

    def __init__(self, *args, **kwargs):
        self._update_attrs_cache()

    def _update_attrs_cache(self):
        ''' This method must be called inside the model's save method.'''
        # Caching current values
        self._cached = {}
        fields = [f.name for f in self._meta.get_fields() if not isinstance(f,models.fields.related.RelatedField) and not isinstance(f,models.fields.related.ForeignObjectRel)]
        for f in fields:
            self._cached[f] = getattr(self, f)

    def _get_changed_fields(self):
        changed_fields = []
        for field in self._cached.keys():
            value = self._cached[field]
            if getattr(self, field) != value:
                changed_fields.append(field)
        return changed_fields

    def _has_changed(self, fields=None):
        changed = False
        if not fields:
            fields = self._cached.keys()

        for key in fields:
            value = self._cached[key]
            if not key.startswith('_') and getattr(self, key) != value:
                return True
        return changed

    def _hidden_fields_changed(self):
        changed = False
        for key,value in self._cached.items():
            if key.startswith('_') and getattr(self, key) != value:
                return True
        return changed
