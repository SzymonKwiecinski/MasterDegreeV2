import pulp
import json

# Input data in JSON format
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

# Decision Variables
coal = pulp.LpVariable.dicts('coal', range(T), lowBound=0, cat='Continuous')
nuke = pulp.LpVariable.dicts('nuke', range(T), lowBound=0, cat='Continuous')

# Problem Definition
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Objective Function
problem += pulp.lpSum(coal_cost * coal[t] + nuke_cost * nuke[t] for t in range(T)), "Total Cost"

# Constraints
for t in range(T):
    # Capacity Constraint
    capacity = oil_capacity[t] + pulp.lpSum(coal[t-s] for s in range(min(t, coal_life))) + pulp.lpSum(nuke[t-s] for s in range(min(t, nuke_life))) 
    problem += capacity >= demand[t], f"Capacity_Constraint_{t}"

    # Nuclear Capacity Constraint
    nuke_capacity_limit = (max_nuke / 100.0) * capacity
    problem += pulp.lpSum(coal[t-s] for s in range(min(t, coal_life))) + pulp.lpSum(nuke[t-s] for s in range(min(t, nuke_life))) * (nuke_cost / coal_cost) <= nuke_capacity_limit, f"Nuclear_Capacity_Constraint_{t}"

# Solve the problem
problem.solve()

# Output results
coal_added = [coal[t].varValue for t in range(T)]
nuke_added = [nuke[t].varValue for t in range(T)]
total_cost = pulp.value(problem.objective)

print(f' (Coal capacities added each year): {coal_added}')
print(f' (Nuclear capacities added each year): {nuke_added}')
print(f' (Total cost): <OBJ>{total_cost}</OBJ>')