import pulp

# Data
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

# Extract data
T = data["T"]
Demand = data["Demand"]
OilCap = data["OilCap"]
CoalCost = data["CoalCost"]
NukeCost = data["NukeCost"]
MaxNuke = data["MaxNuke"]
CoalLife = data["CoalLife"]
NukeLife = data["NukeLife"]

# Define the problem
problem = pulp.LpProblem("Electricity_Capacity_Planning", pulp.LpMinimize)

# Decision variables
coal_capacity_added = [pulp.LpVariable(f'coal_capacity_added_{t}', lowBound=0, cat='Continuous') for t in range(T)]
nuke_capacity_added = [pulp.LpVariable(f'nuke_capacity_added_{t}', lowBound=0, cat='Continuous') for t in range(T)]

# Total capacity for each year
total_capacity = [pulp.LpVariable(f'total_capacity_{t}', lowBound=0, cat='Continuous') for t in range(T)]

# Objective function: Minimize total cost
total_cost = pulp.lpSum(CoalCost * coal_capacity_added[t] + NukeCost * nuke_capacity_added[t] for t in range(T))
problem += total_cost, "Total_Cost"

# Constraints
for t in range(T):
    # Total capacity available
    coal_contrib = pulp.lpSum(coal_capacity_added[i] for i in range(max(0, t - CoalLife + 1), t + 1))
    nuke_contrib = pulp.lpSum(nuke_capacity_added[i] for i in range(max(0, t - NukeLife + 1), t + 1))
    problem += total_capacity[t] == OilCap[t] + coal_contrib + nuke_contrib

    # Demand satisfaction
    problem += total_capacity[t] >= Demand[t]

    # Nuclear capacity constraint
    problem += nuke_contrib <= (MaxNuke / 100) * total_capacity[t]

# Solve the problem
problem.solve()

# Output the results
coal_cap_added_result = [pulp.value(coal_capacity_added[t]) for t in range(T)]
nuke_cap_added_result = [pulp.value(nuke_capacity_added[t]) for t in range(T)]
total_cost_result = pulp.value(problem.objective)

output = {
    "coal_cap_added": coal_cap_added_result,
    "nuke_cap_added": nuke_cap_added_result,
    "total_cost": total_cost_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')