import pulp

# Data input
data = {'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}

# Parameters
P = len(data['supply'])  # Number of power plants
C = len(data['demand'])   # Number of cities

supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

# Define the problem
problem = pulp.LpProblem("ElectricUtilityProblem", pulp.LpMinimize)

# Decision Variables
send = pulp.LpVariable.dicts("send", ((p, c) for p in range(P) for c in range(C)), lowBound=0)

# Objective Function
problem += pulp.lpSum(transmission_costs[p][c] * send[p, c] for p in range(P) for c in range(C)), "TotalTransmissionCost"

# Supply Constraints
for p in range(P):
    problem += pulp.lpSum(send[p, c] for c in range(C)) <= supply[p], f"SupplyConstraint_P{p}"

# Demand Constraints
for c in range(C):
    problem += pulp.lpSum(send[p, c] for p in range(P)) == demand[c], f"DemandConstraint_C{c}"

# Solve the problem
problem.solve()

# Print the results
for p in range(P):
    for c in range(C):
        print(f'Amount sent from power plant {p} to city {c}: {send[p, c].varValue} million kwh')

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')