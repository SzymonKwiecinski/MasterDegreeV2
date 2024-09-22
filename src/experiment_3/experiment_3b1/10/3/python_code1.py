import pulp
import json

# Load data from the given JSON format
data = json.loads("""{"T": 12, "Demand": [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], "OilCap": [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], "CoalCost": 10, "NukeCost": 5, "MaxNuke": 20, "CoalLife": 5, "NukeLife": 10}""")

# Extract data
T = data['T']
demand = data['Demand']
oil_capacity = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100  # convert percentage to fraction
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Define the problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Define decision variables
coal_vars = pulp.LpVariable.dicts("Coal", range(1, T + 1), lowBound=0, cat='Continuous')
nuke_vars = pulp.LpVariable.dicts("Nuke", range(1, T + 1), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(coal_cost * coal_vars[t] + nuke_cost * nuke_vars[t] for t in range(1, T + 1)), "Total_Cost"

# Constraints
# 1. Capacity must meet demand
for t in range(1, T + 1):
    C_t = oil_capacity[t - 1] + pulp.lpSum(coal_vars[j] for j in range(1, t + 1)) + pulp.lpSum(nuke_vars[k] for k in range(1, t + 1))
    problem += C_t >= demand[t - 1], f"Demand_Constraint_{t}"

# 2. Nuclear capacity constraint
for t in range(1, T + 1):
    C_t = oil_capacity[t - 1] + pulp.lpSum(coal_vars[j] for j in range(1, t + 1)) + pulp.lpSum(nuke_vars[k] for k in range(1, t + 1))
    problem += nuke_vars[t] <= max_nuke * C_t, f"Nuke_Capacity_Constraint_{t}"

# 3. Lifetime constraints for coal
for t in range(1, coal_life + 1):  # Changed to coal_life + 1
    problem += coal_vars[t] == 0, f"Coal_Lifetime_Constraint_{t}"

# 4. Lifetime constraints for nuclear
for t in range(1, nuke_life + 1):  # Changed to nuke_life + 1
    problem += nuke_vars[t] == 0, f"Nuke_Lifetime_Constraint_{t}"

# Solve the problem
problem.solve()

# Gather results
coal_cap_added = [coal_vars[t].varValue for t in range(1, T + 1)]
nuke_cap_added = [nuke_vars[t].varValue for t in range(1, T + 1)]
total_cost = pulp.value(problem.objective)

# Print the objective value
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')