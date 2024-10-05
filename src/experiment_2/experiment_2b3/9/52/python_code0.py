import pulp

# Load data
data = {'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}

supply = data["supply"]
demand = data["demand"]
transmission_costs = data["transmission_costs"]

P = len(supply)  # Number of power plants
C = len(demand)  # Number of cities

# Create a linear programming problem
problem = pulp.LpProblem("Minimize Transmission Costs", pulp.LpMinimize)

# Decision variables
send_vars = pulp.LpVariable.dicts("send", ((p, c) for p in range(P) for c in range(C)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(send_vars[p, c] * transmission_costs[p][c] for p in range(P) for c in range(C))

# Constraints
# Supply constraints
for p in range(P):
    problem += pulp.lpSum(send_vars[p, c] for c in range(C)) <= supply[p]

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(send_vars[p, c] for p in range(P)) >= demand[c]

# Solve the problem
problem.solve()

send_results = [[pulp.value(send_vars[p, c]) for c in range(C)] for p in range(P)]
total_cost = pulp.value(problem.objective)

# Format the output
output = {
    "send": send_results,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')