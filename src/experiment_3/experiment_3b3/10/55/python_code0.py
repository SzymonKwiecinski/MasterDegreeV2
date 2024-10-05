import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'standard_cost': 20,
    'overtime_cost': 30,
    'overtime_hour': 400,
    'min_profit': 5000
}

# Parameters
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Problem
problem = pulp.LpProblem("AutoPartsProfitMaximization", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

# Objective Function: Maximize Total Profit
profits = [
    data['prices'][p] * batches[p] - pulp.lpSum(
        data['machine_costs'][m] * data['time_required'][m][p] * batches[p] / 100 for m in range(M)
    ) for p in range(P)
]

total_time = pulp.lpSum(data['time_required'][m][p] * batches[p] for m in range(M) for p in range(P))
labor_cost = pulp.LpVariable("labor_cost", lowBound=0, cat='Continuous')
problem += pulp.lpSum(profits) - labor_cost

# Constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m]

for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

problem += pulp.lpSum(profits) - labor_cost >= data['min_profit']

# Labor cost calculation based on overtime
problem += labor_cost == (
    data['standard_cost'] * total_time
    if total_time <= data['overtime_hour']
    else data['standard_cost'] * data['overtime_hour'] + data['overtime_cost'] * (total_time - data['overtime_hour'])
)

# Solve
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')