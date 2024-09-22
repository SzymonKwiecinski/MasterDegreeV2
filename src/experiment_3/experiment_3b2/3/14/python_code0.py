import pulp
import json

# Data from JSON
data = json.loads('{"P": 2, "Cash": 3000, "Hour": [2, 6], "Cost": [3, 2], "Price": [6, 5], "InvestPercentage": [0.4, 0.3], "UpgradeHours": 2000, "UpgradeCost": 400, "AvailableHours": 2000}')

# Parameters
P = data['P']
cash = data['Cash']
hour = data['Hour']
cost = data['Cost']
price = data['Price']
investPercentage = data['InvestPercentage']
upgradeHours = data['UpgradeHours']
upgradeCost = data['UpgradeCost']
availableHours = data['AvailableHours']

# Problem definition
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(P)]
u = pulp.LpVariable('u', cat='Binary')

# Objective Function
net_income = pulp.lpSum([(price[i] - cost[i] - price[i] * investPercentage[i]) * x[i] for i in range(P)]) - u * upgradeCost
problem += net_income, "Total_Net_Income"

# Constraints
# Machine capacity constraint
problem += pulp.lpSum([hour[i] * x[i] for i in range(P)]) <= availableHours + u * upgradeHours, "Machine_Capacity_Constraint"

# Cash availability constraint
problem += pulp.lpSum([cost[i] * x[i] for i in range(P)]) <= cash + pulp.lpSum([price[i] * investPercentage[i] * x[i] for i in range(P)]) - u * upgradeCost, "Cash_Availability_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')