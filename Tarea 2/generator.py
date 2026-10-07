import uuid
import random
from datetime import datetime
from cassandra.cluster import Cluster

# 1. Conexión al clúster de Docker (localhost)
cluster = Cluster(['127.0.0.1'])
session = cluster.connect('actors')

# 2. Lista de 20 actores (Formato: Nombre, Nacionalidad, Fecha Nac, Edad, Patrimonio)
actors_data = [
    ("Mario Castaneda", "Mexicana", "1962-06-29", 64, 1500000.0),
    ("Laura Torres", "Mexicana", "1967-08-15", 59, 900000.0),
    ("Rene Garcia", "Mexicana", "1970-03-12", 56, 1100000.0),
    ("Gerardo Reyero", "Mexicana", "1965-10-02", 61, 850000.0),
    ("Masako Nozawa", "Japonesa", "1936-10-25", 89, 3000000.0),
    ("Ryo Horikawa", "Japonesa", "1958-02-01", 68, 2000000.0),
    ("Takashi Kondo", "Japonesa", "1979-05-12", 47, 750000.0),
    ("Mamoru Miyano", "Japonesa", "1983-06-08", 43, 1800000.0),
    ("Nancy Cartwright", "Estadounidense", "1957-10-25", 68, 40000000.0),
    ("Dan Castellaneta", "Estadounidense", "1957-10-29", 68, 35000000.0),
    ("Hank Azaria", "Estadounidense", "1964-04-25", 62, 25000000.0),
    ("Tara Strong", "Estadounidense", "1973-02-12", 53, 10000000.0),
    ("Carlos Segundo", "Mexicana", "1956-09-16", 70, 950000.0),
    ("Humberto Velez", "Mexicana", "1955-03-30", 71, 1300000.0),
    ("Cristina Hernandez", "Mexicana", "1977-02-13", 49, 800000.0),
    ("Claudia Garzon", "Chilena", "1985-04-10", 41, 300000.0),
    ("Gaston Malaguti", "Chilena", "1990-11-20", 35, 250000.0),
    ("Loreto Araya", "Chilena", "1981-07-05", 45, 400000.0),
    ("Claudio Serrano", "Espanola", "1970-01-20", 56, 1200000.0),
    ("Nuria Mediavilla", "Espanola", "1967-06-03", 59, 1100000.0)
]

print("Iniciando inserción de datos desnormalizados...")

for nombre, nac, fecha_str, edad, patrimonio in actors_data:
    # Generamos un ID único por actor
    actor_id = uuid.uuid4()
    fecha_nac = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    idiomas_set = {'Espanol', 'Ingles'}

    # 1. Inserción en tabla 1: actors_by_id
    session.execute("""
        INSERT INTO identificadorActor (id, nombre, nacionalidad, fecha_nacimiento, edad, patrimonio, idiomas)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (actor_id, nombre, nac, fecha_nac, edad, patrimonio, idiomas_set))

    # 2. Inserción en tabla 2: actors_by_nationality
    session.execute("""
        INSERT INTO nacionalidadActores (nacionalidad, edad, id, nombre, fecha_nacimiento, patrimonio, idiomas)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (nac, edad, actor_id, nombre, fecha_nac, patrimonio, idiomas_set))

    # 3. Inserción en tabla 3: characters_by_actor_role
    # Creamos 2 personajes por actor (uno 'principal' y uno 'secundario')
    roles = ['principal', 'secundario']
    for i, rol in enumerate(roles):
        apariciones = (i + 1) * 20
        personaje_nom = f"Personaje {i+1} de {nombre.split()[0]}"
        
        # Asignamos 'profesional' o 'independiente' según el rol (o según tu preferencia)
        tipo_prod = "profesional" if rol == "principal" else "independiente"
        
        session.execute("""
            INSERT INTO personajesActor 
            (actor_id, rol, apariciones, personaje_nombre, actor_nombre, produccion, generos)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (actor_id, rol, apariciones, personaje_nom, nombre, tipo_prod, {'Anime', 'Animacion'}))

print("¡Proceso completado! Los 20 actores y sus personajes han sido creados correctamente.")
cluster.shutdown()