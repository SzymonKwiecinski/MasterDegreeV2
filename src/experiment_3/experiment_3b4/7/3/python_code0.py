import pulp

# Data
T = 12
Demand = [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35]
OilCap = [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5]
CoalCost = 10
NukeCost = 5
MaxNuke = 20
CoalLife = 5
NukeLife = 10

# Problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision Variables
coal_cap_added = [pulp.LpVariable(f"coal_cap_added_{t}", lowBound=0) for t in range(T)]
nuke_cap_added = [pulp.LpVariable(f"nuke_cap_added_{t}", lowBound=0) for t in range(T)]

# Objective Function
problem += pulp.lpSum(CoalCost * coal_cap_added[t] + NukeCost * nuke_cap_added[t] for t in range(T)), "Total Cost"

# Constraints

# Demand Satisfaction
for t in range(T):
    coal_life_sum = pulp.lpSum(coal_cap_added[i] for i in range(max(0, t-CoalLife+1), t+1))
    nuke_life_sum = pulp.lpSum(nuke_cap_added[i] for i in range(max(0, t-NukeLife+1), t+1))
    problem += OilCap[t] + coal_life_sum + nuke_life_sum >= Demand[t], f"Demand_Satisfaction_{t}"

# Nuclear Capacity Limit
for t in range(T):
    nuke_life_sum = pulp.lpSum(nuke_cap_added[i] for i in range(max(0, t-NukeLife+1), t+1))
    total_capacity = OilCap[t] + pulp.lpSum(coal_cap_added[i] for i in range(max(0, t-CoalLife+1), t+1)) + nuke_life_sum
    problem += nuke_life_sum <= MaxNuke / 100 * total_capacity, f"Nuclear_Capacity_Limit_{t}"

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')