import pulp

# Data provided
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

# Initialize problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
num_parts = len(data['prices'])
num_machines = len(data['machine_costs'])

x = [pulp.LpVariable(f'x_{p}', lowBound=0) for p in range(num_parts)]
extra = [pulp.LpVariable(f'extra_{m}', lowBound=0, upBound=data['max_extra'][m]) for m in range(num_machines)]

# Objective function
profit = (
    pulp.lpSum(data['prices'][p] * x[p] for p in range(num_parts)) 
    - pulp.lpSum(
        data['machine_costs'][m] * (
            pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(num_parts))
        ) + extra[m] * data['extra_costs'][m] 
        for m in range(num_machines)
    )
)
problem += profit

# Constraints

# Machine availability including extra hours
for m in range(num_machines):
    problem += (
        pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(num_parts)) 
        <= data['availability'][m] + extra[m]
    )

# Minimum batch production requirements
for p in range(num_parts):
    problem += x[p] >= data['min_batches'][p]

# Solve problem
problem.solve()

# Print objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')