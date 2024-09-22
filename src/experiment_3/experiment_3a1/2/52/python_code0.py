import pulp
import json

# Data from JSON
data = {'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}

# Parameters
P = len(data['supply'])  # Number of power plants
C = len(data['demand'])   # Number of cities
supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

# Define the problem
problem = pulp.LpProblem("Electricity_Transmission_Cost_Minimization", pulp.LpMinimize)

# Decision Variables
send = pulp.LpVariable.dicts("send", (range(P), range(C)), lowBound=0)

# Objective Function
problem += pulp.lpSum(transmission_costs[p][c] * send[p][c] for p in range(P) for c in range(C))

# Supply Constraints
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= supply[p]

# Demand Constraints
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) >= demand[c]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')