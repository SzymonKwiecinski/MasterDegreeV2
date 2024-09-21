import pulp
import json

# Data input
data_json = '{"time": [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], "profit": [30, 20, 40, 25, 10], "capacity": [700, 1000]}'
data = json.loads(data_json)

# Parameters
K = len(data['profit'])         # Number of different spare parts
S = len(data['capacity'])       # Number of machines
Time_ks = data['time']          # Time to produce spare parts on machines
Profit_k = data['profit']       # Profit from each spare part
Capacity_s = data['capacity']   # Capacity of each machine

# Decision Variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  # x_k >= 0

# Problem Definition
problem = pulp.LpProblem("Optimal_Production_Spare_Parts", pulp.LpMaximize)

# Objective Function
problem += pulp.lpSum(Profit_k[k] * x[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(Time_ks[k][s] * x[k] for k in range(K)) <= Capacity_s[s], f"Capacity_Constraint_{s}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')