import pulp

# Data from JSON
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],  # Time taken to make spare parts on machines
    'profit': [30, 20, 40, 25, 10],                   # Profit from each spare part
    'capacity': [700, 1000]                           # Capacity of each machine
}

# Parameters
K = len(data['profit'])        # Number of different spare parts
S = len(data['capacity'])      # Number of machines
time_ks = data['time']         # Time to produce each spare part on each machine
profit_k = data['profit']      # Profit for each spare part
capacity_s = data['capacity']   # Machines capacity

# Create the problem
problem = pulp.LpProblem("Optimal_Production_of_Spare_Parts", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  # Quantity of spare parts to produce

# Objective Function
problem += pulp.lpSum(profit_k[k] * x[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(time_ks[k][s] * x[k] for k in range(K)) <= capacity_s[s], f"Machine_Capacity_{s}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')