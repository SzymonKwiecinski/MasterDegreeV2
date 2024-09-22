import pulp

# Data loading
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

# Sets
P = data['NumParts']
M = data['NumMachines']

# Parameters
time_required = data['TimeRequired']
cost_m = data['MachineCosts']
available_m = data['Availability']
price_p = data['Prices']
min_batches_p = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hour = data['OvertimeHour']

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

# Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function
profit_expr = pulp.lpSum([price_p[p] * batches[p] for p in range(P)]) - \
              pulp.lpSum([cost_m[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)]) - \
              pulp.lpSum([pulp.lpSum([time_required[0][p] * batches[p] for p in range(P)]) * standard_cost if pulp.lpSum([time_required[0][p] * batches[p] for p in range(P)]) <= overtime_hour[0] 
              else (overtime_hour[0] * standard_cost + 
                    (pulp.lpSum([time_required[0][p] * batches[p] for p in range(P)]) - overtime_hour[0]) * overtime_cost) 
              for p in range(P)])  # Fixed the indentation here
              ])

# Constraints
# Production Time Constraints for each machine
for m in range(M):
    problem += (pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= available_m[m]), f"Machine_{m+1}_Time_Constraint"

# Minimum production requirements
for p in range(P):
    problem += (batches[p] >= min_batches_p[p]), f"Min_Batches_Constraint_{p+1}"

# Add the objective
problem += profit_expr

# Solve the problem
problem.solve()

# Output results
batches_output = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')