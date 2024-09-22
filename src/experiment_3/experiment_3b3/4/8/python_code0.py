import pulp

# Data
data = {
    'NumParts': 5,
    'NumMachines': 2,
    'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'Profit': [30, 20, 40, 25, 10],
    'Capacity': [700, 1000]
}

# Indices
K = data['NumParts']
S = data['NumMachines']

# Parameters
time = data['Time']
profit = data['Profit']
capacity = data['Capacity']

# Problem
problem = pulp.LpProblem("Spare_Automobile_Parts_Production", pulp.LpMaximize)

# Decision Variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s], f"Capacity_Shop_{s}"

# Solve the problem
problem.solve()

# Output
quantities = [pulp.value(quantity[k]) for k in range(K)]
output = {'quantity': quantities}

print(f'Optimal production quantities: {output}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')