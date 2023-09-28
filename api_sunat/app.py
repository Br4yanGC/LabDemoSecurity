import psycopg2
from flask import Flask, jsonify, request
from decouple import Config, RepositoryEnv

app = Flask(__name__)

# Carga las variables de entorno desde el archivo .env
config = Config(RepositoryEnv('./.env'))

# api_key 
api_key = config.get('API_KEY')


def require_api_key(func):
    def wrapper(*args, **kwargs):
        provided_api_key = request.headers.get('Authorization')

        # Verifica si la clave de API proporcionada coincide con la clave almacenada
        if provided_api_key == api_key:
            return func(*args, **kwargs)
        else:
            return jsonify({"error": "Acceso no autorizado"}), 401

    return wrapper

# Configura la conexión a la base de datos PostgreSQL utilizando las variables de entorno
conn = psycopg2.connect(
    dbname=config.get('DATABASE_NAME'),
    user=config.get('DATABASE_USER'),
    password=config.get('DATABASE_PASSWORD'),
    host=config.get('DATABASE_HOST')
)

@app.route('/obtener_datos/<string:dni>', methods=['GET', 'POST'])
@require_api_key
def obtener_datos_por_dni(dni):
    cursor = conn.cursor()

    # Consulta SQL para obtener los datos de la persona por DNI
    consulta = """
    SELECT p.nombre, p.dni, p.fecha_nacimiento, p.estado_civil, p.dependientes,
           i.ingresos_brutos_totales, i.otros_ingresos,
           d.gastos_educativos, d.donaciones_caritativas,
           c.credito_por_hijos,
           r.impuesto_renta_retenido, r.contribucion_seguridad_social_retenida
    FROM Personas p
    LEFT JOIN Ingresos i ON p.dni = i.dni_persona
    LEFT JOIN Deducciones d ON p.dni = d.dni_persona
    LEFT JOIN CreditosFiscales c ON p.dni = c.dni_persona
    LEFT JOIN Retenciones r ON p.dni = r.dni_persona
    WHERE p.dni = %s
    """
    cursor.execute(consulta, (dni,))

    resultado = cursor.fetchone()
    cursor.close()

    if not resultado:
        return jsonify({"error": "Persona no encontrada"}), 404

    # Construir el resultado deseado en un diccionario
    resultado_dict = {
        "persona": {
            "nombre": resultado[0],
            "identificación": resultado[1],
            "fecha_nacimiento": resultado[2].strftime('%Y-%m-%d'),
            "estado_civil": resultado[3],
            "dependientes": resultado[4]
        },
        "ingresos": {
            "salario": resultado[5],
            "otros_ingresos": resultado[6]
        },
        "deducciones": {
            "gastos_médicos": resultado[7],
            "donaciones_caritativas": resultado[8]
        },
        "creditos_fiscales": {
            "credito_por_hijos": resultado[9]
        },
        "impuestos": {
            "impuesto_sobre_la_renta": resultado[10],
            "impuesto_a_la_seguridad_social": resultado[11],
            "otros_impuestos": 0.0,  # No hay datos disponibles en la tabla para esto
            "total_impuestos": resultado[10] + resultado[11]
        }
    }

    return jsonify(resultado_dict), 200

if __name__ == '__main__':
    app.run(debug=True)
