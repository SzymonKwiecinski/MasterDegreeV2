import pulp
import json

# Input Data in JSON format
data = {'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}

# Extracting parameters from data
P = data['P']
cash = data['Cash']
hours = data['Hour']
costs = data['Cost']
prices = data['Price']
invest_percentages = data['InvestPercentage']
upgrade_hours = data['UpgradeHours']
upgrade_cost = data['UpgradeCost']
available_hours = data['AvailableHours']

# Create the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

# Decision variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(P)]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

# Constraints
# Machine hours constraint
total_hours = pulp.lpSum([production[i] * hours[i] for i in range(P)]) 
problem += total_hours <= available_hours + upgrade * upgrade_hours, "Machine_Hours_Constraint"

# Cash constraint
total_cost = pulp.lpSum([production[i] * costs[i] for i in range(P)]) 
total_revenue = pulp.lpSum([production[i] * prices[i] for i in range(P)]) 
total_investment = pulp.lpSum([total_revenue * invest_percentages[i] for i in range(P)])

problem += total_cost + upgrade_cost * upgrade <= cash + total_investment, "Cash_Constraint"

# Objective function: maximize net income
net_income = pulp.lpSum([production[i] * (prices[i] - costs[i]) for i in range(P)]) - upgrade_cost * upgrade
problem += net_income, "Net_Income_Objective"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "net_income": pulp.value(net_income),
    "production": [pulp.value(production[i]) for i in range(P)],
    "upgrade": bool(pulp.value(upgrade))
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')