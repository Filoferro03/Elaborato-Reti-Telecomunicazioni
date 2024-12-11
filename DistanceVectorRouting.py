#Stampa la tabela di routing 
def print_routing_table(node, routing_table):
    print(f"Routing Table for Node {node}:")
    print("Destination\t\tCost\t\tNext Hop")
    for dest in sorted(routing_table.keys()):
        next_hop, cost = routing_table[dest]
        print(f"{dest}\t\t\t\t{cost}\t\t\t\t{next_hop}")
    print("\n")


#Aggiorna la tabella di routing del nodo sulla base delle informazioni ricevute dai suoi vicini
def update_routing_table(node, neighbors, routing_table, tables):
    updated = False
    
    # Itera sui vicini e il loro costo diretto
    for neighbor, cost_to_neighbor in neighbors.items():
        # Ottieni la tabella di routing del vicino
        neighbor_table = tables[neighbor]        
        # Itera su ciascuna destinazione conosciuta dal vicino
        for dest, (next_hop, cost_from_neighbor) in neighbor_table.items():
            # Calcola il nuovo costo passando attraverso il vicino
            new_cost = cost_to_neighbor + cost_from_neighbor
            
            # Aggiorna la tabella di routing se:
            # - La destinazione non è nella tabella
            # - Oppure il nuovo costo è migliore
            if dest not in routing_table or new_cost < routing_table[dest][1]:
                routing_table[dest] = (neighbor, new_cost)
                updated = True
    
    return updated


#Simula il protocollo distance vector routing
def simulate_distance_vector_routing(nodes, edges):
    # Controlla che ci siano nodi ed archi
    if not nodes:
        raise ValueError("La lista dei nodi non può essere vuota.")
    if not edges:
        raise ValueError("La lista degli archi non può essere vuota.")
        
    # Calcolare le iterazioni massime come il numero di nodi
    iterations = len(nodes)

    # Inizializza la rete
    neighbors = {node: {} for node in nodes}  # Vicini di ciascun nodo
    tables = {node: {node: (node, 0)} for node in nodes}  # Tabelle di routing di ciascun nodo

    for node1, node2, cost in edges:
        if node1 not in nodes or node2 not in nodes:
            raise ValueError(f"Edge ({node1}, {node2}) contains unknown nodes.")
        if cost < 0:
            raise ValueError(f"Edge ({node1}, {node2}) has a negative cost: {cost}.")
        neighbors[node1][node2] = cost
        neighbors[node2][node1] = cost

    # Simula l'algoritmo per un massimo di `iterations` iterazioni
    for _ in range(iterations):
        updated = False
        for node in nodes:
            if update_routing_table(node, neighbors[node], tables[node], tables):
                updated = True
        # Se nessuna tabella è stata aggiornata, termina prima
        if not updated:
            break

    # Stampa le tabelle di routing finali
    for node in nodes:
        print_routing_table(node, tables[node])


#Main del programma, Vengono creati nodi e archi iniziali della rete
if __name__ == "__main__":
    nodes = ["A", "B", "C", "D", "E"]
    edges = [
        ("A", "B", 2),
        ("A", "C", 5),
        ("A", "E", 4),
        ("B", "C", 1),
        ("B", "D", 3),
        ("C", "D", 1),
        ("C", "E", 6),
        ("D", "E", 3),
    ]

    try:
        simulate_distance_vector_routing(nodes, edges)
    except ValueError as e:
        print(f"Error: {e}")
