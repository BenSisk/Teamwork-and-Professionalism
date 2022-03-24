from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

#dataset to verify data later
MATERIALS = ["plywood", "steel"]

#array of tuples to create the materials web form dropdown list
MATERIAL_CHOICES= [
    ('plywood', 'Plywood'),
    ('steel', 'Steel'),
    ]

#array of tuples to create the timeframe web form dropdown list
TIME_CHOICES= [
    (1, '1 Month'),
    (2, '2 Months'),
    (3, '3 Months'),
    (4, '4 Months'),
    (5, '5 Months'),
    (6, '6 Months'),
    (12, '12 Months'),
    ]


class pricePredictionForm(forms.Form):
    #material dropdown box
    material = forms.CharField(label="Select Material", widget=forms.Select(choices=MATERIAL_CHOICES))
    #timeframe dropdown box
    date = forms.CharField(label="Select Timeframe", widget=forms.Select(choices=TIME_CHOICES))

    #material data cleansing function
    def clean_material_data(self):
        data = self.cleaned_data["material"]

        if (data not in MATERIALS):
            raise ValidationError(_('Invalid Material - %(material)s is not in the material list'), params={"material" : data}, code="invalid")

        return data
    
    #timeframe data cleansing function
    def clean_date_data(self):
        data = self.cleaned_data["date"]

        if (type(data) is not int):
            try:
                data = int(data)
            except:
                raise ValidationError(_('Invalid Timeframe - %(date)s is not an integer and cannot be parsed'), params={"date" : data})
            
        if (data < 0):
            raise ValidationError(_('Invalid Timeframe - %(date)s is less than 0'), params={"date" : data})
        elif (data > 12):
            raise ValidationError(_('Invalid Timeframe - %(date)s is greater than 12'), params={"date" : data})

        return data