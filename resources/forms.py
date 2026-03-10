from django import forms

TYPE_CHOICES = [
    ("NOTES", "Notes"),
    ("BOOK", "Text Book"),
    ("NPTEL", "NPTEL"),
    ("PREV_PAPER", "Previous Paper"),
    ("ASSIGNMENT", "Assignment"),
    ("QUEST_PAPER", "Question Paper"),
    ("LINK", "External Link"),
    ("VIDEO", "Video/Lecture"),
]

DEPARTMENT_CHOICES = [
    ("ALL", "All Departments"),
    ("CSE", "Computer Science"),
    ("MECH", "Mechanical Engineering"),
    ("ECE", "Electronics & Communication"),
    ("EEE", "Electrical & Electronics"),
    ("CIVIL", "Civil Engineering"),
]

class ResourceForm(forms.Form):

    title = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={"placeholder": "Resource title"})
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Description"}),
        required=False
    )

    department = forms.ChoiceField(
        choices=DEPARTMENT_CHOICES,
        widget=forms.Select(attrs={"class": "w-full p-sm rounded border"})
    )

    semester = forms.IntegerField(
        min_value=1,
        max_value=8,
        widget=forms.NumberInput(attrs={"placeholder": "Semester (1-8)"})
    )

    subject = forms.CharField(
        max_length=80,
        widget=forms.TextInput(attrs={"placeholder": "Subject"})
    )

    resource_type = forms.ChoiceField(
        choices=TYPE_CHOICES
    )

    file = forms.FileField(required=False, help_text="Upload PDF or Image")

    external_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={"placeholder": "External Link (optional)"}),
        help_text="Provide a link for Videos or NPTEL resources"
    )