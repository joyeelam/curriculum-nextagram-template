from models.base_model import BaseModel
import peewee as pw
import re
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

class User(BaseModel, UserMixin):

    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.TextField(null = False)
    profile_image = pw.TextField(null = True)

    def validate(self):

        password_regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$"
        email_regex = "\S+@\S+\.\S+"
        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)

        if self.username.strip() == "":
            self.errors["Username"] = "Username is required"
        if duplicate_username:
            self.errors["Username"] = "Username already exists"

        if self.password:
            if self.password.strip() == "":
                self.errors["Password"] = "Password is required"
            else:
                check_password = re.search(password_regex, self.password)
                if check_password:
                    self.password = generate_password_hash(self.password)
                else:
                    self.errors["Password2"] = ["Password should be longer than 6 characters", "Password should have both uppercase and lowercase characters", "Password should have at least one special character"]

        if self.email.strip() == "":
            self.errors["Email"] = "Email is required"
        elif duplicate_email:
            self.errors["Email"] = "Email already exists"
        else:
            check_email = re.search(email_regex, self.email)
            if check_email:
                return self.email
            else:
                self.errors["Email"] = "Email format not valid"
