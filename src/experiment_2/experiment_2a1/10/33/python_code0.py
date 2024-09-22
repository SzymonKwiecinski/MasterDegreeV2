import pulp
import json

# Input data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Create the linear programming problem
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

# Create binary variables for each item
x = pulp.LpVariable.dicts("item", range(K), lowBound=0, upBound=1, cat='Binary')

# Objective function: Maximize the total value of the packed items
problem += pulp.lpSum([values[k] * x[k] for k in range(K)])

# Constraint: The total size of the packed items must not exceed the capacity
problem += pulp.lpSum([sizes[k] * x[k] for k in range(K)]) <= C

# Solve the problem
problem.solve()

# Collecting results
isincluded = [int(x[k].varValue) for k in range(K)]

# Prepare output
output = {"isincluded": isincluded}
print(json.dumps(output))

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')