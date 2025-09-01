from django import forms
from tasks.models import Task

class TaskForm(forms.Form):
    title=forms.CharField(max_length=250)
    description=forms.CharField(widget=forms.Textarea)
    duedate=forms.DateField(widget=forms.SelectDateWidget,label="Due Date")
    assigned_to=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

    def __init__(self,*args, **kwargs):
        # print(args,kwargs)
        employees=kwargs.pop("employees",[])
        
        super().__init__(*args,**kwargs)
        print(self.fields['assigned_to'])

class Styledformixin:
    default_class = "border border-gray-300 w-full rounded-lg p-2 focus:border-rose-300 focus:ring focus:ring-rose-200"

    def apply_styled_widget(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_class,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': self.default_class,
                    'placeholder': f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': self.default_class,
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': 'space-y-2'
                })

class TaskModelForm(Styledformixin,forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assigned_to']
        # widgets = {
        #     'title': forms.TextInput(attrs={
        #         'class': "border border-gray-300 w-full rounded-lg p-2 focus:border-rose-300 focus:ring focus:ring-rose-200",
        #         'placeholder': "Enter title"
        #     }),
        #     'description': forms.Textarea(attrs={
        #         'class': "border border-gray-300 w-full rounded-lg p-2 focus:border-rose-300 focus:ring focus:ring-rose-200",
        #         'placeholder': "Enter description"
        #     }),
        #     'due_date': forms.SelectDateWidget(attrs={
        #         'class': "border border-gray-300 rounded-lg p-2 focus:border-rose-300 focus:ring focus:ring-rose-200"
        #     }),
        #     'assigned_to': forms.CheckboxSelectMultiple(attrs={
        #         'class': "border border-gray-300 rounded p-2"
        #     }),
        # }


    def __init__(self, *args, **kwargs):
        employees = kwargs.pop('employees', None)
        super().__init__(*args, **kwargs)  
        if employees is not None:
            self.fields['assigned_to'].queryset = employees
        self.apply_styled_widget() 
