from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from .models import User, Url
import qrcode
import io
import shortuuid
from . import app, db, mail, cache


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        print("Form data:", request.form)  # Debug statement
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Email and password are required.")
            return redirect(url_for("login"))

        user = User.query.filter_by(email=email.lower()).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password. Please try again.")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        print("Form data:", request.form)  # Debug statement
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not email or not username or not password or not confirm_password:
            flash("All fields are required.")
            return redirect(url_for("signup"))

        if User.query.filter_by(email=email.lower()).first():
            flash("Email already exists.")
        elif len(username) < 2:
            flash("Username must be greater than 1 character.")
        elif len(password) < 6:
            flash("Password must be at least 6 characters.")
        elif password != confirm_password:
            flash("Passwords don't match.")
        else:
            try:
                hashed_password = generate_password_hash(
                    password, method="pbkdf2:sha256"
                )
                new_user = User(
                    email=email.lower(),
                    username=username.lower(),
                    password=hashed_password,
                )
                db.session.add(new_user)
                db.session.commit()
                flash("Account created successfully! Please log in.")
                return redirect(url_for("login"))
            except Exception as e:
                flash(f"An error occurred: {e}")

    return render_template("signup.html")


def generate_qr_code(url):
    img = qrcode.make(url)
    img_io = io.BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)
    return img_io


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        long_url = request.form.get("long_url")
        custom_url = request.form.get("custom_url") or None

        if not long_url:
            flash("Long URL is required.")
            return redirect(url_for("home"))

        if custom_url:
            if Url.query.filter_by(custom_url=custom_url).first():
                flash("That custom URL already exists. Please try another one!")
                return redirect(url_for("home"))
            short_url = custom_url
        else:
            if long_url[:4] != "http":
                long_url = "http://" + long_url
            short_url = shortuuid.uuid()[:6]

        url = Url(
            long_url=long_url,
            short_url=short_url,
            custom_url=custom_url,
            user_id=current_user.id,
        )
        db.session.add(url)
        db.session.commit()
        return redirect(url_for("dashboard"))

    urls = Url.query.order_by(Url.created_at.desc()).limit(10).all()
    return render_template("index.html", urls=urls)


@app.route("/dashboard")
@login_required
@cache.cached(timeout=50)
def dashboard():
    urls = (
        Url.query.filter_by(user_id=current_user.id)
        .order_by(Url.created_at.desc())
        .all()
    )
    host = request.host_url
    return render_template("dashboard.html", urls=urls, host=host)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/<short_url>")
@cache.cached(timeout=50)
def redirect_url(short_url):
    url = Url.query.filter_by(short_url=short_url).first()
    if url:
        url.clicks += 1
        db.session.commit()
        return redirect(url.long_url)
    return "URL not found."


@app.route("/qr_code/<short_url>")
def generate_qr_code_url(short_url):
    url = Url.query.filter_by(short_url=short_url).first()
    if url:
        img_io = generate_qr_code(request.host_url + url.short_url)
        return img_io.getvalue(), 200, {"Content-Type": "image/png"}
    return "URL not found."


@app.route("/analytics/<short_url>")
@login_required
@cache.cached(timeout=50)
def url_analytics(short_url):
    url = Url.query.filter_by(short_url=short_url).first()
    if url:
        return render_template("analytics.html", url=url)
    return "URL not found."


@app.route("/history")
@login_required
@cache.cached(timeout=50)
def link_history():
    urls = (
        Url.query.filter_by(user_id=current_user.id)
        .order_by(Url.created_at.desc())
        .all()
    )
    host = request.host_url
    return render_template("history.html", urls=urls, host=host)


@app.route("/delete/<int:id>")
@login_required
def delete(id):
    url = Url.query.get_or_404(id)
    if url:
        db.session.delete(url)
        db.session.commit()
        return redirect(url_for("dashboard"))
    return "URL not found."


@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_url(id):
    url = Url.query.get_or_404(id)
    if url:
        if request.method == "POST":
            custom_url = request.form.get("custom_url")
            if custom_url:
                existing_url = Url.query.filter_by(custom_url=custom_url).first()
                if existing_url:
                    flash("That custom URL already exists. Please try another one.")
                    return redirect(url_for("edit_url", id=id))
                url.custom_url = custom_url
                url.short_url = custom_url
            db.session.commit()
            return redirect(url_for("dashboard"))
        return render_template("edit.html", url=url)
    return "URL not found."
