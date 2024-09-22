import pulp

# Parse the input data
data = {'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}
supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

# Number of power plants and cities
P = len(supply)
C = len(demand)

# Initialize the Linear Program with the objective to minimize
problem = pulp.LpProblem("Electricity_Transmission_Cost_Minimization", pulp.LpMinimize)

# Decision variables: electricity sent from power plant p to city c
send = pulp.LpVariable.dicts("send", ((p, c) for p in range(P) for c in range(C)), lowBound=0, cat='Continuous')

# Objective function: Minimize total transmission cost
problem += pulp.lpSum(transmission_costs[p][c] * send[p, c] for p in range(P) for c in range(C))

# Constraints
# Supply constraints: total electricity sent from a power plant should not exceed its capacity
for p in range(P):
    problem += pulp.lpSum(send[p, c] for c in range(C)) <= supply[p]

# Demand constraints: total electricity received by a city should meet its demand
for c in range(C):
    problem += pulp.lpSum(send[p, c] for p in range(P)) == demand[c]

# Solve the problem
problem.solve()

# Prepare the output
send_output = [[send[p, c].varValue for c in range(C)] for p in range(P)]
total_cost = pulp.value(problem.objective)

output = {
    "send": send_output,
    "total_cost": total_cost
}

# Print the output
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')