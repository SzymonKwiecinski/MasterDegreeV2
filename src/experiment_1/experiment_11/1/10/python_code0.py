import pulp

# Data from JSON
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Parameters
K = len(data['price'])            # Number of different types of food
M = len(data['demand'])           # Number of nutrients

Price = data['price']             # Price of food
Demand = data['demand']           # Demand for nutrients
Nutrition = data['nutrition']     # Nutrition values

# Create the optimization problem
problem = pulp.LpProblem("Food_Selection_Problem", pulp.LpMinimize)

# Decision Variables: x_k represents the units purchased from food type k
x = [pulp.LpVariable(f'x_{k}', lowBound=0) for k in range(K)]

# Objective Function: Minimize the total cost
problem += pulp.lpSum(Price[k] * x[k] for k in range(K)), "Total_Cost"

# Constraints: Nutrient requirements
for m in range(M):
    problem += pulp.lpSum(Nutrition[k][m] * x[k] for k in range(K)) >= Demand[m], f"Nutrient_Requirement_{m+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')