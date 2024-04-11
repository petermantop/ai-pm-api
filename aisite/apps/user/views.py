from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.serializers import serialize
from django.contrib.auth.hashers import make_password, check_password
from .serializers import TaskerSerializer, RequesterSerializer

import json
import random
from bson import ObjectId

from .forms import (
    UserRegisterationStep1Form,
    UserRegisterationStep2Form,
    UserRegisterationStep3Form,
    UserRegisterationStep4Form,
    UserRegisterationStep5Form,
    UserLoginForm,
    UserExistForm,
)
from .models import User, Requester, Tasker
from utils import is_valid_solana_address, verify_signature


def convertDBDataToJson(data):
    data_dict = data.to_mongo().to_dict()
    for key, value in data_dict.items():
        if isinstance(value, ObjectId):
            data_dict[key] = str(value)
    return data_dict


# Create your views here.
def handleRegisterStep1(data):
    form = UserRegisterationStep1Form(data)
    print("register1 called")

    if form.is_valid():
        register_step = data.get("step")
        wallet_address = data.get("wallet_address")
        wallet_type = data.get("wallet_type")
        role = data.get("role", "tasker")  # ["tasker", "requester"]

        if role == "requester":
            user = Requester.objects.filter(
                **{f"{wallet_type}Address": wallet_address}
            ).first()
            Tasker.objects(**{f"{wallet_type}Address": wallet_address}).delete()
            if user is None:
                user = Requester.objects.create(
                    **{f"{wallet_type}Address": wallet_address}, register_flag=True
                )
                user.save()
            return JsonResponse(
                {
                    "message": "Registration Completed Successfully",
                    "user": convertDBDataToJson(user),
                },
                safe=False,
                status=200,
            )
        else:
            user = Tasker.objects.filter(
                **{f"{wallet_type}Address": wallet_address}
            ).first()
            Requester.objects(**{f"{wallet_type}Address": wallet_address}).delete()
            if user is None:
                user = Tasker.objects.create(
                    **{f"{wallet_type}Address": wallet_address}, register_flag=False
                )
            user.register_step = register_step
            user.save()
            return JsonResponse(
                {"message": "Step 1 Completed Successfully"}, safe=False, status=200
            )
    else:
        return JsonResponse(
            {"message": "Invalid inputs", "errors": form.errors},
            safe=False,
            status=400,
        )


def handleRegisterStep2(data):
    form = UserRegisterationStep2Form(data)
    print("register2 called")

    if form.is_valid():
        wallet_address = data.get("wallet_address")
        wallet_type = data.get("wallet_type")
        avatar = data.get("avatar")
        name = data.get("name")
        nation = data.get("nation")

        tasker = Tasker.objects(**{f"{wallet_type}Address": wallet_address}).first()
        if tasker is None:
            return JsonResponse(
                {"message": "Tasker Not Found"},
                safe=False,
                status=400,
            )
        else:
            tasker.avatar = avatar
            tasker.name = name
            tasker.nation = nation
            tasker.register_step = "2"
            tasker.save()
            return JsonResponse({"message": "Step 2 completed successfully"})
    else:
        return JsonResponse(
            {"message": "Invalid inputs", "errors": form.errors},
            safe=False,
            status=400,
        )


def handleRegisterStep3(data):
    form = UserRegisterationStep3Form(data)
    print("register3 called")

    if form.is_valid():
        wallet_address = data.get("wallet_address")
        wallet_type = data.get("wallet_type")
        is_dao_member = data.get("is_dao_member", False)
        daos = data.get("daos")

        tasker = Tasker.objects(**{f"{wallet_type}Address": wallet_address}).first()
        if tasker is None:
            return JsonResponse(
                {"message": "Tasker Not Found"},
                safe=False,
                status=400,
            )
        else:
            tasker.is_dao_member = is_dao_member
            tasker.daos = daos
            tasker.register_step = "3"
            tasker.save()
            return JsonResponse({"message": "Step 3 completed successfully"})
    else:
        return JsonResponse(
            {"message": "Invalid inputs", "errors": form.errors},
            safe=False,
            status=400,
        )


