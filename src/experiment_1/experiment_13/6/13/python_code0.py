import pulp
import json

# Data in JSON format
data = '{"time": [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], "profit": [30, 20, 40, 25, 10], "capacity": [700, 1000]}'
data = json.loads(data)

# Parameters
K = len(data['profit'])               # Number of different spare parts
S = len(data['capacity'])             # Number of machines
Time = data['time']                   # Time taken to make spare parts
Profit = data['profit']               # Profit from each spare part
Capacity = data['capacity']           # Capacity of each machine

# Create the problem
problem = pulp.LpProblem("Optimal_Production_of_Spare_Parts", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

# Objective Function
problem += pulp.lpSum(Profit[k] * x[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(Time[k][s] * x[k] for k in range(K)) <= Capacity[s], f"Capacity_Constraint_for_Machine_{s+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')