// ------------------------------------------------------------
// PARTE 1
// -------------------------------------------------
// 1. Visualización e interpretación del grafo

MATCH (e:Estudiante)-[r:PIDIO_DULCES]->(c:Casa)
RETURN e, r, c;

// -------------------------------------------------
// 2. Casa con más visitas

MATCH (c:Casa)
OPTIONAL MATCH (e:Estudiante)-[r:PIDIO_DULCES]->(c)
RETURN
    c.id AS id,
    c.direccion AS direccion,
    count(r) AS visitas
ORDER BY visitas DESC, id ASC;

// -------------------------------------------------
// 3. Estudiante con más dulces

MATCH (e:Estudiante)-[r:PIDIO_DULCES]->(:Casa)
RETURN
    e.id AS estudiante,
    count(r) AS visitas,
    sum(r.cantidad) AS total_dulces
ORDER BY total_dulces DESC, estudiante ASC;

// -------------------------------------------------
// 4. Visitas sin dulces

MATCH (e:Estudiante)-[r:PIDIO_DULCES]->(c:Casa)
WHERE r.cantidad = 0
RETURN
    e.id AS estudiante,
    c.direccion AS casa,
    r.tipo AS tipo;

// ------------------------------------------------------------
// PARTE 2
// -------------------------------------------------
// 1. Proyección del grafo

CALL gds.graph.project(
    'halloween',
    ['Estudiante', 'Casa'],
    {PIDIO_DULCES: {orientation: 'NATURAL'}}
)
YIELD graphName, nodeCount, relationshipCount
RETURN graphName, nodeCount, relationshipCount;

// -------------------------------------------------
// 2. Degree Centrality: centralidad de las casas

CALL gds.degree.stream('halloween', {
    orientation: 'REVERSE'
})
YIELD nodeId, score
WITH gds.util.asNode(nodeId) AS nodo, score
WHERE 'Casa' IN labels(nodo)
RETURN
    nodo.id AS id,
    nodo.direccion AS direccion,
    score AS visitas
ORDER BY visitas DESC, id ASC;

// -------------------------------------------------
// 3. Node Similarity: estudiantes con visitas parecidas

// 3.1
CALL gds.nodeSimilarity.stream('halloween', {
    similarityMetric: 'JACCARD',
    topK: 14,
    similarityCutoff: 0.0001
})
YIELD node1, node2, similarity
WITH
    gds.util.asNode(node1) AS e1,
    gds.util.asNode(node2) AS e2,
    similarity
WHERE
    'Estudiante' IN labels(e1)
    AND 'Estudiante' IN labels(e2)
    AND e1.id < e2.id
RETURN
    e1.id AS estudiante1,
    e2.id AS estudiante2,
    similarity
ORDER BY similarity DESC, estudiante1 ASC, estudiante2 ASC
LIMIT 5;

// 3.2 
MATCH
    (a:Estudiante {id: 'Camila'})
        -[:PIDIO_DULCES]->(c:Casa)
        <-[:PIDIO_DULCES]-
    (b:Estudiante {id: 'Tomas'})
RETURN
    a,
    c,
    b;

// ------------------------------------------------------------
// Parte 3
// -------------------------------------------------
// 1. Casas compartidas

MATCH
    (a:Estudiante {id: 'Nicolas'})
        -[r1:PIDIO_DULCES]->(c:Casa)
        <-[r2:PIDIO_DULCES]-
    (b:Estudiante {id: 'Isidora'})
RETURN
    a,
    r1,
    c,
    r2,
    b;

// -------------------------------------------------
// 2. Camino más corto

MATCH
    (a:Estudiante {id: 'Nicolas'}),
    (b:Estudiante {id: 'Isidora'})
OPTIONAL MATCH p = shortestPath(
    (a)-[:PIDIO_DULCES*1..24]-(b)
)
RETURN
    p,
    length(p) AS longitud,
    nodes(p) AS recorrido;

// ------------------------------------------------------------
// PARTE 4
// 2. Liberar la proyección

// 2.1
CALL gds.graph.drop('halloween', false)
YIELD graphName
RETURN graphName;

// 2.2
CALL gds.graph.exists('halloween')
YIELD exists
RETURN exists;
// ------------------------------------------------------------