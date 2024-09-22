import pulp
import json

# Data provided in JSON format
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Number of foods and nutrients
K = len(data['price'])
M = len(data['demand'])

# Define the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Define decision variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

# Objective function: Minimize the total cost
problem += pulp.lpSum(data['price'][k] * quantity[k] for k in range(K)), "Total_Cost"

# Constraints to meet nutritional demands
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * quantity[k] for k in range(K)) >= data['demand'][m], f"Nutrient_Requirement_{m+1}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')