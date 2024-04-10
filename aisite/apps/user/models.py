from mongoengine import *

# Create your models here.


class User(Document):
    meta = {"collection": "users"}
    email = EmailField(verbose_name="Email Address", required=False)
    password = StringField(required=False)
    name = StringField(max_length=30, verbose_name="Name")
    first_name = StringField(max_length=30, verbose_name="First Name")
    last_name = StringField(max_length=30, verbose_name="Last Name")
    date_of_birth = DateTimeField(verbose_name="Date of Birth")
    biography = StringField(verbose_name="Biography")
    profile_picture = StringField(verbose_name="Profile Picture")
    solanaAddress = StringField(max_length=100, unique=True, verbose_name="Address")
    ethereumAddress = StringField(max_length=100, unique=True, verbose_name="Address")
    nonce = StringField(max_length=30, verbose_name="Nonce", required=False)
    role = StringField(max_length=20, verbose_name="Role")
    is_verified = BooleanField(default=False, verbose_name="Is Verified")
    token_balance = DecimalField(precision=10, verbose_name="Token Balance")
    created_at = DateTimeField()
    updated_at = DateTimeField()
    deleted_at = DateTimeField()


class Requester(Document):
    meta = {"collection": "requesters"}
    email = EmailField(verbose_name="Email Address", required=False)
    password = StringField(required=False)
    register_step = StringField(max_length=30, verbose_name="Register Step")
    register_flag = BooleanField(required=False)
    name = StringField(max_length=30, verbose_name="Name")
    first_name = StringField(max_length=30, verbose_name="First Name")
    last_name = StringField(max_length=30, verbose_name="Last Name")
    date_of_birth = DateTimeField(verbose_name="Date of Birth")
    biography = StringField(verbose_name="Biography")
    profile_picture = StringField(verbose_name="Profile Picture")
    solanaAddress = StringField(max_length=100, verbose_name="Address")
    ethereumAddress = StringField(max_length=100, verbose_name="Address")
    nonce = StringField(max_length=30, verbose_name="Nonce", required=False)
    role = StringField(max_length=20, verbose_name="Role")
    is_verified = BooleanField(default=False, verbose_name="Is Verified")
    token_balance = DecimalField(precision=10, verbose_name="Token Balance")
    created_at = DateTimeField()
    updated_at = DateTimeField()
    deleted_at = DateTimeField()


class Tasker(Document):
    meta = {"collection": "taskers"}
    email = EmailField(verbose_name="Email Address", required=False)
    password = StringField(required=False)
    register_step = StringField(max_length=30, verbose_name="Register Step")
    register_flag = BooleanField(required=False)
    name = StringField(max_length=30, verbose_name="Name", default="")
    avatar = StringField(verbose_name="Avatar")
    nation = StringField(max_length=30, verbose_name="Nation")
    is_dao_member = BooleanField(max_length=30, verbose_name="Is Dao Member")
    daos = ListField(StringField())
    skills = ListField(StringField())
    desired_skills = ListField(StringField())
    first_name = StringField(max_length=30, verbose_name="First Name")
    last_name = StringField(max_length=30, verbose_name="Last Name")
    date_of_birth = DateTimeField(verbose_name="Date of Birth")
    biography = StringField(verbose_name="Biography")
    profile_picture = StringField(verbose_name="Profile Picture")
    solanaAddress = StringField(max_length=100, verbose_name="Solana Address")
    ethereumAddress = StringField(max_length=100, verbose_name="Ethereum Address")
    nonce = StringField(max_length=30, verbose_name="Nonce", required=False)
    role = StringField(max_length=20, verbose_name="Role")
    is_verified = BooleanField(default=False, verbose_name="Is Verified")
    token_balance = DecimalField(precision=10, verbose_name="Token Balance")
    created_at = DateTimeField()
    updated_at = DateTimeField()
    deleted_at = DateTimeField()
