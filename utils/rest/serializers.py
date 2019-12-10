from rest_framework import serializers as drf


class ModelSerializer(drf.ModelSerializer):
    """
    A ModelSerializer that takes an additional `excluded` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        excluded = kwargs.pop('excluded', None)

        # Instantiate the superclass normally
        super(ModelSerializer, self).__init__(*args, **kwargs)

        if excluded is not None:
            # Drop any fields that are not specified in the `fields` argument.
            excluded = set(excluded)
            for field_name in excluded:
                self.fields.pop(field_name)
