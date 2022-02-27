from django import forms

list_of_files=(("1", "ipaddress.txt"), ("2" ,"domain.txt"))
class SelectFileForm(forms.Form):
    myfile = forms.ChoiceField(choices=list_of_files)
    mytext = forms.CharField(widget=forms.Textarea())

