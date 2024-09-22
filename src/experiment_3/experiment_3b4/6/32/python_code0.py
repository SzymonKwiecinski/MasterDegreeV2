import pulp

# Data
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

# Sets
K = range(data['NumProducts'])
S = range(data['NumMachines'])

# Parameters
produce_time = data['ProduceTime']
time = data['AvailableTime']
profit = data['Profit']

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
quantity = pulp.LpVariable.dicts("Quantity", K, lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(profit[k] * quantity[k] for k in K), "Total Profit"

# Constraints
for s in S:
    problem += pulp.lpSum(produce_time[k][s] * quantity[k] for k in K) <= time[s], f"Time_Constraint_Stage_{s}"

# Solve
problem.solve()

# Output the objective
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')