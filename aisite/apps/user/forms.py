from django import forms

role_choices = (("1", "Administrator"), ("2", "Normal"))

user_role_choices = (("requester", "requester"), ("tasker", "tasker"))

walletType_choices = (("solana", "solana"), ("ethereum", "ethereum"))


class UserRegisterationForm(forms.Form):
    name = forms.CharField(required=True)
    date_of_birth = forms.DateField(required=False)
    biography = forms.CharField(required=False)
    profile_picture = forms.CharField(required=False)
    wallet_address = forms.CharField(required=True)
    wallet_type = forms.CharField(required=True)
    role = forms.ChoiceField(choices=role_choices, required=True)
    is_verified = forms.BooleanField(required=False)
    token_balance = forms.IntegerField(required=False)


class UserRegisterationStep1Form(forms.Form):
    step = forms.CharField(required=True)
    wallet_address = forms.CharField(required=True)
    wallet_type = forms.CharField(required=True)
    role = forms.ChoiceField(choices=user_role_choices, required=True)


class UserRegisterationStep2Form(forms.Form):
    wallet_address = forms.CharField(required=True)
    wallet_type = forms.CharField(required=True)
    avatar = forms.CharField(required=False)
    name = forms.CharField(required=True)
    nation = forms.CharField(required=True)


class UserRegisterationStep3Form(forms.Form):
    wallet_address = forms.CharField(required=True)
    wallet_type = forms.CharField(required=True)
    is_dao_member = forms.BooleanField(required=False)
    daos = forms.JSONField(required=False)


class UserRegisterationStep4Form(forms.Form):
    wallet_address = forms.CharField(required=True)
    wallet_type = forms.CharField(required=True)
    skills = forms.JSONField(required=False)
    desired_skills = forms.JSONField(required=False)


class UserRegisterationStep5Form(forms.Form):
    wallet_address = forms.CharField(required=True)
    wallet_type = forms.CharField(required=True)
    agents = forms.JSONField(required=True)


class UserLoginForm(forms.Form):
    email = forms.EmailField(required=False)
    password = forms.CharField(required=False)
    requestNonce = forms.CharField(required=True)
    publicKey = forms.CharField(required=True)
    walletType = forms.ChoiceField(choices=walletType_choices, required=True)
    signature = forms.CharField(required=False)


class UserExistForm(forms.Form):
    walletType = forms.CharField(required=True)
    publicKey = forms.CharField(required=True)
