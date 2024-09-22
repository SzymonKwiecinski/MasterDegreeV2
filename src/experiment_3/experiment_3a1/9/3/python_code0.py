import pulp
import json

# Load data from JSON
data = json.loads("{'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}")

# Parameters
T = data['T']
demand = data['Demand']
oil_capacity = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create the LP problem
problem = pulp.LpProblem("Electric_Capacity_Expansion", pulp.LpMinimize)

# Decision Variables
coal_vars = pulp.LpVariable.dicts("Coal", range(1, T + 1), lowBound=0)
nuke_vars = pulp.LpVariable.dicts("Nuke", range(1, T + 1), lowBound=0)

# Objective Function
problem += pulp.lpSum(coal_cost * coal_vars[t] + nuke_cost * nuke_vars[t] for t in range(1, T + 1)), "Total_Cost"

# Capacity Requirement Constraints
for t in range(1, T + 1):
    coal_sum = pulp.lpSum(coal_vars[j] for j in range(max(1, t - coal_life + 1), t + 1))
    nuke_sum = pulp.lpSum(nuke_vars[j] for j in range(max(1, t - nuke_life + 1), t + 1))
    problem += oil_capacity[t-1] + coal_sum + nuke_sum >= demand[t-1], f"Capacity_Requirement_{t}"

# Maximum Nuclear Capacity Constraints
for t in range(1, T + 1):
    total_capacity = oil_capacity[t-1] + pulp.lpSum(coal_vars[j] for j in range(1, t + 1)) + pulp.lpSum(nuke_vars[j] for j in range(1, t + 1))
    problem += pulp.lpSum(nuke_vars[j] for j in range(1, t + 1)) <= (max_nuke / 100) * total_capacity, f"Max_Nuclear_Capacity_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')