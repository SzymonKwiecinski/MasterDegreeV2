import pulp

# Data from the JSON format
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

# Parameters
P = len(data['supply'])  # number of suppliers
C = len(data['demand'])   # number of consumers

# Create the problem variable
problem = pulp.LpProblem("Electricity_Distribution", pulp.LpMinimize)

# Decision Variables
send = pulp.LpVariable.dicts("send", (range(P), range(C)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['transmission_costs'][p][c] * send[p][c] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

# Supply Constraints
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= data['supply'][p], f"Supply_Constraint_{p}"

# Demand Constraints
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) == data['demand'][c], f"Demand_Constraint_{c}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')