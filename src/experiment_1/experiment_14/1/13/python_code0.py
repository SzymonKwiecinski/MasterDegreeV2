import pulp

# Data from JSON
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Number of different spare parts
K = len(data['profit'])  
# Number of machines
S = len(data['capacity'])  

# Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Problem
problem = pulp.LpProblem("Optimal_Production_Spare_Parts", pulp.LpMaximize)

# Objective Function: Maximize Z = Sum(Profit_k * x_k)
problem += pulp.lpSum(data['profit'][k] * x[k] for k in range(K))

# Constraints

# Time constraints: Sum(Time_{ks} * x_k) <= Capacity_s for each machine s
for s in range(S):
    problem += pulp.lpSum(data['time'][k][s] * x[k] for k in range(K)) <= data['capacity'][s]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')