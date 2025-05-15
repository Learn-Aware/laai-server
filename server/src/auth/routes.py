from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, status, BackgroundTasks
from fastapi.responses import JSONResponse

from src.auth.dependencies import AccessTokenBearer, RefreshTokenBearer, RoleChecker, get_current_user
from src.db.redis import add_jti_to_blocklist

from .schemas import ParentModel, StudentModel, UserResponse, UserLoginModel
from src.utils.errors import InvalidToken, UserAlreadyExistsError
# from ..errors import UserAlreadyExists
auth_router = APIRouter()

from .service import UserService
from .utils import create_access_token, create_url_safe_token, verify_password
# from ..celery_tasks import send_email

user_service = UserService()
role_checker = RoleChecker(["admin", "student"])

REFRESH_TOKEN_EXPIRY = 2

@auth_router.post(
        "/stu/signup", 
        response_description="Add new student account",
        response_model=UserResponse,
        # response_model=StudentModel,
        status_code=status.HTTP_201_CREATED,
        response_model_by_alias=False,
    )   
async def create_student_account(
    student: StudentModel,
    bg_tasks: BackgroundTasks,
    # session: AsyncSession = Depends(get_session),
    ):
    """
    Create a new student account.
    """
    email = student.email

    # Check if the student already exists
    student_exists = await user_service.user_exists(email)
    if student_exists:
        raise UserAlreadyExistsError()
    
    new_user = await user_service.create_student(student)

    # token = create_url_safe_token({"email": email})
    
    # link = f"http://{Config.DOMAIN}/auth/verify/{token}"

    # html = f"""
    #     <html>
    #         <body>
    #             <h1>Welcome to the LAAI platform!</h1>
    #             <p>Click the link below to verify your email address:</p>
    #             <a href="{link}">Verify Email</a>
    #         </body>
    #     </html>
    # """

    # emails = [email]
    # subject = "Welcome to LAAI!"
    # send_email.delay(emails, subject, html)

    # return (new_user)
    return{
        "message": "Student account created successfully. Please check your email to verify your account.",
        "data": new_user,
    }

@auth_router.post(
        "/pnt/signup", 
        response_description="Add new parent account",
        response_model=UserResponse,
        # response_model=StudentModel,
        status_code=status.HTTP_201_CREATED,
        response_model_by_alias=False,
    )   
async def create_parent_account(
    parent: ParentModel,
    bg_tasks: BackgroundTasks,
    # session: AsyncSession = Depends(get_session),
    ):
    """
    Create a new student account.
    """
    email = parent.email

    # Check if the student already exists
    parent_exists = await user_service.user_exists(email)
    if parent_exists:
        raise UserAlreadyExistsError()
    
    new_user = await user_service.create_student(parent)

    return{
        "message": "Student account created successfully. Please check your email to verify your account.",
        "data": new_user,
    }

# @auth_router.get("/verify/{token}")
# async def verify_user_account(token: str, session: AsyncSession = Depends(get_session)):

#     token_data = decode_url_safe_token(token)

#     user_email = token_data.get("email")

#     if user_email:
#         user = await user_service.get_user_by_email(user_email, session)

#         if not user:
#             raise UserNotFound()

#         await user_service.update_user(user, {"is_verified": True}, session)

#         return JSONResponse(
#             content={"message": "Account verified successfully"},
#             status_code=status.HTTP_200_OK,
#         )

#     return JSONResponse(
#         content={"message": "Error occured during verification"},
#         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#     )


@auth_router.post("/login")
async def login_users(
    login_data: UserLoginModel, 
    # session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password
    
    user = await user_service.get_user_by_email(email)

    if user is not None:
        password_valid = verify_password(password, user.get("password"))

        if password_valid:
            access_token = create_access_token(
                user_data={
                    "email": user.get("email"),
                    "user_id": str(user.get("_id")),
                    "role": user.get("role"),
                },
            )

            refresh_token = create_access_token(
                user_data={"email": user.get("email"), "user_id": str(user.get("_id"))},
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.get("email"), "id": str(user.get("_id"))},
                }
            )

#     raise InvalidCredentials()

@auth_router.get("/me", response_model=UserResponse)
async def get_current_user(
    user=Depends(get_current_user), _: bool = Depends(role_checker)
):
#     return user
# async def get_current_user(
#     user=Depends(get_current_user), _: bool = Depends(role_checker)
# ):
    return{
        "message": "User data retrieved successfully",
        "data": user,
    }

@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise InvalidToken


@auth_router.get("/logout")
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details["jti"]

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={"message": "Logged Out Successfully"}, status_code=status.HTTP_200_OK
    )