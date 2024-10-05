import pulp

# Extract data from JSON
data = {
    "T": 12,
    "Demand": [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35],
    "OilCap": [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5],
    "CoalCost": 10,
    "NukeCost": 5,
    "MaxNuke": 20,
    "CoalLife": 5,
    "NukeLife": 10
}

T = data['T']
Demand = data['Demand']
OilCap = data['OilCap']
CoalCost = data['CoalCost']
NukeCost = data['NukeCost']
MaxNuke = data['MaxNuke'] / 100
CoalLife = data['CoalLife']
NukeLife = data['NukeLife']

# Define the problem
problem = pulp.LpProblem("Electricity_Capacity_Planning", pulp.LpMinimize)

# Decision variables
coal_cap_added = pulp.LpVariable.dicts(
    "CoalCapAdded", range(T), lowBound=0, cat='Continuous')
nuke_cap_added = pulp.LpVariable.dicts(
    "NukeCapAdded", range(T), lowBound=0, cat='Continuous')

# Objective function: Minimize the total cost
problem += sum(CoalCost * coal_cap_added[t] + NukeCost * nuke_cap_added[t] for t in range(T))

# Constraints
for t in range(T):
    # Total capacity must meet demand
    total_coal_cap = sum(coal_cap_added[j] for j in range(max(0, t - CoalLife + 1), t + 1))
    total_nuke_cap = sum(nuke_cap_added[j] for j in range(max(0, t - NukeLife + 1), t + 1))
    problem += OilCap[t] + total_coal_cap + total_nuke_cap >= Demand[t], f"DemandConstraint{t}"

    # Nuclear capacity limit
    problem += total_nuke_cap <= MaxNuke * (OilCap[t] + total_coal_cap + total_nuke_cap), f"NuclearCapacityConstraint{t}"

# Solve the problem
problem.solve()

# Extract results
coal_cap_added_result = [pulp.value(coal_cap_added[t]) for t in range(T)]
nuke_cap_added_result = [pulp.value(nuke_cap_added[t]) for t in range(T)]
total_cost = pulp.value(problem.objective)

output = {
    "coal_cap_added": coal_cap_added_result,
    "nuke_cap_added": nuke_cap_added_result,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')