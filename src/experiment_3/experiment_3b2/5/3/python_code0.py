import pulp
import json

# Load data from JSON format
data = json.loads("{'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}")

# Create the LP problem
problem = pulp.LpProblem("Energy_Production_Optimization", pulp.LpMinimize)

# Decision variables
coal_add = pulp.LpVariable.dicts("coal_add", range(1, data['T'] + 1), lowBound=0)
nuke_add = pulp.LpVariable.dicts("nuke_add", range(1, data['T'] + 1), lowBound=0)
oil = pulp.LpVariable.dicts("oil", range(1, data['T'] + 1), lowBound=0, upBound=data['OilCap'])

# Objective function
problem += pulp.lpSum(data['CoalCost'] * coal_add[t] + data['NukeCost'] * nuke_add[t] for t in range(1, data['T'] + 1))

# Constraints
for t in range(1, data['T'] + 1):
    # Demand satisfaction constraint
    problem += (oil[t] + 
                 pulp.lpSum(coal_add[t - k] for k in range(1, min(t, data['CoalLife']) + 1)) + 
                 pulp.lpSum(nuke_add[t - k] for k in range(1, min(t, data['NukeLife']) + 1)) >= data['Demand'][t - 1])

    # Nuclear capacity limit constraint
    problem += (pulp.lpSum(nuke_add[t - k] for k in range(1, min(t, data['NukeLife']) + 1)) <= 
                 (data['MaxNuke'] / 100) * (oil[t] + 
                 pulp.lpSum(coal_add[t - k] for k in range(1, min(t, data['CoalLife']) + 1)) + 
                 pulp.lpSum(nuke_add[t - k] for k in range(1, min(t, data['NukeLife']) + 1))))

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')