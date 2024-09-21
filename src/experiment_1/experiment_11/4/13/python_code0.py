import pulp

# Data from the provided JSON format
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],  # Time taken to make each spare part on each machine
    'profit': [30, 20, 40, 25, 10],  # Profit for each spare part
    'capacity': [700, 1000]  # Capacity of each machine
}

# Parameters
K = len(data['profit'])  # Number of spare parts
S = len(data['capacity'])  # Number of machines
Time = data['time']  # Time matrix
Profit = data['profit']  # Profit array
Capacity = data['capacity']  # Capacity array

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  # Quantity of each spare part to produce

# Objective function
problem += pulp.lpSum(Profit[k] * x[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(Time[k][s] * x[k] for k in range(K)) <= Capacity[s], f"Machine_Capacity_{s+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')