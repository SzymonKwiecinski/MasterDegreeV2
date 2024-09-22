import pulp
import json

# Load data
data = json.loads('{"T": 12, "Demand": [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], "OilCap": [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], "CoalCost": 10, "NukeCost": 5, "MaxNuke": 20, "CoalLife": 5, "NukeLife": 10}')

# Constants
T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
coal_add = pulp.LpVariable.dicts("coal_add", range(1, T + 1), lowBound=0)
nuke_add = pulp.LpVariable.dicts("nuke_add", range(1, T + 1), lowBound=0)

# Objective function
problem += pulp.lpSum(coal_cost * coal_add[t] + nuke_cost * nuke_add[t] for t in range(1, T + 1))

# Constraints
for t in range(1, T + 1):
    # Demand Satisfaction
    problem += (pulp.lpSum(coal_add[j] for j in range(max(1, t - coal_life + 1), t + 1)) +
                 pulp.lpSum(nuke_add[j] for j in range(max(1, t - nuke_life + 1), t + 1)) +
                 oil_cap[t - 1] >= demand[t - 1], f"Demand_Satisfaction_{t}")

    # Nuclear Capacity Limit
    problem += (pulp.lpSum(nuke_add[j] for j in range(max(1, t - nuke_life + 1), t + 1)) <=
                 (max_nuke / 100) * (oil_cap[t - 1] + 
                 pulp.lpSum(coal_add[j] for j in range(max(1, t - coal_life + 1), t + 1)) +
                 pulp.lpSum(nuke_add[j] for j in range(max(1, t - nuke_life + 1), t + 1))), 
                 f"Nuclear_Capacity_Limit_{t}")

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')