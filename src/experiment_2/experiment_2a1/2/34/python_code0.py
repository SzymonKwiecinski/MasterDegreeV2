import pulp
import json

# Input data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Problem setup
K = len(data['price'])  # number of foods
M = len(data['demand'])  # number of nutrients

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Food_Costs", pulp.LpMinimize)

# Decision variables: quantity of each food to purchase
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

# Objective function: minimize total cost
problem += pulp.lpSum(data['price'][k] * quantity[k] for k in range(K))

# Constraints: ensure each nutrient demand is met
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * quantity[k] for k in range(K)) >= data['demand'][m]

# Solve the problem
problem.solve()

# Output results
result = {
    "quantity": [quantity[k].varValue for k in range(K)]
}

print(json.dumps(result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')