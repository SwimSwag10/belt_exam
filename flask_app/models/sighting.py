from urllib import request
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Sighting:
  db = 'belt_exam_schema'

  def __init__(self,data):
    self.id = data['id']
    self.location = data['location']
    self.description = data['description']
    self.number_of = data['number_of']
    self.date_made = data['date_made']
    self.user_id = data['user_id']
    self.author_id = data['author_id']
    self.author_name = user.User.get_name_by_id(data['user_id'])

    self.created_at = data['created_at']
    self.updated_at = data['updated_at']
    self.creator = None

  # CREATE

  @classmethod
  def create_sighting(cls,data):
    query = """
    INSERT INTO sightings (location, description, number_of, date_made, user_id, author_id) 
    VALUES (%(location)s,%(description)s,%(number_of)s,%(date_made)s,%(user_id)s, %(author_id)s)
    ;"""
    return connectToMySQL(cls.db).query_db(query,data)

  # READ

  @classmethod
  def get_all(cls):
    query = """SELECT * FROM sightings;"""
    result = connectToMySQL(cls.db).query_db(query)
    sightings = []
    for row in result:
      sightings.append(cls(row))
    return result

  @classmethod
  def get_one_sighting(cls, data):
    query = "SELECT * FROM sightings WHERE id = %(id)s;"
    results = connectToMySQL(cls.db).query_db(query, data)
    return cls(results[0])

  @classmethod
  def get_by_id(cls, data):
    sightings = []
    query = "SELECT * FROM sightings WHERE author_id = %(id)s;"
    results = connectToMySQL(cls.db).query_db(query, data)
    for row in results:
      sightings.append(cls(row))
    print('!!!!!!!!!!!!!!!!!!!!!!', results)
    return sightings

  # UPDATE

  @classmethod
  def update(cls, data):
    query = """
    UPDATE sightings 
    SET location=%(location)s, description=%(description)s, number_of=%(number_of)s, date_made=%(date_made)s,updated_at=NOW() 
    WHERE id = %(id)s
    ;"""
    return connectToMySQL(cls.db).query_db(query,data)

  # DELETE

  @classmethod
  def delete(cls, data):
    query = "DELETE FROM sightings WHERE id = %(id)s;"
    return connectToMySQL(cls.db).query_db(query,data)
  
  @staticmethod
  def validate_sighting( sighting ):
    is_valid = True

    if len(sighting['location']) < 3:
      flash("Location must be longer than 2 characters", 'sighting')
      is_valid = False

    if len(sighting['description']) < 3:
      flash("Description must be longer than 2 characters", 'sighting')
      is_valid = False

    if int(sighting['number_of']) < 1:
      flash("number of sasquaches must be greater than 0", 'sighting')
      is_valid = False

    return is_valid