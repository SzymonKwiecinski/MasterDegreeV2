import pulp
import json

# Data provided in JSON format
data = json.loads("{'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}")

# Extracting data
T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
x_coal = pulp.LpVariable.dicts("Coal_Capacity", range(1, T + 1), lowBound=0)
x_nuke = pulp.LpVariable.dicts("Nuke_Capacity", range(1, T + 1), lowBound=0)

# Objective function
problem += pulp.lpSum(coal_cost * x_coal[t] + nuke_cost * x_nuke[t] for t in range(1, T + 1))

# Constraints

# Demand constraints
for t in range(1, T + 1):
    problem += (
        oil_cap[t - 1] + 
        pulp.lpSum(x_coal[j] for j in range(max(1, t - coal_life + 1), t + 1)) +
        pulp.lpSum(x_nuke[j] for j in range(max(1, t - nuke_life + 1), t + 1)) >= demand[t - 1],
        f"Demand_Constraint_{t}"
    )

# Nuclear capacity constraints
for t in range(1, T + 1):
    problem += (
        pulp.lpSum(x_nuke[j] for j in range(max(1, t - nuke_life + 1), t + 1)) <= 
        (max_nuke / 100) * (
            oil_cap[t - 1] + 
            pulp.lpSum(x_coal[j] for j in range(max(1, t - coal_life + 1), t + 1)) +
            pulp.lpSum(x_nuke[j] for j in range(max(1, t - nuke_life + 1), t + 1))
        ),
        f"Nuclear_Capacity_Constraint_{t}"
    )

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')