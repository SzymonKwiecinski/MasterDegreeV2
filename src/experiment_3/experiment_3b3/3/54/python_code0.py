import pulp

# Data from the JSON format
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

P = data['NumParts']
M = data['NumMachines']
time_required = data['TimeRequired']
cost_m = data['MachineCosts']
availability = data['Availability']
price_p = data['Prices']
min_batches = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hour = data['OvertimeHour'][0]  # Using only the first machine's overtime hour since it is relevant for labor cost

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
b = [pulp.LpVariable(f'b_{p}', lowBound=0, cat='Continuous') for p in range(P)]

# Objective Function components
profit_from_sales = sum((price_p[p] - sum(cost_m[m] * time_required[m][p] / 100 for m in range(M))) * b[p] for p in range(P))

# Labor Cost calculation
machine_1_usage = sum(b[p] * time_required[0][p] / 100 for p in range(P))
labor_cost = pulp.LpVariable('Labor_Cost', lowBound=0, cat='Continuous')

# Defining labor cost constraint
problem += (labor_cost == standard_cost * machine_1_usage, "Labor_Cost_Standard") if machine_1_usage <= overtime_hour else \
    (labor_cost == standard_cost * overtime_hour + overtime_cost * (machine_1_usage - overtime_hour), "Labor_Cost_Overtime")

# Define the objective function
problem += profit_from_sales - labor_cost, "Total_Profit"

# Constraints
# Machine availability constraints for machines other than machine 1
for m in range(1, M):
    problem += sum(b[p] * time_required[m][p] / 100 for p in range(P)) <= availability[m], f"Availability_Machine_{m}"

# Minimum production requirements
for p in range(P):
    problem += b[p] >= min_batches[p], f"Min_Batches_Part_{p}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')