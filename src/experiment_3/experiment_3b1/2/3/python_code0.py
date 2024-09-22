import pulp
import json

# Data 
data = json.loads('{"T": 12, "Demand": [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], "OilCap": [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], "CoalCost": 10, "NukeCost": 5, "MaxNuke": 20, "CoalLife": 5, "NukeLife": 10}')
T = data['T']
demand = data['Demand']
oil_capacity = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create the LP problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision Variables
coal = pulp.LpVariable.dicts("coal", range(T), lowBound=0)
nuke = pulp.LpVariable.dicts("nuke", range(T), lowBound=0)

# Objective Function
problem += pulp.lpSum([coal_cost * coal[t] + nuke_cost * nuke[t] for t in range(T)])

# Constraints
for t in range(T):
    # Capacity must meet the demand
    capacity = (
        oil_capacity[t] +
        pulp.lpSum([coal[j] for j in range(max(0, t - coal_life + 1), t + 1)]) +
        pulp.lpSum([nuke[j] for j in range(max(0, t - nuke_life + 1), t + 1)])
    )
    problem += capacity >= demand[t]

    # Nuclear capacity limit
    total_capacity = (
        oil_capacity[t] +
        pulp.lpSum([coal[j] for j in range(t + 1)]) +
        pulp.lpSum([nuke[j] for j in range(t + 1)])
    )
    problem += pulp.lpSum([nuke[j] for j in range(t + 1)]) <= (max_nuke / 100) * total_capacity

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')