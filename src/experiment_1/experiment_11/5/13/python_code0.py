import pulp
import json

# Data provided in JSON format
data = json.loads('{"time": [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], "profit": [30, 20, 40, 25, 10], "capacity": [700, 1000]}')

# Parameters
K = len(data['profit'])  # Number of different spare parts
S = len(data['capacity'])  # Number of machines
time_ks = data['time']  # Time taken to make spare parts on machines
profit_k = data['profit']  # Profits from making spare parts
capacity_s = data['capacity']  # Capacities of machines

# Create the LP problem
problem = pulp.LpProblem("Optimal_Production_of_Spare_Parts", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(profit_k[k] * x[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(time_ks[k][s] * x[k] for k in range(K)) <= capacity_s[s], f"Machine_Capacity_{s}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')