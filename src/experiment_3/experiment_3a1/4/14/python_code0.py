import pulp
import json

# Data extraction from JSON
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

# Define the problem
problem = pulp.LpProblem("Production_and_Investment_Problem", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("Production", range(P), lowBound=0)
u = pulp.LpVariable("Upgrade", cat='Binary')

# Objective Function
problem += pulp.lpSum([(price[i] - cost[i]) * x[i] - invest_percentage[i] * (price[i] * x[i]) for i in range(P)]) - upgrade_cost * u, "Total_Net_Income"

# Cash Constraint
problem += pulp.lpSum([cost[i] * x[i] for i in range(P)]) <= cash - pulp.lpSum([invest_percentage[i] * (price[i] * x[i]) for i in range(P)]), "Cash_Constraint"

# Machine Hours Constraint
problem += pulp.lpSum([hour[i] * x[i] for i in range(P)]) <= available_hours + upgrade_hours * u, "Machine_Hours_Constraint"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')