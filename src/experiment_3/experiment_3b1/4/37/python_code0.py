import pulp

# Given data
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],  # time[k][s]
    'profit': [30, 20, 40, 25, 10],  # profit[k]
    'capacity': [700, 1000]  # capacity[s]
}

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define variables
K = len(data['profit'])  # number of different spare parts
S = len(data['capacity'])  # number of different shops
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(data['profit'][k] * quantity[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(data['time'][k][s] * quantity[k] for k in range(K)) <= data['capacity'][s], f"Capacity_Constraint_Shop_{s+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')