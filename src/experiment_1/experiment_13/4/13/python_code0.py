import pulp

# Data from the JSON format
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Parameters
K = len(data['profit'])  # Number of different spare parts
S = len(data['capacity'])  # Number of machines capable of making the spare parts
Time = data['time']  # Time taken to make spare part k on machine s
Profit = data['profit']  # Profit obtained from making spare part k
Capacity = data['capacity']  # Capacity of machine s

# Decision Variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  # Quantity of spare part k to produce

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function
problem += pulp.lpSum(Profit[k] * x[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(Time[k][s] * x[k] for k in range(K)) <= Capacity[s], f"Machine_Capacity_{s}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')