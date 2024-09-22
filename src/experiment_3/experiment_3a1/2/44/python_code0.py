import pulp

# Data from JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Parameters
P = len(data['prices'])  # Number of products
M = len(data['machine_costs'])  # Number of machines

# Create the problem
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

# Decision variables
b = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['prices'][p] * b[p] for p in range(P)) - \
           pulp.lpSum(data['machine_costs'][m] * 
                       pulp.lpSum(data['time_required'][m][p] * b[p] for p in range(P)) 
                       for m in range(M)), "Total_Profit"

# Constraints for machine availability
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * b[p] for p in range(P)) <= data['availability'][m], f"Machine_Availability_{m}"

# Constraints for minimum production requirements
for p in range(P):
    problem += b[p] >= data['min_batches'][p], f"Minimum_Batches_{p}"

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')