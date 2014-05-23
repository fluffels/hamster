from django import forms
import datetime

class LoginForm(forms.Form):
    username = forms.CharField(required=True)#pattern="u[0-9]{8}"
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    
class AssessmentManagerForm(forms.Form):
    Assessment_Name = forms.CharField(required=True)
    Assessment_Type = forms.CharField(required=True)
    Mark_Weight = forms.CharField(required=True)   

class RenderForm(forms.Form):
    outputType = forms.CharField(required=True)# //type either csv or pdf
    assessment = forms.CharField(required=True) #// eg pracs, tests
    module = forms.CharField()#// eg COS212
    userID = forms.CharField()
    alteredTable = forms.CharField()
    dateFrom = forms.DateField(initial=datetime.date.today)
    dateTo = forms.DateField(initial=datetime.date.today)

class SessionDetailsForm(forms.Form): 
    CHOICES=[('0','Opened between'),('1','Always opened'),('2','Always closed')]
    session_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'id':'session_name'}))
    open_date = forms.DateField(initial=datetime.date.today, required=True, widget=forms.TextInput(attrs={'id':'opendate'}))
    close_date = forms.DateField(initial=datetime.date.today, required=True, widget=forms.TextInput(attrs={'id':'closedate'}))
    status = forms.ChoiceField(choices=CHOICES, required=True, widget=forms.RadioSelect(attrs={'id':'status'}))
 
class LeafAssessmentForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'id':'LAname'}))
    maxMark = forms.CharField(required=True, widget=forms.TextInput(attrs={'id':'LAmaxMark'}))