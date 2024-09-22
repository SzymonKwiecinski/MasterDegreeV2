import pulp
import json

# Data input
data = json.loads("{'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}")

# Model parameters
P = data['P']
cash = data['Cash']
hours = data['Hour']
costs = data['Cost']
prices = data['Price']
invest_percentage = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

# Initialize the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0)  # Production quantities
u = pulp.LpVariable("u", cat='Binary')  # Machine upgrade binary variable

# Objective Function
problem += pulp.lpSum(((prices[i] - costs[i]) * x[i] - invest_percentage[i] * prices[i] * x[i]) for i in range(P)) - upgrade_cost * u, "Total_Net_Income")

# Constraints
# Machine capacity constraint
problem += (pulp.lpSum(hours[i] * x[i] for i in range(P)) <= available_hours + upgrade_hours * u, "Machine_Capacity_Constraint")

# Cash availability constraint
problem += (pulp.lpSum((costs[i] * x[i] - invest_percentage[i] * prices[i] * x[i]) for i in range(P)) + upgrade_cost * u <= cash, "Cash_Availability_Constraint"))

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')