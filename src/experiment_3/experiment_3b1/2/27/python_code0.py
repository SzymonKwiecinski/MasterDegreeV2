import pulp
import json

# Load data from JSON format
data = json.loads('{"benefit": [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]], "communication": [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]], "cost": [[5, 14, 13], [15, 5, 9], [13, 9, 10]]}')

# Define sets
K = range(len(data['benefit']))  # Departments
L = range(len(data['cost']))      # Cities

# Create a linear programming problem
problem = pulp.LpProblem("Department_Relocation", pulp.LpMinimize)

# Define decision variables
islocated = pulp.LpVariable.dicts("islocated", (K, L), cat=pulp.LpBinary)

# Define the objective function
problem += pulp.lpSum(islocated[k][l] * (
    pulp.lpSum(data['communication'][k][j] * pulp.lpSum(data['cost'][l][m] * islocated[j][m] for m in L) 
               for j in K) - data['benefit'][k][l]
) for k in K for l in L), "Total Cost"

# Department location constraints
for k in K:
    problem += pulp.lpSum(islocated[k][l] for l in L) <= 1, f"Department_Location_Constraint_{k}"

# City capacity constraints
for l in L:
    problem += pulp.lpSum(islocated[k][l] for k in K) <= 3, f"City_Capacity_Constraint_{l}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Optionally print the results for each department and city
for k in K:
    for l in L:
        print(f'Department {k} is located in City {l}: {islocated[k][l].varValue}')