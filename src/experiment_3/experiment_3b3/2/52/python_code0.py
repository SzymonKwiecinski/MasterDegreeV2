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

# Parameters
P = len(data['supply'])  # Number of power plants
C = len(data['demand'])  # Number of cities
supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

# Problem
problem = pulp.LpProblem("Electric_Utility", pulp.LpMinimize)

# Decision Variables
send = pulp.LpVariable.dicts("send", [(p, c) for p in range(P) for c in range(C)], lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(transmission_costs[p][c] * send[(p, c)] for p in range(P) for c in range(C))

# Supply Constraints
for p in range(P):
    problem += pulp.lpSum(send[(p, c)] for c in range(C)) <= supply[p], f"Supply_Constraint_{p}"

# Demand Constraints
for c in range(C):
    problem += pulp.lpSum(send[(p, c)] for p in range(P)) >= demand[c], f"Demand_Constraint_{c}"

# Solve
problem.solve()

# Output
send_result = [[send[(p, c)].varValue for c in range(C)] for p in range(P)]
total_cost = pulp.value(problem.objective)

print("Electricity Amount Sent from Power Plants to Cities:")
for p in range(P):
    for c in range(C):
        print(f"Power Plant {p} to City {c}: {send_result[p][c]} million kWh")

print(f"Total Transmission Cost: ${total_cost}")

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')