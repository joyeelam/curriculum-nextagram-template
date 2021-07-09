from models.base_model import BaseModel
import peewee as pw
import re
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

class User(BaseModel, UserMixin):

    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.TextField(null = False)
    profile_image = pw.TextField(default="https://flask-nextagram-2021.s3.ap-southeast-1.amazonaws.com/default_avatar.png")
    private_account = pw.BooleanField(default=False)

    def validate(self):

        modified_fields = self.dirty_fields
        # print(modified_fields)

        if "username" in [field.name for field in modified_fields]:
            duplicate_username = User.get_or_none(User.username == self.username)
            if self.username.strip() == "":
                self.errors["Username"] = "Username is required"
            if duplicate_username and duplicate_username.id != self.id:
                self.errors["Username"] = "Username already exists"

        if "email" in [field.name for field in modified_fields]:
            duplicate_email = User.get_or_none(User.email == self.email)
            if self.email.strip() == "":
                self.errors["Email"] = "Email is required"
            elif duplicate_email and duplicate_email.id != self.id:
                self.errors["Email"] = "Email already exists"
            else:
                email_regex = "\S+@\S+\.\S+"
                check_email = re.search(email_regex, self.email)
                if not check_email:
                    self.errors["Email"] = "Email format not valid"

        if "password" in [field.name for field in modified_fields]:
            if self.password.strip() == "":
                self.errors["Password"] = "Password is required"
            else:
                password_regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$"
                check_password = re.search(password_regex, self.password)
                if check_password:
                    self.password = generate_password_hash(self.password)
                else:
                    self.errors["Password2"] = ["Password should be longer than 6 characters", "Password should have both uppercase and lowercase characters", "Password should have at least one special character"]
