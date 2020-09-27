############################
# solver for android game 'Transmission'
############################
from collections import namedtuple

Node = namedtuple("Node", "id type N L charge")
Exeption_z = namedtuple("Exception", "id node1 node2")
Connection = namedtuple("Connection", 'from_node to_node')
Broadcast = namedtuple("Broadcast", 'id nodes connected_nodes')


nodes = []
exps = []
connections = []
special_node = 0
broadcasts = []
path = "Path: "


# format is like 'n' - num of nodes
# n * 'TNLC' - n entries with structure 'TNLC' where
# T - type "T - transmiter V - reciver R - retranslator B - broadcast antenna"
# N - num buffs L - least buffs to fill C- initial charge (data packets)
#'e' - num exeptions
# e * 'NM'  - exeption entries where N and M is nodes that can't connect together
#'s' - special node num for task where need save charge on this node 
#'b1NM...XYZb2NM...XYZ' broadcast antenna entry. b - num nodes affected, NM...XYZ nodes affected 
#example '7R220R110R440R440V110R211R21130603150'
def parse_state(state):
    global  nodes
    global exps
    global special_node
    global broadcasts
    b_ant = []
    n_n = int(state[0])
    print(n_n)
    for i in range(n_n):
        type_node = state[1 + i * 4]
        if type_node == 'B':
            b_ant.append(i)
        N = int(state[2 + i * 4])
        L = int(state[3 + i * 4])
        charge = int(state[4 + i * 4])
        node = Node(i, type_node, N, L, charge)
        nodes.append(node)
    print(nodes)
    n_e = int(state[n_n * 4 + 1])
    print(n_e)
    for j in range(n_e):
        node1 = int(state[n_n * 4 + j * 2 + 2])
        node2 = int(state[n_n * 4 + j * 2 + 3])
        e = Exeption_z(j, node1, node2)
        exps.append(e)

    shift = n_n * 4 + 2 * n_e + 3
    if int(state[n_n * 4 + 2 * n_e + 2]) == 1:
        special_node = nodes[int(state[n_n * 4 + 2 * n_e + 3])]
        shift += 1
        print(special_node)


    print(exps)


    nums = 0
    for id in b_ant:
        num_nodes = int(state[shift + nums])
        print(num_nodes)

        b_nodes = []
        for n in range(num_nodes):
            b_nodes.append(int(state[shift + nums + n + 1]))
        b = Broadcast(id, b_nodes, [])
        broadcasts.append(b)
        nums += num_nodes + 1
    print(broadcasts)



    return


def passed_test():
    global nodes
    global special_node
    passed = 1
    for i in nodes:
        if i.type == 'B':
            continue
        if i.L:
            passed = 0
    #if not nodes[special_node.id].charge:
    #    passed = 0
    return passed


def allowed_nodes():
    global nodes
    nds = []
    for i in nodes:
        if i.charge:
            nds.append(i)
    return nds



def connection_not_allowed(a, b):
    global exps
    if a.charge == 0 or (b.L == 0 and b.type != 'B') or a.type == 'V' or b.type == 'T' or a.type == 'B':
        return 1
    for i in exps:
        if (a.id == i.node1 and b.id == i.node2) or (b.id == i.node1 and a.id == i.node2):
            return 1
    for j in connections:
        if (a.id == j.from_node and b.id == j.to_node) or (b.id == j.from_node and a.id == j.to_node):
            return 1
    return 0


def charge_antenna_nodes(from_node_id, node_id, charge):
    global nodes
    global broadcasts

    for ant in broadcasts:
        for id in ant.connected_nodes:
            if id == from_node_id:
                break;							#need to take care of relaying shit stuff




    for ant in broadcasts:
        if ant.id == node_id:
            for id in ant.nodes:
                L = nodes[id].L
                if from_node_id == nodes[id]:
                    continue
                if L >= charge:
                    nodes[id] = nodes[id]._replace(L = L-charge)
                else:
                    nodes[id] = nodes[id]._replace(L=0)
                if nodes[id].type == 'R':
                    nodes[id] = nodes[id]._replace(charge=min(charge, L))

