import pulp

# Data
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
    'OvertimeHour': 400
}

# Indices
P = range(data['NumParts'])
M = range(data['NumMachines'])

# Decision Variables
batches = {p: pulp.LpVariable(f'batches_{p}', lowBound=data['MinBatches'][p], cat='Continuous') for p in P}
hours_machine1_standard = pulp.LpVariable('hours_machine1_standard', lowBound=0, cat='Continuous')
hours_machine1_overtime = pulp.LpVariable('hours_machine1_overtime', lowBound=0, cat='Continuous')

# Problem
problem = pulp.LpProblem("Maximize_Profit_Auto_Parts", pulp.LpMaximize)

# Objective Function
revenue = pulp.lpSum(data['Prices'][p] * batches[p] for p in P)
cost_machines = (pulp.lpSum(data['MachineCosts'][m] * data['TimeRequired'][m][p] * batches[p] for m in range(1, data['NumMachines']) for p in P))
cost_machine1 = data['StandardCost'] * hours_machine1_standard + data['OvertimeCost'] * hours_machine1_overtime

problem += revenue - (cost_machines + cost_machine1), "Total_Profit"

# Constraints

# Machine Time Constraint for m = 2, ..., M
for m in range(1, data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in P) <= data['Availability'][m], f"Machine_Time_Constraint_{m}"

# Machine 1 Time Partitioning
problem += pulp.lpSum(data['TimeRequired'][0][p] * batches[p] for p in P) == hours_machine1_standard + hours_machine1_overtime, "Machine_1_Time_Partitioning"

# Overtime Constraint for Machine 1
problem += hours_machine1_standard <= data['OvertimeHour'], "Overtime_Constraint_Machine_1"

# Solve
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')