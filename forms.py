from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import (
    DataRequired, Length, Email, EqualTo, ValidationError
)
import re
RESERVED_USERNAMES = {"admin", "root", "superuser"}
COMMON_PASSWORDS = {
    "password123", "admin", "123456", "qwerty", "letmein",
    "welcome", "iloveyou", "abc123", "monkey", "football"
}
USERNAME_RE = re.compile(r"^[A-Za-z_]{3,30}$")
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(message="Username required."),
        Length(min=3, max=30),
    ])
    email = StringField("Email", validators=[
        DataRequired(),
        Email(message="Enter a valid email."),
    ])
    password = PasswordField("Password", validators=[
        DataRequired(),
    ])
    confirm = PasswordField("Confirm Password", validators=[
        DataRequired(),
        EqualTo("password", message="Passwords must match.")
    ])
    bio = TextAreaField("Bio", validators=[
        Length(max=1000, message="Bio must be 1000 characters or less.")
    ])
    submit = SubmitField("Register")
    def validate_username(self, field):
        if not USERNAME_RE.match(field.data):
            raise ValidationError("Use only letters and underscores (3–30).")
        if field.data.lower() in RESERVED_USERNAMES:
            raise ValidationError("This username is reserved.")
    def validate_email(self, field):
        lower = field.data.lower()
        if not lower.endswith((".edu", ".ac.uk", ".org")):
            raise ValidationError("Email must end with .edu, .ac.uk, or .org")
    def validate_password(self, field):
        pwd = field.data or ""
        user = (self.username.data or "").lower()
        email_user = (self.email.data.split("@")[0]).lower() if self.email.data else ""
        if len(pwd) < 12 \
            or not re.search(r"[A-Z]", pwd) \
            or not re.search(r"[a-z]", pwd) \
            or not re.search(r"\d", pwd) \
            or not re.search(r"[^\w\s]", pwd) \
            or re.search(r"\s", pwd):
            raise ValidationError(
                "Password must be at least 12 characters & include at least 1 upper, lower, number, special and no spaces."
            )
        if user in pwd.lower():
            raise ValidationError("Password must not contain username.")
        if email_user in pwd.lower():
            raise ValidationError("Password must not contain email username.")
        if pwd.lower() in COMMON_PASSWORDS:
            raise ValidationError("Password too common.")