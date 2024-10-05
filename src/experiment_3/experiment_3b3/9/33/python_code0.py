import pulp

# Data from JSON
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Parameters
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Decision Variables
isincluded = pulp.LpVariable.dicts("isincluded", range(K), cat="Binary")

# Objective Function
problem += pulp.lpSum(values[k] * isincluded[k] for k in range(K)), "Total_Value"

# Constraints
problem += pulp.lpSum(sizes[k] * isincluded[k] for k in range(K)) <= C, "Capacity_Constraint"

# Solve the problem
problem.solve()

# Output
isincluded_output = [pulp.value(isincluded[k]) for k in range(K)]
print(f'Decision Variables (isincluded): {isincluded_output}')

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')