def handleRegisterStep4(data):
    form = UserRegisterationStep4Form(data)
    print("register3 called")

    if form.is_valid():
        wallet_address = data.get("wallet_address")
        wallet_type = data.get("wallet_type")
        skills = data.get("skills")
        desired_skills = data.get("desired_skills")

        tasker = Tasker.objects(**{f"{wallet_type}Address": wallet_address}).first()
        if tasker is None:
            return JsonResponse(
                {"message": "Tasker Not Found"},
                safe=False,
                status=400,
            )
        else:

            tasker.skills = skills
            tasker.desired_skills = desired_skills
            tasker.register_step = "4"
            tasker.save()
            return JsonResponse({"message": "Step 4 completed successfully"})
    else:
        return JsonResponse(
            {"message": "Invalid inputs", "errors": form.errors},
            safe=False,
            status=400,
        )


def handleRegisterStep5(data):
    form = UserRegisterationStep5Form(data)
    print("register5 called")

    if form.is_valid():
        wallet_address = data.get("wallet_address")
        wallet_type = data.get("wallet_type")
        agents = data.get("agents")

        tasker = Tasker.objects(**{f"{wallet_type}Address": wallet_address}).first()
        if tasker is None:
            return JsonResponse(
                {"message": "Tasker Not Found"},
                safe=False,
                status=400,
            )
        else:
            tasker.register_step = "5"
            tasker.register_flag = True
            tasker.agents = agents
            tasker.save()
            return JsonResponse(
                {
                    "message": "Step 5 completed successfully",
                    "user": convertDBDataToJson(tasker),
                }
            )
    else:
        return JsonResponse(
            {"message": "Invalid inputs", "errors": form.errors},
            safe=False,
            status=400,
        )


@method_decorator(csrf_exempt, name="dispatch")
class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)
        register_step = data.get("step")

        if register_step == "1":
            return handleRegisterStep1(data)
        elif register_step == "2":
            return handleRegisterStep2(data)
        elif register_step == "3":
            return handleRegisterStep3(data)
        elif register_step == "4":
            return handleRegisterStep4(data)
        elif register_step == "5":
            return handleRegisterStep5(data)


@method_decorator(csrf_exempt, name="dispatch")
class SigninView(View):
    def post(self, request):
        data = json.loads(request.body)
        form = UserLoginForm(data)

        if form.is_valid():
            publicKey = data.get("publicKey")
            requestNonce = data.get("requestNonce")
            signature = data.get("signature")
            walletType = data.get("walletType")
            registerFlag = False

            if is_valid_solana_address(publicKey) == False:
                return JsonResponse(
                    {"message": "Invalid ${walletType} wallet address provided"},
                    safe=False,
                    status=400,
                )

            # Generate a nonce (random number) between 10000 and 109998
            nonce = str(random.randint(10000, 109998))

            requester = (
                Requester.objects.filter(
                    solanaAddress=publicKey, register_flag=True
                ).first()
                or Requester.objects.filter(
                    ethereumAddress=publicKey, register_flag=True
                ).first()
            )
            tasker = (
                Tasker.objects.filter(
                    solanaAddress=publicKey, register_flag=True
                ).first()
                or Tasker.objects.filter(
                    ethereumAddress=publicKey, register_flag=True
                ).first()
            )
            print("requester")
            print(requester)
            print(tasker)
            user = requester or tasker
            if user is None:
                registerFlag = True

            if requestNonce:
                if registerFlag:
                    request.session["publicKey"] = nonce
                else:
                    user.nonce = nonce
                    user.save()

                return JsonResponse({"nonce": nonce}, safe=True, status=200)

            if registerFlag:
                nonceToVerify = request.session["publicKey"]
            else:
                nonceToVerify = user.nonce

            print("publicKey", nonceToVerify, publicKey, signature)

            verified = verify_signature(nonceToVerify, signature, publicKey, walletType)

            if verified == False:
                return JsonResponse(
                    {"message": "Invalid signature, unable to login"},
                    safe=False,
                    status=400,
                )

            print(registerFlag)
            print(requester)
            print(tasker)
            if registerFlag:
                print("public key here", publicKey)
                # user = Requester.objects.create(
                #     **{f"{walletType}Address": publicKey},
                #     register_flag=False
                # )
                # user = Tasker.objects.create(
                #     **{f"{walletType}Address": publicKey},
                #     register_flag=False
                # )
                request.session["role"] = "Guest"
                return JsonResponse(
                    {"message": "User not found"},
                    safe=True,
                    status=400,
                )
            else:
                user.nonce = nonce
                user.save()
                request.session["role"] = "requester" if requester else "tasker"

            request.session["userId"] = str(user.id)
            request.session["logged"] = True

            print("request.session")
            print(request.session["userId"])
            user_dict = convertDBDataToJson(user)
            user_dict["role"] = request.session["role"]
            return JsonResponse(
                {"message": "Logged in successfully", "user": user_dict},
                safe=True,
                status=200,
            )

        else:
            return JsonResponse(
                {"message": "Invalid inputs", "errors": form.errors},
                safe=False,
                status=400,
            )


