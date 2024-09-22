import pulp

# Data
data = {
    'NumLinks': 4,
    'StartNode': [1, 2, 2, 3],
    'EndNode': [2, 3, 4, 4],
    'Capacity': [50, 40, 60, 50],
    'Cost': [2, 3, 1, 1],
    'NumFlowReqs': 2,
    'Source': [1, 2],
    'Destination': [4, 3],
    'DataRate': [40, 30]
}

# Extract data
num_links = data['NumLinks']
start_node = data['StartNode']
end_node = data['EndNode']
capacity = data['Capacity']
cost = data['Cost']
num_flow_reqs = data['NumFlowReqs']
source = data['Source']
destination = data['Destination']
data_rate = data['DataRate']

# Create the problem
problem = pulp.LpProblem("MinimizeTotalCost", pulp.LpMinimize)

# Create variables
flow = {}
for i in range(num_links):
    for k in range(num_flow_reqs):
        link_id = (start_node[i], end_node[i])
        flow_req_id = (source[k], destination[k])
        flow[link_id, flow_req_id] = pulp.LpVariable(f"f_{link_id[0]}_{link_id[1]}^{flow_req_id[0]}_{flow_req_id[1]}", 
                                                     0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(cost[i] * flow[(start_node[i], end_node[i]), (source[k], destination[k])]
                      for i in range(num_links) for k in range(num_flow_reqs))

# Capacity Constraints
for i in range(num_links):
    link_id = (start_node[i], end_node[i])
    problem += pulp.lpSum(flow[link_id, (source[k], destination[k])]
                          for k in range(num_flow_reqs)) <= capacity[i], f"Capacity_{link_id[0]}_{link_id[1]}"

# Flow Conservation Constraints
nodes = set(start_node) | set(end_node)
for n in nodes:
    for k in range(num_flow_reqs):
        flow_req_id = (source[k], destination[k])
        problem += (pulp.lpSum(flow[(n, j), flow_req_id] for j in end_node if (n, j) in flow)
                    - pulp.lpSum(flow[(i, n), flow_req_id] for i in start_node if (i, n) in flow) 
                    == (data_rate[k] if n == source[k] else -data_rate[k] if n == destination[k] else 0), 
                    f"FlowConservation_{n}^{flow_req_id[0]}_{flow_req_id[1]}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')