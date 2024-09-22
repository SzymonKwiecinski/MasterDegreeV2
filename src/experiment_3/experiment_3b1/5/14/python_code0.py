import pulp
import json

# Data from the JSON format
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 
        'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 
        'AvailableHours': 2000}

# Extracting parameters
P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
invest_percentage = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

# Define the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(1, P + 1), lowBound=0, cat='Continuous')  # Production quantities
u = pulp.LpVariable("u", cat='Binary')  # Upgrade decision

# Objective Function
problem += pulp.lpSum([(price[i-1] * x[i] - cost[i-1] * x[i] - invest_percentage[i-1] * (price[i-1] * x[i])) for i in range(1, P + 1)]) - upgrade_cost * u, "Total_Net_Income"

# Constraints
problem += pulp.lpSum([hour[i-1] * x[i] for i in range(1, P + 1)]) <= available_hours + upgrade_hours * u, "Machine_Capacity_Constraint"
problem += pulp.lpSum([cost[i-1] * x[i] for i in range(1, P + 1)]) <= cash, "Cash_Availability_Constraint"

# Solve the problem
problem.solve()

# Output results
net_income = pulp.value(problem.objective)
production = [pulp.value(x[i]) for i in range(1, P + 1)]
upgrade = pulp.value(u)

print(f' (Objective Value): <OBJ>{net_income}</OBJ>')
print(f'Production quantities: {production}')
print(f'Upgrade: {upgrade}')