import pulp

# Data from JSON
data = {
    'T': 12,
    'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35],
    'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5],
    'CoalCost': 10,
    'NukeCost': 5,
    'MaxNuke': 20,
    'CoalLife': 5,
    'NukeLife': 10
}

# Extracting data
T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Define the problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision Variables
coal_added = pulp.LpVariable.dicts("Coal_Added", range(T), lowBound=0)
nuke_added = pulp.LpVariable.dicts("Nuke_Added", range(T), lowBound=0)

# Objective Function
problem += pulp.lpSum(coal_cost * coal_added[t] + nuke_cost * nuke_added[t] for t in range(T)), "Total Cost"

# Constraints

# Demand constraints
for t in range(T):
    problem += (
        oil_cap[t] + pulp.lpSum(coal_added[t_] for t_ in range(t+1)) + pulp.lpSum(nuke_added[t_] for t_ in range(t+1)) 
        >= demand[t], 
        f"Demand_Constraint_{t}"
    )

# Nuclear capacity percentage constraint
problem += (
    pulp.lpSum(nuke_added[t] for t in range(T)) 
    <= (max_nuke / 100) * (pulp.lpSum(oil_cap[t] for t in range(T)) + pulp.lpSum(coal_added[t] for t in range(T)) + pulp.lpSum(nuke_added[t] for t in range(T))), 
    "Max_Nuclear_Capacity_Constraint"
)

# Solve the problem
problem.solve()

# Extracting results
coal_cap_added = [coal_added[t].varValue for t in range(T)]
nuke_cap_added = [nuke_added[t].varValue for t in range(T)]
total_cost = pulp.value(problem.objective)

# Print outputs
print("Coal Capacity Added Each Year:", coal_cap_added)
print("Nuclear Capacity Added Each Year:", nuke_cap_added)
print("Total Cost:", total_cost)

print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')