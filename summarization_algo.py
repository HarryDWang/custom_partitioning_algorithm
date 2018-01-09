import networkx as nx

def bitwise_and(list_1,list_2):
    list_U = [0 for index in range(len(list_1))]
    for index in range(len(list_1)):
        if list_1[index] == 1 and list_2[index] == 1:
            list_U[index] = 1
    return list_U

def get_nodes(filename):
    node1 = 0
    node2 = 0

    fhandNodes = open(filename)
    for line in fhandNodes:
        node1,node2 = line.split()
        G.add_edge(node1,node2)

    return G.number_of_nodes()

def get_adj_matrix():
    for edge in G.edges:
        node1 = int(edge[0])
        node2 = int(edge[1])
        Matrix[node1-1][node2-1]=1
        Matrix[node2-1][node1-1]=1

def add_I_matrix():
    for x in range(len(Matrix)):
        Matrix[x][x] = 1

def get_score(edge):
    weight = 0
    u = edge[0]
    v = edge[1]
    td = G.degree(u)+G.degree(v)
    for x in range(G.number_of_nodes()):
        if Matrix[int(u)-1][x] == 1 and Matrix[int(v)-1][x] == 1:
            weight += 1
    return (weight,td)

def get_all_scores():
    for edge in G.edges():
        all_scores_dict_prev[edge] = get_score(edge)
        all_scores_list_prev.append(edge)

#comparator used for sorting
def comparator(edge):
        return -all_scores_dict_prev[edge][0],all_scores_dict_prev[edge][1]

#need to get rid of set data structure
def assign_communities():
    unused_nodes = set(G.nodes)
    community_assignment = '1'
    for edge in all_scores_list_prev:
        if edge[0] in unused_nodes and edge[1] in unused_nodes:
            nodes_to_community[edge[0]] = community_assignment
            nodes_to_community[edge[1]] = community_assignment
            communities[int(community_assignment)].append(edge[0])
            communities[int(community_assignment)].append(edge[1])
            unused_nodes.remove(edge[0])
            unused_nodes.remove(edge[1])
            temp = int(community_assignment)+1
            community_assignment = str(temp)

    for node in unused_nodes:
        nodes_to_community[node] = community_assignment
        communities[int(community_assignment)].append(node)
        temp = int(community_assignment) + 1
        community_assignment = str(temp)
    return int(community_assignment)

def get_current_edges():
    for edge in all_scores_list_prev:
        community_1 = nodes_to_community[edge[0]]
        community_2 = nodes_to_community[edge[1]]
        if community_1 != community_2:
            if (community_1,community_2) not in all_scores_dict_current:
                all_scores_dict_current[(community_1, community_2)] = ([0 for index in range(num_nodes)],0)
                all_scores_dict_current[(community_1,community_2)] = (bitwise_and(Matrix[int(edge[0])-1],Matrix[int(edge[1])-1]),0)
            else:
                all_scores_dict_current[(community_1, community_2)] = (bitwise_and(all_scores_dict_current[(community_1,community_2)][0],Matrix[int(edge[0])-1]),0)
                all_scores_dict_current[(community_1, community_2)] = (bitwise_and(all_scores_dict_current[(community_1,community_2)][0],Matrix[int(edge[1])-1]),0)

    for key in all_scores_dict_current:
        td = 0
        for item in communities[int(key[0])]:
            td += G.degree(item)
        for item in communities[int(key[1])]:
            td += G.degree(item)
            all_scores_dict_current[key] = (all_scores_dict_current[(community_1, community_2)][0],td)

def update_scores():
    for edge in all_scores_list_current:
        td = 0
        weight = 0
        u = edge[0]
        v = edge[1]


#begin script
G = nx.Graph()
num_nodes = get_nodes("small_sample.txt") #reads txt file and parses into networkx Graph object
Matrix = [[0 for x in range(num_nodes)] for y in range(num_nodes)] #initialize Matrix
get_adj_matrix() #populate adjacency matrix A
add_I_matrix() #compute A+I (result is matrix B)

all_scores_dict_prev = dict() #hashtable of scores from previous iteration
all_scores_list_prev = list() #list of scores from previous iteration

all_scores_dict_current = dict() #dictionary of current scores
all_scores_list_current = list() #list of current scores

get_all_scores()
all_scores_list_prev = sorted(all_scores_list_prev,key=comparator) #sort list

nodes_to_community = dict() #hashtable that has <node,community pairs>
communities = [[] for y in range(num_nodes)] #row index i hold all node ids in community i --> probably need to get rid of this

num_communities = assign_communities() #assigns communities

print("sorted edge list L1:")
for edge in all_scores_list_prev:
    print(edge)

print("mapping nodes to communities:")
for item in nodes_to_community:
    print(item,nodes_to_community[item])


#for item in communities:
#    print(item)

get_current_edges()

for key in all_scores_dict_current:
    print(key,all_scores_dict_current[key])


