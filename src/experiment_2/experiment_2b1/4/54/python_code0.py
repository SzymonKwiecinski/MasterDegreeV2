import pulp
import json

# Input data
data = {
    'NumMachines': 3,
    'NumParts': 4,
    'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'MachineCosts': [160, 10, 15],
    'Availability': [200, 300, 500],
    'Prices': [570, 250, 585, 430],
    'MinBatches': [10, 10, 10, 10],
    'StandardCost': 20,
    'OvertimeCost': 30,
    'OvertimeHour': [400, 400, 300]
}

# Problem variables
num_machines = data['NumMachines']
num_parts = data['NumParts']
time_required = data['TimeRequired']
machine_costs = data['MachineCosts']
availability = data['Availability']
prices = data['Prices']
min_batches = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hours = data['OvertimeHour']

# Initialize the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(num_parts), lowBound=0, cat='Integer')

# Objective function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(num_parts)) - \
         pulp.lpSum(machine_costs[m] * 
                     (pulp.lpSum(time_required[m][p] * batches[p] / 100 for p in range(num_parts)) 
                      / availability[m] if availability[m] > 0 else 0) 
                     for m in range(num_machines))
          
problem += profit

# Constraints
for p in range(num_parts):
    problem += batches[p] >= min_batches[p]

# Machine time constraints
for m in range(num_machines):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(num_parts)) <= availability[m] * 100

# Solve the problem
problem.solve()

# Output the results
batches_output = [batches[p].varValue for p in range(num_parts)]
total_profit = pulp.value(problem.objective)

output = {
    "batches": batches_output,
    "total_profit": total_profit
}

print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')