from flask import Blueprint, render_template, request, redirect, url_for, flash
import bleach
from .forms import RegistrationForm, RESERVED_USERNAMES
main = Blueprint('main', __name__)
ALLOWED_TAGS = ["b", "i", "u", "em", "strong", "a", "p", "ul", "ol", "li"]
ALLOWED_ATTRIBUTES = {"a": ["href", "title"]}
@main.route("/", methods=["GET"])
def home():
    return redirect(url_for("main.register"))
@main.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    ip = request.remote_addr

    if form.validate_on_submit():
        raw_bio = form.bio.data or ""
        cleaned_bio = bleach.clean(
            raw_bio,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=True
        )
        if cleaned_bio != raw_bio:
            from flask import current_app as app
            app.logger.warning(f"Sanitized bio from IP={ip} user={form.username.data}")
        from flask import current_app as app
        app.logger.info(f"Registration OK IP={ip} user={form.username.data}")
        flash("Registration successful!", "success")

        return render_template("register.html", form=form, cleaned_bio=cleaned_bio)
    elif request.method == "POST":
        from flask import current_app as app
        app.logger.warning(f"Validation failed IP={ip} errors={form.errors}")
        flash("Please fix the errors.", "error")
    return render_template("register.html", form=form, cleaned_bio=None)
