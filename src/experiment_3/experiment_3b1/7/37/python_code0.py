import pulp
import json

# Data in JSON format
data = '''{
    "time": [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 
    "profit": [30, 20, 40, 25, 10], 
    "capacity": [700, 1000]
}'''

# Load data
data_dict = json.loads(data)

# Extracting values from data
time = data_dict['time']
profit = data_dict['profit']
capacity = data_dict['capacity']

# Defining the problem
K = len(profit)  # Number of different spare parts
S = len(capacity)  # Number of shops
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += (pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_{s}")

# Solve the problem
problem.solve()

# Output results
quantities = [quantity[k].varValue for k in range(K)]
print(f'Quantities: {quantities}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')