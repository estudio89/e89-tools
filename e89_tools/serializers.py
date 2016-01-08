from rest_framework import serializers
from rest_framework.fields import DateTimeField
from rest_framework.validators import UniqueValidator

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes additional `fields` and `exclude` arguments that
    control which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):

        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        # Drop any fields that are not required.
        fields = set(fields) if fields else set(self.fields)

        exclude = set(exclude) if exclude else set([])
        allowed = fields - exclude
        existing = set(self.fields.keys())

        # Removing excluded fields
        for field_name in existing - allowed:
            self.fields.pop(field_name)

        # Adding included fields
        for field_name in self._declared_fields.keys():
            if not field_name in existing and field_name in fields:
                self.fields[field_name] = self._declared_fields[field_name]


class CustomDateTimeField(DateTimeField):
    ''' This class fixes a bug in the rest framework's implementation of DateTimeField
        whenever the attribute in the object being serialized is already a string.'''

    def to_representation(self, value):
        if isinstance(value, str) or isinstance(value, unicode) and value:
            value = parse_datetime(value)
        return super(CustomDateTimeField, self).to_representation(value)

class DeepUniqueValidator(UniqueValidator):
    ''' This is a validator that can be used in serializer fields in order
        to ensure that a particular attribute that belongs to a foreign key is unique.

        For example, consider the following models:

        class User(models.Model):
            username = models.CharField(max_length=100, unique=True)

        class ExtendedUser(models.Model):
            user = models.ForeignKey(User)
            birthDate = models.DateField()

        If you have a ModelSerializer for the ExtendedUser model that also changes
        attributes in the User model, you may want to ensure that its username is unique.

        To achieve that, do the following:

        class ExtendedUserSerializer(models.Model):
            username = serializers.CharField(source='user.username', max_length=255, validators=[core.validators.DeepUniqueValidator(queryset=accounts.models.UserEmployee.objects.all())])
            ...

            '''

    def set_context(self, serializer_field):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # Determine the underlying model field name. This may not be the
        # same as the serializer field name if `source=<>` is set.
        self.field_name = "__".join(serializer_field.source_attrs)
        # Determine the existing instance, if this is an update operation.
        self.instance = getattr(serializer_field.parent, 'instance', None)

