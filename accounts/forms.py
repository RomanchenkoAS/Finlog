from django import forms


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100)
    confirmation = forms.CharField(label='Confirm password', max_length=100)

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100)

# Just in case you would like to unpack form manually:

# {{ form.non_field_errors }}
# <div class="fieldWrapper">
#     {{ form.subject.errors }}
#     <label for="{{ form.subject.id_for_label }}">Email subject:</label>
#     {{ form.subject }}
# </div>
# <div class="fieldWrapper">
#     {{ form.message.errors }}
#     <label for="{{ form.message.id_for_label }}">Your message:</label>
#     {{ form.message }}
# </div>
# <div class="fieldWrapper">
#     {{ form.sender.errors }}
#     <label for="{{ form.sender.id_for_label }}">Your email address:</label>
#     {{ form.sender }}
# </div>
# <div class="fieldWrapper">
#     {{ form.cc_myself.errors }}
#     <label for="{{ form.cc_myself.id_for_label }}">CC yourself?</label>
#     {{ form.cc_myself }}
# </div>