def logout(request):
    if "logged" in request.session:
        del request.session["logged"]
        request.session.flush()  # Optional: Flush all of the session data
        return JsonResponse({"message": "You are logged out"}, safe=True, status=200)
    else:
        return JsonResponse(
            {"message": "You are already logged out"}, safe=False, status=400
        )


def GetUserByPublicKey(walletType, publicKey, isAuthenticated):
    requester = Requester.objects(
        **{f"{walletType}Address": publicKey},
    ).first()
    tasker = Tasker.objects(
        **{f"{walletType}Address": publicKey},
    ).first()

    if requester is None and tasker is None:
        return {"exist": False}

    if requester:
        return {
            "exist": True,
            "isAuthenticated": isAuthenticated,
            "user": {
                "name": requester.name,
                "role": "requester",
                "registerFlag": requester.register_flag,
                "step": requester.register_step,
            },
        }
    if tasker:
        return {
            "exist": True,
            "isAuthenticated": isAuthenticated,
            "user": {
                "name": tasker.name,
                "role": "tasker",
                "registerFlag": tasker.register_flag,
                "step": tasker.register_step,
            },
        }


@method_decorator(csrf_exempt, name="dispatch")
class UserExist(View):
    def post(self, request):
        data = json.loads(request.body)
        form = UserExistForm(data)

        if form.is_valid():
            walletType = data.get("walletType")
            publicKey = data.get("publicKey")

            return JsonResponse(
                GetUserByPublicKey(
                    walletType,
                    publicKey,
                    isAuthenticated=request.session.get("publicKey") is not None,
                ),
                status=200,
            )
        else:
            return JsonResponse({"message": "Invalid Request", "errors": form.errors})

@method_decorator(csrf_exempt, name="dispatch")
class UserByPublicKey(View):
    def get(self, request):
        walletType = request.GET.get('walletType', None)
        publicKey = request.GET.get('publicKey', None)

        requester = Requester.objects(
            **{f"{walletType}Address": publicKey},
        ).first()
        tasker = Tasker.objects(
            **{f"{walletType}Address": publicKey},
        ).first()

        if requester is None and tasker is None:
            return {"exist": False}

        if requester:
            return JsonResponse({
                "exist": True,
                "role": "requester",
                "user": convertDBDataToJson(requester)
            })
        if tasker:
            return JsonResponse({
                "exist": True,
                "role": "tasker",
                "user": convertDBDataToJson(tasker)
            })