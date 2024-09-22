import pulp
import json

# Input data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Extracting the problem parameters
prices = data['price']
demands = data['demand']
nutrition = data['nutrition']

# Number of foods (K) and nutrients (M)
K = len(prices)
M = len(demands)

# Defining the Linear Programming problem
problem = pulp.LpProblem('Diet_Problem', pulp.LpMinimize)

# Defining decision variables
quantities = pulp.LpVariable.dicts('quantity', range(K), lowBound=0)

# Objective function: Minimize total cost
problem += pulp.lpSum(prices[k] * quantities[k] for k in range(K)), "Total_Cost"

# Constraints: Ensure nutritional demands are met
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * quantities[k] for k in range(K)) >= demands[m], f"Nutrient_{m+1}_Demand"

# Solve the problem
problem.solve()

# Prepare output
quantity_solution = [quantities[k].varValue for k in range(K)]
output = {"quantity": quantity_solution}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')