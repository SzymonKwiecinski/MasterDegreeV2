import pulp
import json

# Data from the provided JSON
data = json.loads("{'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}")

# Parameters
K = len(data['price'])  # Number of different types of food
M = len(data['demand'])  # Number of nutrients

Price = data['price']  # Price of food
Demand = data['demand']  # Demand for nutrients
Nutrition = data['nutrition']  # Nutritional values

# Decision Variables
x = pulp.LpVariable.dicts("Food", range(K), lowBound=0)  # Number of units purchased from each food type

# Define the problem
problem = pulp.LpProblem("Food_Selection_Problem", pulp.LpMinimize)

# Objective Function: Minimize total cost
problem += pulp.lpSum(Price[k] * x[k] for k in range(K)), "Total_Cost"

# Constraints: Nutrient requirements
for m in range(M):
    problem += pulp.lpSum(Nutrition[k][m] * x[k] for k in range(K)) >= Demand[m], f"Nutrient_Requirement_{m}"

# Solve the problem
problem.solve()

# Display the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')