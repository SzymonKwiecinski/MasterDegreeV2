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
    'OvertimeHour': [400, 400, 300]
}

# Problem
problem = pulp.LpProblem("Auto_Parts_Profit_Maximization", pulp.LpMaximize)

# Variables
b = [pulp.LpVariable(f'b_p{p+1}', lowBound=0, cat='Continuous') for p in range(data['NumParts'])]
x = [pulp.LpVariable(f'x_m{m+1}', lowBound=0, cat='Continuous') for m in range(data['NumMachines'])]
y = pulp.LpVariable('y', lowBound=0, cat='Continuous')

# Objective Function
total_profit = (
    pulp.lpSum(data['Prices'][p] * b[p] for p in range(data['NumParts'])) -
    pulp.lpSum(data['MachineCosts'][m] * x[m] for m in range(data['NumMachines']))
    - (data['StandardCost'] * pulp.lpSum(min(y, data['OvertimeHour'][m]) for m in range(1))
       + data['OvertimeCost'] * pulp.lpSum(max(0, y - data['OvertimeHour'][m]) for m in range(1)))
)
problem += total_profit

# Constraints
# Machine hours constraint
for m in range(data['NumMachines']):
    problem += (
        pulp.lpSum(data['TimeRequired'][m][p] * b[p] for p in range(data['NumParts']))
        <= data['Availability'][m], f"Machine_{m+1}_Availability"
    )

# Minimum batch production requirement
for p in range(data['NumParts']):
    problem += (b[p] >= data['MinBatches'][p], f"Min_Batches_{p+1}")

# Total hours used on machine 1
problem += (x[0] == pulp.lpSum(data['TimeRequired'][0][p] * b[p] for p in range(data['NumParts'])) + y, "Total_Hours_Machine_1")

# Overtime condition
problem += (y >= 0, "Overtime_Non_Negativity")

# Solve
problem.solve()

# Output
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")