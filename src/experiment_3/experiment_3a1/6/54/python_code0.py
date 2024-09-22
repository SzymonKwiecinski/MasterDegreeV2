import pulp
import json

# Data from the provided JSON
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

# Parameters
P = data['NumParts']
M = data['NumMachines']
time = data['TimeRequired']
costs = data['MachineCosts']
availability = data['Availability']
prices = data['Prices']
min_batches = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hour = data['OvertimeHour']

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

# Problem
problem = pulp.LpProblem("Maximize_Total_Profit", pulp.LpMaximize)

# Objective Function
profit_expr = pulp.lpSum(prices[p] * batches[p] for p in range(P))  # Total revenue
cost_expr = pulp.lpSum(
    costs[m] * (pulp.lpSum(time[m][p] * batches[p] for p in range(P)) / 100) 
    for m in range(M))  # Total cost
problem += profit_expr - cost_expr, "Total_Profit"

# Constraints
# Time availability for each machine
for m in range(M):
    problem += pulp.lpSum(time[m][p] * batches[p] for p in range(P)) <= availability[m], f"Machine_Availability_{m}"

# Minimum production requirement for each part
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batches_{p}"

# Labor cost constraints for machine 1
labor_hours = pulp.lpSum((time[0][p] / 100) * batches[p] for p in range(P))
cost_labor = pulp.lpSum(
    (standard_cost * labor_hours if labor_hours <= overtime_hour[0] else 
     (standard_cost * overtime_hour[0]) + 
     ((labor_hours - overtime_hour[0]) * overtime_cost))
)

problem += cost_labor <= (labor_hours / 100) * (standard_cost + overtime_cost), "Labor_Cost_Constraint"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')