import pulp
import json

# Data provided in JSON format
data = json.loads('{"NumMachines": 3, "NumParts": 4, "TimeRequired": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "MachineCosts": [160, 10, 15], "Availability": [200, 300, 500], "Prices": [570, 250, 585, 430], "MinBatches": [10, 10, 10, 10], "StandardCost": 20, "OvertimeCost": 30, "OvertimeHour": [400, 400, 300]}')

# Parameters
P = data['NumParts']
M = data['NumMachines']
time = data['TimeRequired']
cost = data['MachineCosts']
available = data['Availability']
price = data['Prices']
min_batches = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hour = data['OvertimeHour']

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

# Objective Function
total_profit = pulp.lpSum([price[p] * batches[p] for p in range(P)]) - \
               pulp.lpSum([cost[m] * pulp.lpSum([time[m][p] * batches[p] for p in range(P)]) for m in range(M)])
problem += total_profit, "Total_Profit"

# Constraints for machine availability
for m in range(M):
    problem += pulp.lpSum([time[m][p] * batches[p] for p in range(P)]) <= available[m], f"Machine_Availability_{m}"

# Constraints for minimum production requirements
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Production_{p}"

# Overtime labor cost consideration for machine 1
extra_hours = pulp.lpSum([time[0][p] * batches[p] for p in range(P)]) - available[0]
problem += (pulp.lpSum([time[0][p] * batches[p] for p in range(P)]) <= available[0] + pulp.lpSum([overtime_hour[0], 0]) +
            (overtime_cost * pulp.lpMax(0, extra_hours - overtime_hour[0])) +
            (standard_cost * pulp.lpMin(overtime_hour[0], extra_hours))), "Overtime_Cost_Consideration"

# Solve the problem
problem.solve()

# Output results
batches_result = [batches[p].varValue for p in range(P)]
total_profit_value = pulp.value(problem.objective)

print(f' (Objective Value): <OBJ>{total_profit_value}</OBJ>')