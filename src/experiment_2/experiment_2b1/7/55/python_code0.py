import pulp
import json

# Input data in JSON format
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'min_batches': [10, 10, 10, 10], 
        'standard_cost': 20, 
        'overtime_cost': 30, 
        'overtime_hour': 400, 
        'min_profit': 5000}

# Parameters
P = len(data['prices'])  # number of parts
M = len(data['machine_costs'])  # number of machines

# Create the LP problem
problem = pulp.LpProblem("AutoPartsProduction", pulp.LpMaximize)

# Decision variables: batches produced for each part
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective function: maximize profit
profit = pulp.lpSum((data['prices'][p] * batches[p] - 
                     pulp.lpSum(data['time_required'][m][p] * 
                     data['machine_costs'][m] * batches[p] 
                     for m in range(M))) for p in range(P))
problem += profit, "Total Profit"

# Constraints for minimum batches
for p in range(P):
    problem += batches[p] >= data['min_batches'][p], f"MinBatches_{p}"

# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m], f"MachineAvailability_{m}"

# Labor cost constraint for Machine 1 (outsource)
total_time_machine_1 = pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P))
standard_hours = pulp.lpSum(pulp.lpMin(total_time_machine_1, data['overtime_hour']))
overtime_hours = total_time_machine_1 - data['overtime_hour']
overtime_hours = pulp.lpMax(overtime_hours, 0)

total_labor_cost = data['standard_cost'] * standard_hours + data['overtime_cost'] * overtime_hours
problem += profit - total_labor_cost >= data['min_profit'], "MinProfitConstraint"

# Solve the problem
problem.solve()

# Collect results
batches_result = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output result in the specified format
result = {
    "batches": batches_result,
    "total_profit": total_profit
}

# Print objective value
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')