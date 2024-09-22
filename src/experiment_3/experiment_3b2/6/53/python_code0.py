import pulp
import json

# Given data
data = json.loads('{"NumTerminals": 3, "NumDestinations": 4, "Cost": [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]], "Demand": [65, 70, 50, 45], "Supply": [150, 100, 100]}')

# Define the problem
problem = pulp.LpProblem("SoybeanTransportation", pulp.LpMinimize)

# Define decision variables
A = [(i, j) for i in range(data['NumTerminals']) for j in range(data['NumDestinations'])]
x = pulp.LpVariable.dicts("x", A, lowBound=0)

# Objective function
problem += pulp.lpSum(data['Cost'][i][j] * x[(i, j)] for (i, j) in A), "TotalTransportationCost"

# Supply constraints
for k in range(data['NumTerminals']):
    problem += pulp.lpSum(x[(k, j)] for j in range(data['NumDestinations'])) <= data['Supply'][k], f"SupplyConstraint_{k}"

# Demand constraints
for l in range(data['NumDestinations']):
    problem += pulp.lpSum(x[(i, l)] for i in range(data['NumTerminals'])) == data['Demand'][l], f"DemandConstraint_{l}"

# Flow conservation constraints
for p in range(data['NumTerminals']):
    problem += pulp.lpSum(x[(i, p)] for i in range(data['NumTerminals'])) == pulp.lpSum(x[(p, j)] for j in range(data['NumDestinations'])), f"FlowConservation_{p}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')