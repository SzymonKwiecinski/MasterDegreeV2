import pulp

# Data from JSON input
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

# Extract data
supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

# Number of power plants and cities
P = len(supply)
C = len(demand)

# Initialize the linear programming problem
problem = pulp.LpProblem("Electric_Utility_Cost_Minimization", pulp.LpMinimize)

# Decision Variables: send_{p,c} is the amount of electricity sent from power plant p to city c
send_vars = [
    [pulp.LpVariable(f"send_{p}_{c}", lowBound=0) for c in range(C)]
    for p in range(P)
]

# Objective Function: Minimize total transmission costs
problem += pulp.lpSum(transmission_costs[p][c] * send_vars[p][c] for p in range(P) for c in range(C))

# Constraints
# Supply constraints: Total electricity sent from each power plant does not exceed its capacity
for p in range(P):
    problem += pulp.lpSum(send_vars[p][c] for c in range(C)) <= supply[p], f"Supply_Constraint_{p}"

# Demand constraints: Total electricity received by each city meets its demand
for c in range(C):
    problem += pulp.lpSum(send_vars[p][c] for p in range(P)) >= demand[c], f"Demand_Constraint_{c}"

# Solve the problem
problem.solve()

# Prepare the output in required format
send_output = [
    [pulp.value(send_vars[p][c]) for c in range(C)]
    for p in range(P)
]

total_cost = pulp.value(problem.objective)

output = {
    "send": send_output,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')