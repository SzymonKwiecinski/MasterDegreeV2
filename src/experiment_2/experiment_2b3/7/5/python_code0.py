import pulp

# Data input from JSON
input_data = {
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

# Unpack the data
links = [{'start': input_data['StartNode'][i], 'end': input_data['EndNode'][i],
          'U': input_data['Capacity'][i], 'C': input_data['Cost'][i]} for i in range(input_data['NumLinks'])]
data_flows = [{'source': input_data['Source'][i], 'destination': input_data['Destination'][i],
               'rate': input_data['DataRate'][i]} for i in range(input_data['NumFlowReqs'])]

# Prepare the LP problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Define variables
flow_vars = {}
for link in links:
    for flow_req in data_flows:
        # Variable for flow through link (i, j) for data from source k to destination l
        flow_vars[(link['start'], link['end'], flow_req['source'], flow_req['destination'])] = pulp.LpVariable(
            f'flow_{link["start"]}_{link["end"]}_{flow_req["source"]}_{flow_req["destination"]}', lowBound=0)

# Objective function: Minimize total cost
problem += pulp.lpSum(link['C'] * flow_vars[(link['start'], link['end'], flow_req['source'], flow_req['destination'])]
                      for link in links for flow_req in data_flows), "Total_Cost"

# Constraints
# Capacity constraints
for link in links:
    problem += pulp.lpSum(flow_vars[(link['start'], link['end'], flow_req['source'], flow_req['destination'])]
                          for flow_req in data_flows) <= link['U'], f'capacity_{link["start"]}_{link["end"]}'

# Flow conservation constraints
for flow_req in data_flows:
    nodes = set([link['start'] for link in links] + [link['end'] for link in links])
    for node in nodes:
        flow_in = pulp.lpSum(flow_vars[(j, node, flow_req['source'], flow_req['destination'])]
                             for j in [link['start'] for link in links if link['end'] == node])
        flow_out = pulp.lpSum(flow_vars[(node, j, flow_req['source'], flow_req['destination'])]
                              for j in [link['end'] for link in links if link['start'] == node])

        if node == flow_req['source']:  # Source node
            problem += flow_out - flow_in == flow_req['rate'], f'flow_conservation_source_{node}_{flow_req["source"]}_{flow_req["destination"]}'
        elif node == flow_req['destination']:  # Destination node
            problem += flow_out - flow_in == -flow_req['rate'], f'flow_conservation_dest_{node}_{flow_req["source"]}_{flow_req["destination"]}'
        else:  # Intermediate node
            problem += flow_out - flow_in == 0, f'flow_conservation_intermediate_{node}_{flow_req["source"]}_{flow_req["destination"]}'

# Solve the problem
problem.solve()

# Output formatting
optimized_paths = {'paths': [], 'total_cost': pulp.value(problem.objective)}

for flow_req in data_flows:
    for link in links:
        flow_value = pulp.value(flow_vars[(link['start'], link['end'], flow_req['source'], flow_req['destination'])])
        if flow_value > 0:
            optimized_paths['paths'].append({
                'source': flow_req['source'],
                'destination': flow_req['destination'],
                'route': [link['start'], link['end']],
                'path_flow': flow_value,
                'path_cost': flow_value * link['C']
            })

print(optimized_paths)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')