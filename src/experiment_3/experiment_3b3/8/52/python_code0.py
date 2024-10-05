import pulp

# Data
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

# Indices
P = len(supply)
C = len(demand)

# Problem
problem = pulp.LpProblem("Electricity_Distribution", pulp.LpMinimize)

# Decision Variables
send = pulp.LpVariable.dicts("send", ((p, c) for p in range(P) for c in range(C)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(transmission_costs[p][c] * send[p, c] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

# Constraints

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(send[p, c] for p in range(P)) == demand[c], f"Demand_Constraint_City_{c}"

# Supply constraints
for p in range(P):
    problem += pulp.lpSum(send[p, c] for c in range(C)) <= supply[p], f"Supply_Constraint_Power_Plant_{p}"

# Solve the problem
problem.solve()

# Output results
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
for p in range(P):
    for c in range(C):
        print(f'Power Plant {p+1} sends {send[p,c].varValue} million kWh to City {c+1}')