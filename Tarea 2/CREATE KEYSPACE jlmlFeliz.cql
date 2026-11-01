CREATE KEYSPACE jlmlFeliz
WITH replication = {
    'class': 'NetworkTopologyStrategy',
    'datacenter1': 3
};

USE jlmlFeliz;

# tabla consulta 1
CREATE TABLE Perfil_residente (
    id_residente uuid,
    monto_pago int,
    reserva text,
    timestamp_monto timestamp,
    timestamp_reserva timestamp,
    id_comunidad uuid,
    PRIMARY KEY ((id_residente, id_comunidad), timestamp_monto, timestamp_reserva)
) WITH CLUSTERING ORDER BY (timestamp_monto DESC, timestamp_reserva DESC);

# tabla consulta 2
CREATE TABLE Accesos_IOT (
    id_sensor     uuid,
    id_residente  uuid,
    timestamp     timestamp,
    tipo_acceso   text,
    PRIMARY KEY ((id_sensor, id_residente))
);

# tabla consulta 3
CREATE TABLE Deudas_comunidad (
    id_residente  uuid,
    id_comunidad  uuid,
    deuda         decimal,
    fecha         date,
    PRIMARY KEY ((id_residente, id_comunidad))
);

# tabla consulta 4
CREATE TABLE Ingresos_residente (
    id_residente  uuid,
    timestamp     timestamp,
    id_sensor     uuid,
    tipo_acceso   text,
    PRIMARY KEY ((id_residente), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);