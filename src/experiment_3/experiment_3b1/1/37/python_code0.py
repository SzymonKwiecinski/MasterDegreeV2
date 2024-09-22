import pulp

# Data from the JSON format
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Extracting data
time = data['time']  # time[k][s] - Required worker-hours for part k in shop s
profit = data['profit']  # profit[k] - Profit of part k
capacity = data['capacity']  # capacity[s] - Capacity of shop s

K = len(profit)  # Number of spare parts
S = len(capacity)  # Number of shops

# Create the Linear Programming problem
problem = pulp.LpProblem("Spare_Parts_Production", pulp.LpMaximize)

# Decision Variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

# Objective Function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_{s+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')