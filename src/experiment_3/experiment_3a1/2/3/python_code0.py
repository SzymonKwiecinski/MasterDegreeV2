import pulp
import json

# Load data
data = json.loads('{"T": 12, "Demand": [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], "OilCap": [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], "CoalCost": 10, "NukeCost": 5, "MaxNuke": 20, "CoalLife": 5, "NukeLife": 10}')
T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create the problem
problem = pulp.LpProblem("Electricity_Capacity_Planning", pulp.LpMinimize)

# Variables
coal = pulp.LpVariable.dicts("coal", range(T), lowBound=0, cat='Continuous')
nuke = pulp.LpVariable.dicts("nuke", range(T), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(coal_cost * coal[t] + nuke_cost * nuke[t] for t in range(T)), "Total_Cost"

# Constraints
# Capacity must meet demand
for t in range(T):
    problem += (
        oil_cap[t] + 
        pulp.lpSum(coal[s] for s in range(max(0, t - coal_life + 1), t + 1)) + 
        pulp.lpSum(nuke[s] for s in range(max(0, t - nuke_life + 1), t + 1)) 
        >= demand[t], 
        f"Demand_Constraint_{t}"
    )

# Nuclear capacity constraint
problem += (
    pulp.lpSum(nuke[t] for t in range(T)) 
    <= (max_nuke / 100) * (pulp.lpSum(oil_cap[t] for t in range(T)) + 
    pulp.lpSum(coal[t] for t in range(T)) + 
    pulp.lpSum(nuke[t] for t in range(T))), 
    "Nuclear_Capacity_Constraint"
)

# Non-negativity constraints already included in variable definitions

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')