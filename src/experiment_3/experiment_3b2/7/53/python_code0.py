import pulp
import json

# Data
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Sets
A = [(i, j) for i in range(data['NumTerminals']) for j in range(data['NumDestinations'])]
terminals = range(data['NumTerminals'])
destinations = range(data['NumDestinations'])

# Parameters
C = {(i, j): data['Cost'][i][j] for (i, j) in A}
supply = {k: data['Supply'][k] for k in terminals}
demand = {l: data['Demand'][l] for l in destinations}

# Decision Variables
amount = pulp.LpVariable.dicts("amount", A, lowBound=0, cat='Continuous')

# Problem Definition
problem = pulp.LpProblem("SoybeanTransportation", pulp.LpMinimize)

# Objective Function
problem += pulp.lpSum(C[i, j] * amount[i, j] for (i, j) in A)

# Constraints
for k in terminals:
    problem += pulp.lpSum(amount[k, j] for j in destinations if (k, j) in A) <= supply[k]

for l in destinations:
    problem += pulp.lpSum(amount[i, l] for i in terminals if (i, l) in A) == demand[l]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')