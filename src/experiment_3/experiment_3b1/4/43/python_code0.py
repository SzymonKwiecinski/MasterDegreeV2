import pulp
import json

# Data in JSON format
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Extract data from the dictionary
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

M = len(prices)  # Number of different products
N = len(available)  # Number of different raw materials

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Create decision variables
amount = pulp.LpVariable.dicts("amount", range(M), lowBound=0)

# Objective Function
profit = pulp.lpSum([(prices[j] - costs[j]) * amount[j] for j in range(M)])
problem += profit, "Total_Profit"

# Constraints for raw materials
for i in range(N):
    problem += pulp.lpSum([requirements[j][i] * amount[j] for j in range(M)]) <= available[i], f"Raw_Material_Constraint_{i}"

# Constraints for demand
for j in range(M):
    problem += amount[j] <= demands[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')