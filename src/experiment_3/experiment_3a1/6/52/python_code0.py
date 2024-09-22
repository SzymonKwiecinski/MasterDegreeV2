import pulp

# Data from the provided JSON-like structure
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

# Define the number of power plants and cities
P = len(data['supply'])
C = len(data['demand'])

# Create a linear programming problem
problem = pulp.LpProblem("ElectricUtility", pulp.LpMinimize)

# Decision variables: send[p][c] is the amount of electricity sent from power plant p to city c
send = pulp.LpVariable.dicts("send", (range(P), range(C)), lowBound=0, cat='Continuous')

# Objective function: Minimize total transmission cost
problem += pulp.lpSum(data['transmission_costs'][p][c] * send[p][c] for p in range(P) for c in range(C))

# Supply constraints for each power plant
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= data['supply'][p], f"Supply_Constraint_{p}"

# Demand constraints for each city
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) >= data['demand'][c], f"Demand_Constraint_{c}"

# Solve the problem
problem.solve()

# Output the results
for p in range(P):
    for c in range(C):
        print(f"send[{p}][{c}] = {send[p][c].varValue}")

total_cost = pulp.value(problem.objective)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')