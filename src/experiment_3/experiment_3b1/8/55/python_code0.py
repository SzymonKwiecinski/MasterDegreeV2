import pulp

# Data from the provided input
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],  # Machine time per part
    'machine_costs': [160, 10, 15],  # Cost per hour for machines
    'availability': [200, 300, 500],  # Available hours per month for each machine
    'prices': [570, 250, 585, 430],  # Selling prices for each part
    'min_batches': [10, 10, 10, 10],  # Minimum batches required for each part
    'standard_cost': 20,  # Standard labor cost per hour
    'overtime_cost': 30,  # Overtime labor cost per hour
    'overtime_hour': 400,  # Hours after which overtime cost applies
    'min_profit': 5000  # Minimum profit required
}

P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
b = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum(data['prices'][p] * b[p] for p in range(P)) - \
         pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * b[p] for p in range(P)) for m in range(M))

problem += profit, "Total_Profit"

# Resource Availability Constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * b[p] for p in range(P)) <= data['availability'][m], f"Available_Hours_Machine_{m+1}"

# Minimum Production Requirements
for p in range(P):
    problem += b[p] >= data['min_batches'][p], f"Min_Batches_Part_{p+1}"

# Profit Constraint
problem += profit >= data['min_profit'], "Min_Profit"

# Labor Cost Calculations for Machine 1
# Total hours worked on machine 1
h = pulp.lpSum(data['time_required'][0][p] * b[p] for p in range(P))

# Define labor cost based on hours worked
labor_cost = pulp.LpVariable("Labor_Cost", lowBound=0)

problem += labor_cost == (data['standard_cost'] * h + data['overtime_cost'] * pulp.lpMax(0, h - data['overtime_hour'])), "Labor_Cost_Definition"

# Solve the problem
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')