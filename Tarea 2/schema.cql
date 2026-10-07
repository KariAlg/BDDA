CREATE KEYSPACE actors
WITH replication = {
    'class': 'NetworkTopologyStrategy',
    'datacenter1': 3
};

USE actors;

# tabla consulta 1
CREATE TABLE identificadorActor (
    id uuid,
    nombre text,
    nacionalidad text,
    fecha_nacimiento date,
    edad int,
    patrimonio double,
    idiomas set<text>,
    PRIMARY KEY (id)
);

# tabla consulta 2
CREATE TABLE nacionalidadActores (
    nacionalidad text,
    edad int,
    id uuid,
    nombre text,
    fecha_nacimiento date,
    patrimonio double,
    idiomas set<text>,
    PRIMARY KEY (nacionalidad, edad, id)
) WITH CLUSTERING ORDER BY (edad ASC, id ASC);

# tabla consulta 3
CREATE TABLE personajesActor (
    actor_id uuid,
    rol text,
    apariciones int,
    personaje_nombre text,
    actor_nombre text,
    produccion text,
    tipo_produccion text,
    generos set<text>,
    PRIMARY KEY ((actor_id, rol), apariciones, personaje_nombre)
) WITH CLUSTERING ORDER BY (apariciones DESC, personaje_nombre ASC);