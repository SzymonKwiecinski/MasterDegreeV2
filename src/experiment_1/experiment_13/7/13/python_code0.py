import pulp

# Data from the provided JSON format
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Parameters
K = len(data['profit'])  # Number of spare parts
S = len(data['capacity'])  # Number of machines
Time = data['time']  # Time taken to make spare parts
Profit = data['profit']  # Profit from producing spare parts
Capacity = data['capacity']  # Capacity of the machines

# Create the problem
problem = pulp.LpProblem("Optimal_Production_Spare_Parts", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

# Objective Function
problem += pulp.lpSum(Profit[k] * x[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(Time[k][s] * x[k] for k in range(K)) <= Capacity[s], f"Capacity_Constraint_{s+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')