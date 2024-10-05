import pulp

# Data from JSON
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

# Create the problem
problem = pulp.LpProblem("AutoParts_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
b = {p: pulp.LpVariable(f'b_{p}', lowBound=data['MinBatches'][p], cat='Continuous') for p in range(data['NumParts'])}

# Expressions for labor cost and profit
time_machine_1 = pulp.lpSum(data['TimeRequired'][0][p] * b[p] for p in range(data['NumParts']))
labor_cost = pulp.LpVariable("LaborCost", lowBound=0, cat='Continuous')

# Piecewise linear approximation for labor cost
problem += labor_cost, "Labor_Cost_Expression"
problem += labor_cost >= data['StandardCost'] * time_machine_1
problem += labor_cost >= (data['StandardCost'] * data['OvertimeHour'][0] +
                          data['OvertimeCost'] * (time_machine_1 - data['OvertimeHour'][0]))

# Objective Function
objective = pulp.lpSum(data['Prices'][p] * b[p] for p in range(data['NumParts'])) - \
            sum(data['MachineCosts'][m] * pulp.lpSum(data['TimeRequired'][m][p] * b[p] for p in range(data['NumParts']))
                for m in range(data['NumMachines'])) - labor_cost
problem += objective

# Constraints
for m in range(1, data['NumMachines']):  # Machines 2, 3, ..., M
    problem += pulp.lpSum(data['TimeRequired'][m][p] * b[p] for p in range(data['NumParts'])) <= data['Availability'][m], f"Availability_Constraint_Machine_{m+1}"
    
# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')