def affected_by_antenna(node_id, ant_id):
    global nodes
    global broadcasts

    for ant in broadcasts:
        if ant_id == ant.id:
            for i in ant.nodes:
                if node_id == i:
                    return 1
    return 0

def do_connect(a, b, not_reqursive):
    global nodes
    global connections
    global broadcasts



    if a.charge == 0 or (b.L == 0 and b.type != 'B') or a.type == 'V' or b.type == 'T' or a.type == 'B':
        return

    charges = a.charge

    if b.type != 'B':
        L = b.L
        if L >= charges:
            nodes[a.id] = nodes[a.id]._replace(charge = 0)
            nodes[b.id] = nodes[b.id]._replace(L = L-charges)
        else:
            nodes[a.id] = nodes[a.id]._replace(charge=charges-L)
            nodes[b.id] = nodes[b.id]._replace(L=0)
        if b.type == 'R':
            nodes[b.id] = nodes[b.id]._replace(charge=min(charges, L))
    else:
        nodes[a.id] = nodes[a.id]._replace(charge = 0)
        nodes[b.id] = nodes[b.id]._replace(charge=b.charge + charges)
        #nodes[b.id] = nodes[b.id]._replace(charge=min(a.N, b.charge + charges))

        charge_antenna_nodes(a.id, b.id, charges)
    connection = Connection(a.id,b.id)
    if(not_reqursive):
        connections.append(connection)
        print(f'### {connections} ###')
        for i in connections:
            do_connect(nodes[i.from_node], nodes[i.to_node], 0)
            print(f'### {nodes} ###')
    return connection

solutions = 0
moves = 0
most_big_solution = ''
big_moves = 0
most_small_solution = ''
small_moves = 100

def make_next_move():
    global path
    global nodes
    global connections
    global solutions
    global moves
    global big_moves
    global small_moves
    global most_big_solution
    global most_small_solution

    #print(path)
    #print(nodes)
    if passed_test():
        print('Test_passed')
        print(path)
        solutions = solutions + 1
        if moves > big_moves:
            big_moves = moves
            most_big_solution = path
        if moves < small_moves:
            small_moves = moves
            most_small_solution = path
        return
    an = allowed_nodes()
    if not an:
        return
    temp = nodes.copy()
    for a in an:
        saved_path1 = path
        path = path + str(a.id)
        moves = moves + 1

        temp.remove(a)
        for b in temp:
            if connection_not_allowed(a, b):
                continue
            saved_path2 = path
            path = path + "to" + str(b.id) + '\n'
            saved_nodes = nodes.copy()
            connection = do_connect(a, b, 1)
            make_next_move()  # <----------- reqursion over here
            connections.remove(connection)
            nodes = saved_nodes
            path = saved_path2

        path = saved_path1
        moves = moves - 1
    return


#parse_state('4R220R220R220R2110')  # 4 nodes R220R220R220R211 0 exps level 3-3
#parse_state('6V220V110V110R440R220T004124') # 6 nodes V220 V110 V110 R440 R220 T004 1 exps 3-5 level 3-2
#parse_state('6T004V220R220R110V220R11020435') # 6 nodes T004V220R220R110V220R110 1 exps 0-4 level 3-1
#parse_state('5R220R220R330R101R211113') # 3-6
#parse_state('7R220R110R440R440V110R211R2113060315') # 3-7 need understand how to not cross signals
#parse_state('7R220R101R211R550R220V110R22030624156') # 3-12
parse_state('7V110V110V110V110B000V110T00100501235') # hmm bugs !!!! understand game logic first then do solver idioto !
make_next_move()
print(f'{solutions} solutions found')
print(f'smallest solution is {most_small_solution}')
print(f'biggest solution is {most_big_solution}')