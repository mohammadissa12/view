from django import forms
from django.contrib import admin
from .models import PlaceMixin, PlaceType, PlaceSubType


class PlaceMixinAdminForm(forms.ModelForm):
    class Meta:
        model = PlaceMixin
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get the selected place_type from the form data if available
        selected_place_type_id = self.data.get('place_type')

        # Create a default choice for the 'type' field
        default_subtype = ('', 'Select Type')

        # Get the subtypes associated with the selected place_type
        if selected_place_type_id:
            subtypes = PlaceSubType.objects.filter(place_type_id=selected_place_type_id)
        else:
            subtypes = []

        # Construct choices list, including the default option at the top
        type_choices = [default_subtype] + [(subtype.id, subtype.name) for subtype in subtypes]

        # Set the choices for the 'type' field
        self.fields['type'].choices = type_choices
        