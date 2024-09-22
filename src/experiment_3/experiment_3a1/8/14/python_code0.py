import pulp
import json

# Data
data = json.loads('{"P": 2, "Cash": 3000, "Hour": [2, 6], "Cost": [3, 2], "Price": [6, 5], "InvestPercentage": [0.4, 0.3], "UpgradeHours": 2000, "UpgradeCost": 400, "AvailableHours": 2000}')

# Parameters
P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
invest_percentage = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

# Problem definition
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(P)]
u = pulp.LpVariable('u', cat='Binary')

# Objective function
problem += pulp.lpSum([(price[i] * x[i]) - (cost[i] * x[i]) - (invest_percentage[i] * price[i] * x[i]) for i in range(P)]) - (upgrade_cost * u), "Total_Net_Income"

# Constraints
problem += pulp.lpSum([cost[i] * x[i] for i in range(P)]) <= cash, "Cash_Availability"
problem += pulp.lpSum([hour[i] * x[i] for i in range(P)]) <= available_hours + (upgrade_hours * u), "Machine_Capacity"

# Solve the problem
problem.solve()

# Output objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')