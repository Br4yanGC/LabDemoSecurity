from flask import Flask, jsonify, request, redirect, render_template, url_for, flash, session
import jwt
import datetime
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import requests
import asyncio

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisthesecret'

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://brayangc@localhost/ingsoft2'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'  # Specify the table name
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = request.args.get('token')      
    if not token:
      return jsonify({'message': 'Token is missing'}), 403
    try:
      data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    except:
      ##return jsonify({'message': 'Token is invalid'}), 403
      return render_template('login.html')
    return f(*args, **kwargs)
  return decorated

@app.route('/')
def unprotected():
  return render_template('index.html')

@app.route('/protected')
@token_required
def protected():
  return render_template('protected.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Query the user from the database
        user = User.query.filter_by(username=username, password=password).first()

        if user:
            token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)}, app.config['SECRET_KEY'])
            session['token'] = token
            return redirect(f'/protected?token={token}')
        else:
            flash('Invalid credentials. Please try again.', 'danger')  # You can use flash to display error messages
            return render_template('login.html')

    return render_template('login.html')

async def fetch_data_from_api(api_url, headers):
    response = requests.get(api_url, headers=headers)
    return response.json()

@app.route('/get-data', methods=['GET'])
@token_required
def get_data():
    dni = request.args.get('dni')

    if not dni:
        return render_template('error.html', error_message="DNI is missing.")

    # Define the headers for the API request
    headers = {'Authorization': '99a5453529982e2582b42b2e65884909ca4efe018ff39015d4c45e54ccf81057'}

    # Make the API request
    api_url = f'https://6ba6-204-199-168-25.ngrok-free.app/obtener_datos/{dni}'
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        data["creditos_fiscales"]["credito_por_hijos"] = float(data["creditos_fiscales"]["credito_por_hijos"])
        data["deducciones"]["donaciones_caritativas"] = float(data["deducciones"]["donaciones_caritativas"])
        data["deducciones"]["gastos_médicos"] = float(data["deducciones"]["gastos_médicos"])
        data["impuestos"]["impuesto_a_la_seguridad_social"] = float(data["impuestos"]["impuesto_a_la_seguridad_social"])
        data["impuestos"]["impuesto_sobre_la_renta"] = float(data["impuestos"]["impuesto_sobre_la_renta"])
        data["impuestos"]["otros_impuestos"] = float(data["impuestos"]["otros_impuestos"])
        data["impuestos"]["total_impuestos"] = float(data["impuestos"]["total_impuestos"])
        data["ingresos"]["otros_ingresos"]["alquileres"] = float(data["ingresos"]["otros_ingresos"]["alquileres"])
        data["ingresos"]["otros_ingresos"]["intereses_bancarios"] = float(data["ingresos"]["otros_ingresos"]["intereses_bancarios"])
        data["ingresos"]["salario"] = float(data["ingresos"]["salario"])
        data["persona"]["dependientes"] = int(data["persona"]["dependientes"])

        return render_template('data.html', data=data)
    else:
        return render_template('error.html', error_message="Failed to fetch data from the API.")


if __name__ == '__main__':
  app.run(debug=True)
