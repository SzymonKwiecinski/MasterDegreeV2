import pulp
import json

# Data input
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Number of food types and nutritional ingredients
K = len(data['price'])
M = len(data['demand'])

# Create a linear programming problem
problem = pulp.LpProblem("Nutritional_Diet", pulp.LpMinimize)

# Define decision variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum([data['price'][k] * quantity[k] for k in range(K)]), "Total_Cost"

# Constraints
for m in range(M):
    problem += pulp.lpSum([data['nutrition'][k][m] * quantity[k] for k in range(K)]) >= data['demand'][m], f"Demand_Constraint_{m+1}"

# Solve the problem
problem.solve()

# Results
quantities = [quantity[k].varValue for k in range(K)]
result = {
    "quantity": quantities
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')