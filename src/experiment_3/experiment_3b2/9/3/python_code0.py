import pulp
import json

# Data in JSON format
data = json.loads('{"T": 12, "Demand": [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], "OilCap": [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], "CoalCost": 10, "NukeCost": 5, "MaxNuke": 20, "CoalLife": 5, "NukeLife": 10}')

# Define the problem
problem = pulp.LpProblem("Electricity_Capacity_Planning", pulp.LpMinimize)

# Decision Variables
x_coal = pulp.LpVariable.dicts("x_coal", range(1, data['T'] + 1), lowBound=0, cat='Continuous')
x_nuke = pulp.LpVariable.dicts("x_nuke", range(1, data['T'] + 1), lowBound=0, cat='Continuous')
o = pulp.LpVariable.dicts("o", range(1, data['T'] + 1), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['CoalCost'] * x_coal[t] + data['NukeCost'] * x_nuke[t] for t in range(1, data['T'] + 1))

# Constraints

# Demand Satisfaction
for t in range(1, data['T'] + 1):
    demand_expr = o[t] + pulp.lpSum(x_coal[j] for j in range(max(1, t - data['CoalLife'] + 1), t + 1)) + \
                 pulp.lpSum(x_nuke[j] for j in range(max(1, t - data['NukeLife'] + 1), t + 1))
    problem += (demand_expr >= data['Demand'][t - 1], f"Demand_Satisfaction_{t}")

# Nuclear Capacity Limit
for t in range(1, data['T'] + 1):
    nuke_capacity_expr = pulp.lpSum(x_nuke[j] for j in range(max(1, t - data['NukeLife'] + 1), t + 1))
    problem += (nuke_capacity_expr <= (data['MaxNuke'] / 100) * \
                 (o[t] + pulp.lpSum(x_coal[j] for j in range(max(1, t - data['CoalLife'] + 1), t + 1)) + \
                  pulp.lpSum(x_nuke[j] for j in range(max(1, t - data['NukeLife'] + 1), t + 1))), 
                 f"Nuclear_Capacity_Limit_{t}")

# Solve the problem
problem.solve()

# Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')