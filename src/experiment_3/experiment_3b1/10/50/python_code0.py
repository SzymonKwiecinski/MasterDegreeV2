import pulp

# Data from JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10], 
    'extra_costs': [0, 15, 22.5], 
    'max_extra': [0, 80, 80]
}

# Constants
P = len(data['prices'])  # Number of different parts
M = len(data['machine_costs'])  # Number of different machines

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)
extra_time = pulp.LpVariable.dicts("extra_time", range(M), lowBound=0)

# Objective Function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) \
        - pulp.lpSum(data['machine_costs'][m] * (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) + extra_time[m]) + 
                   data['extra_costs'][m] * extra_time[m] for m in range(M))
problem += profit

# Constraints

# Production Requirements
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

# Machine Availability
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) + extra_time[m] <= data['availability'][m] + data['max_extra'][m]

# Extra Time Limit
for m in range(M):
    problem += extra_time[m] <= data['max_extra'][m]

# Solve the problem
problem.solve()

# Output results
batches_result = [pulp.value(batches[p]) for p in range(P)]
extra_time_result = [pulp.value(extra_time[m]) for m in range(M)]
total_profit = pulp.value(problem.objective)

print(f'Batches Produced: {batches_result}')
print(f'Extra Time Purchased: {extra_time_result}')
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')