import pulp

# Data from JSON
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

# Problem setup
P = len(data['min_batches'])  # Number of different parts
M = len(data['availability'])  # Number of different machines

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

# Objective function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) - \
         pulp.lpSum(data['machine_costs'][m] * 
                     pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) 
                     for m in range(M))

problem += profit

# Constraints
# Machine time utilization constraints
for m in range(M):
    problem += (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m])

# Minimum production requirements
for p in range(P):
    problem += (batches[p] >= data['min_batches'][p])

# Labor cost constraints for Machine 1
total_hours_m1 = pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P))
problem += (total_hours_m1 <= data['overtime_hour'], "Overtime_Hour_Constraint")

# Profit constraint
problem += (profit >= data['min_profit'], "Minimum_Profit_Constraint")

# Solve the problem
problem.solve()

# Output results
batches_result = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

print(f' (Batches Produced): {batches_result}')
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')