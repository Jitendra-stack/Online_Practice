from django import forms
from .models import Problem, TestCase

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'description', 'difficulty', 'tag']


class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ['input', 'output']  # 'problem' is excluded since it's set in the view

    def clean(self):
        cleaned_data = super().clean()
        input_data = cleaned_data.get('input')
        output_data = cleaned_data.get('output')

        # You can add custom validation here if needed
        if not input_data or not output_data:
            raise forms.ValidationError("Both input and output fields are required.")
        
        return cleaned_data