from models.base_model import BaseModel
import peewee as pw
import re
from werkzeug.security import generate_password_hash

class User(BaseModel):

    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.TextField(null = False)

    def validate(self):

        password_regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$"
        check_password = re.search(password_regex, self.password)
        if check_password:
            self.password = generate_password_hash(self.password)
        else:
            self.errors.extend(["Password should be longer than 6 characters", "Password should have both uppercase and lowercase characters", "Password should have at least one special character"])

        email_regex = "\S+@\S+\.\S+"
        check_email = re.search(email_regex, self.email)
        if check_email:
            return self.email
        else:
            self.errors.append("Email not valid")

        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)

        if duplicate_username:
            self.errors.append('Username not unique')
        if duplicate_email:
            self.errors.append('Email not unique')
