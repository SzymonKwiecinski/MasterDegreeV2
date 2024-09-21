import pulp
import json

# Data from the JSON input
data = json.loads("{'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}")

# Parameters
K = len(data['profit'])  # Number of spare parts
S = len(data['capacity'])  # Number of machines
Time = data['time']       # Time taken to make spare part k on machine s
Profit = data['profit']   # Profit from making spare part k
Capacity = data['capacity']  # Capacity of machine s

# Decision Variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  # Quantity of spare part k to produce

# Define the Problem
problem = pulp.LpProblem("Optimal_Production_of_Spare_Parts", pulp.LpMaximize)

# Objective Function
problem += pulp.lpSum([Profit[k] * x[k] for k in range(K)]), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum([Time[k][s] * x[k] for k in range(K)]) <= Capacity[s], f"Machine_Capacity_{s+1}"

# Solve the Problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')