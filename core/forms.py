from django import forms

from .models import Queue


class QueueForm(forms.ModelForm):
    class Meta:
        model = Queue
        fields = ['person', 'service', 'attending', 'attended']

    def clean(self):
        cleaned_data = super().clean()
        attending = cleaned_data.get("attending")
        attended = cleaned_data.get("attended")

        if attending and attended:
            raise forms.ValidationError(
                "There can not be attending"
                " and attended at the same time"
            )

        return cleaned_data
