import pulp

# Data from JSON
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Parameters
K = len(data['profit'])  # Number of spare parts
S = len(data['capacity'])  # Number of machines
Time = data['time']  # Time to make spare parts on each machine
Profit = data['profit']  # Profit from each spare part
Capacity = data['capacity']  # Capacity of each machine

# Create the LP problem
problem = pulp.LpProblem("Optimal_Production_of_Spare_Parts", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  # Quantity of each spare part to produce

# Objective Function
problem += pulp.lpSum(Profit[k] * x[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(Time[k][s] * x[k] for k in range(K)) <= Capacity[s], f"Capacity_Constraint_{s}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')