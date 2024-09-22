import pulp
import json

# Load data
data = json.loads('{"T": 12, "Demand": [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], "OilCap": [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], "CoalCost": 10, "NukeCost": 5, "MaxNuke": 20, "CoalLife": 5, "NukeLife": 10}')

# Parameters
T = data['T']
demand = data['Demand']
oil_capacity = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create the problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision Variables
coal = pulp.LpVariable.dicts("Coal", range(1, T + 1), lowBound=0, cat='Continuous')
nuke = pulp.LpVariable.dicts("Nuke", range(1, T + 1), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(coal_cost * coal[t] + nuke_cost * nuke[t] for t in range(1, T + 1)), "Total Cost"

# Constraints
for t in range(1, T + 1):
    problem += (oil_capacity[t-1] + 
                pulp.lpSum(coal[t-s] for s in range(1, min(t, coal_life) + 1)) + 
                pulp.lpSum(nuke[t-s] for s in range(1, min(t, nuke_life) + 1)) >= demand[t-1]), f"Demand_Constraint_{t}")

# Nuclear capacity constraint
problem += (pulp.lpSum(nuke[s] for s in range(1, T + 1)) / 
            (pulp.lpSum(coal[s] for s in range(1, T + 1)) + 
             pulp.lpSum(nuke[s] for s in range(1, T + 1)) + 
             pulp.lpSum(oil_capacity[s-1] for s in range(1, T + 1))) <= max_nuke / 100), "Nuclear_Capacity_Constraint")

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')