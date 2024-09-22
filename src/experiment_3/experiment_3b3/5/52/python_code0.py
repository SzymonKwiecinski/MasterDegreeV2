import pulp

# Data
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [
        [14, 22],
        [18, 12],
        [10, 16]
    ]
}

# Number of power plants and cities
P = len(data['supply'])
C = len(data['demand'])

# Create the Linear Programming problem
problem = pulp.LpProblem("Electricity_Transmission", pulp.LpMinimize)

# Decision Variables
send = pulp.LpVariable.dicts("send", ((p, c) for p in range(P) for c in range(C)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['transmission_costs'][p][c] * send[p, c] for p in range(P) for c in range(C))

# Constraints
# Supply constraints
for p in range(P):
    problem += pulp.lpSum(send[p, c] for c in range(C)) <= data['supply'][p], f"Supply_Constraint_{p}"

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(send[p, c] for p in range(P)) >= data['demand'][c], f"Demand_Constraint_{c}"

# Non-negativity is ensured by the 'lowBound' in decision variables

# Solve the problem
problem.solve()

# Print the results
for p in range(P):
    for c in range(C):
        print(f"Electricity sent from plant {p} to city {c}: {send[p, c].varValue} million kWh")

print(f"Total Transmission Cost (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")