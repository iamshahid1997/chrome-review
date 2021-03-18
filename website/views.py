from flask import Blueprint, render_template, request
from flask_login import login_user, login_required, logout_user, current_user
from .logic import incorrect_reviews_df_from_doc

views = Blueprint('views', __name__)

@views.route("/", methods=["GET", "POST"])
@login_required
def home():
  if request.method == "POST":
    file = request.files["reviews_csv"]
    df = incorrect_reviews_df_from_doc(file)
    return render_template(
      "home.html", user=current_user,
      res_headers=df.columns.tolist(),
      res_data=df.values.tolist(),
      res_df=df
    )

  return render_template("home.html", user=current_user)