from cassandra.cluster import Cluster

def actualizar_actores_y_personajes():
    cluster = Cluster(['127.0.0.1'], port=9042)
    session = cluster.connect('actors')

    print("Antes de la actualizacion")
    actores_antes = session.execute("SELECT id, nombre, edad, patrimonio FROM identificadoractor")
    for a in actores_antes:
        print(f"ID: {a.id} | {a.nombre} | Edad: {a.edad} | Patrimonio: {a.patrimonio}")

    actores = session.execute("SELECT id, nombre, nacionalidad, edad, patrimonio FROM identificadoractor")
    stmt_upd_id = session.prepare("UPDATE identificadoractor SET patrimonio = ? WHERE id = ?")
    stmt_upd_nac = session.prepare("UPDATE nacionalidadactores SET patrimonio = ? WHERE nacionalidad = ? AND edad = ? AND id = ?")
    
    stmt_ins_personaje = session.prepare("""
        INSERT INTO personajesactor (actor_id, produccion, personaje_nombre, actor_nombre, rol, apariciones)
        VALUES (?, ?, ?, ?, ?, ?)
    """)

    for actor in actores:
        actor_id = actor.id
        nombre = actor.nombre
        nacionalidad = actor.nacionalidad
        edad = actor.edad
        patrimonio_actual = actor.patrimonio


        nuevo_patrimonio = round(patrimonio_actual * 1.32, 2)
        session.execute(stmt_upd_id, [nuevo_patrimonio, actor_id])
        session.execute(stmt_upd_nac, [nuevo_patrimonio, nacionalidad, edad, actor_id])
        produccion = "Sansa Ball Race"
        personaje_nombre = "Personaje Sansa"

        if edad < 40:
            rol = "principal"
            apariciones = 3
        else:
            rol = "secundario"
            apariciones = 1

        session.execute(stmt_ins_personaje, [
            actor_id,
            produccion,
            personaje_nombre,
            nombre,
            rol,
            apariciones
        ])

    print("Despues de la actualizacion")
    actores_despues = session.execute("SELECT id, nombre, edad, patrimonio FROM identificadoractor")
    for a in actores_despues:
        print(f"ID: {a.id} | {a.nombre} | Edad: {a.edad} | Nuevo Patrimonio: {a.patrimonio}")

    print("\nParticipaciones en personajesactor:")
    participaciones = session.execute("SELECT actor_id, actor_nombre, produccion, rol, apariciones FROM personajesactor")
    for p in participaciones:
        if p.produccion == "Sansa Ball Race":
            print(f"Actor: {p.actor_nombre} | Producción: {p.produccion} | Rol: {p.rol} | Apariciones: {p.apariciones}")

    cluster.shutdown()

if __name__ == "__main__":
    actualizar_actores_y_personajes()