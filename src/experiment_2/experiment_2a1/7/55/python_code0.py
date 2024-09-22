import pulp
import json

# Input data
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
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Create a linear programming problem
problem = pulp.LpProblem("Auto_Parts_Production", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective function - Maximize profit
profit = pulp.lpSum((data['prices'][p] * batches[p] - 
                     pulp.lpSum(data['time_required'][m][p] * data['machine_costs'][m] * (batches[p] / 100) 
                                for m in range(M))) 
                    for p in range(P))
problem += profit

# Constraints for machine availability
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m]

# Minimum batches constraint
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

# Profit constraint
total_cost = (pulp.lpSum(data['standard_cost'] * (pulp.lpSum(data['time_required'][0][p] * (batches[p] / 100) for p in range(P)))
                            for m in range(1, M))) + \
              (pulp.lpSum(data['overtime_cost'] * (pulp.lpSum(data['time_required'][0][p] * (batches[p] / 100) - data['overtime_hour'] 
                            for p in range(P) if (pulp.lpSum(data['time_required'][0][p] * (batches[p] / 100)) > data['overtime_hour'])) )
                            for m in range(1, M)) if (pulp.lpSum(data['time_required'][0][p] * (batches[p] / 100) 
                            for p in range(P) if (pulp.lpSum(data['time_required'][0][p] * (batches[p] / 100)) > data['overtime_hour'])) > 0))
problem += profit - total_cost >= data['min_profit']

# Solve the problem
problem.solve()

# Output results
batches_result = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

output = {
    "batches": batches_result,
    "total_profit": total_profit
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')