import pulp

# Parse the data
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

time = data['time']
profit = data['profit']
capacity = data['capacity']

# Initialize problem
problem = pulp.LpProblem("Optimal_Spare_Parts_Production", pulp.LpMaximize)

# Number of spare parts (K) and machines (S)
K = len(profit)
S = len(capacity)

# Decision variables: quantity of each spare part to produce
x = [pulp.LpVariable(f"x_{k}", lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Maximize total profit
problem += pulp.lpSum(profit[k] * x[k] for k in range(K)), "Total Profit"

# Constraints
# Machine capacity constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * x[k] for k in range(K)) <= capacity[s], f"Machine_Capacity_{s}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')