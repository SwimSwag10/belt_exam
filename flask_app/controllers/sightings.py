from flask import render_template,request, redirect, flash, session
from flask_app import app
from flask_app.models.sighting import Sighting
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# CREATE

@app.route('/sighting/create', methods=['POST'])
def create_sighting():
  if 'user_id' not in session:
    return redirect('/logout')
  if not Sighting.validate_sighting(request.form):
    return redirect('/sighting/dashboard')
  data = {
    "location": request.form["location"],
    "description": request.form["description"],
    "number_of": int(request.form["number_of"]),
    "date_made": request.form["date_made"],
    "user_id": session["user_id"],
    "author_id" : request.form["author_id"],
  }
  Sighting.create_sighting(data)
  return redirect('/dashboard')


# READ

@app.route('/sighting/dashboard')
def sighting_dashboard():
  if 'user_id' not in session:
    return redirect('/logout')
  data = {
    'id' : session['user_id']
  }
  return render_template('sightings_new.html', user=User.get_by_id(data))

@app.route('/sighting/<int:id>')
def show_sighting(id):
  if 'user_id' not in session:
    return redirect('/logout')
  data = {
    "id":id
  }
  user_data = {
    "id":session['user_id']
  }
  return render_template("sightings.html", sighting=Sighting.get_one_sighting(data), user=User.get_by_id(user_data))

# UPDATE

@app.route('/sighting/update/<int:id>', methods=['POST'])
def update_sighting(id):
  if 'user_id' not in session:
      return redirect('/logout')
  if not Sighting.validate_sighting(request.form):
    return redirect('/dashboard')
  data = {
    "location": request.form["location"],
    "description": request.form["description"],
    "number_of": int(request.form["number_of"]),
    "date_made": request.form["date_made"],
    "id" : id
  }
  Sighting.update(data)
  return redirect('/dashboard')

@app.route('/sighting/update/form/<int:id>')
def sighting_update_form(id):
  if 'user_id' not in session:
    return redirect('/logout')
  data = {
    "id":id
  }
  user_data = {
    "id" : session['user_id']
  }
  return render_template("sightings_edit.html", sighting=Sighting.get_one_sighting(data), user=User.get_by_id(user_data))

# DELETE

@app.route('/sighting/delete/<int:id>')
def delete_sighting(id):
  if 'user_id' not in session:
    return redirect('/logout')
  data = {
    "id" : id
  }
  Sighting.delete(data)
  return redirect('/dashboard')