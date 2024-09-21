import pulp

# Data
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],  # Time taken for each spare part on each machine
    'profit': [30, 20, 40, 25, 10],                   # Profit from each spare part
    'capacity': [700, 1000]                           # Capacity of each machine
}

# Parameters
K = len(data['profit'])       # Number of spare parts
S = len(data['capacity'])     # Number of machines
Time = data['time']           # Time matrix
Profit = data['profit']       # Profit vector
Capacity = data['capacity']   # Capacity vector

# Problem Definition
problem = pulp.LpProblem("Optimal_Production_of_Spare_Parts", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  # Quantity of each spare part to produce

# Objective Function
problem += pulp.lpSum(Profit[k] * x[k] for k in range(K)), "Total_Profit"

# Constraints
# Time constraints for each machine
for s in range(S):
    problem += pulp.lpSum(Time[k][s] * x[k] for k in range(K)) <= Capacity[s], f"Machine_Capacity_{s}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')