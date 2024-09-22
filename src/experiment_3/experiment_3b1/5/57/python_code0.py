import pulp
import json

# Data
data = '''{
    "T": 4,
    "Demands": [450, 700, 500, 750],
    "UnloadCosts": [75, 100, 105, 130],
    "UnloadCapacity": [800, 500, 450, 700],
    "HoldingCost": 20,
    "MaxContainer": 500,
    "InitContainer": 200,
    "NumCranes": 4,
    "CraneCapacity": 200,
    "CraneCost": 1000
}'''
data = json.loads(data)

# Problem Definition
problem = pulp.LpProblem("Seaport_Container_Management", pulp.LpMinimize)

# Decision Variables
t = list(range(1, data["T"] + 1))
amount = pulp.LpVariable.dicts("amount", t, lowBound=0, cat='Continuous')
crane = pulp.LpVariable.dicts("crane", t, lowBound=0, cat='Integer')
containers = pulp.LpVariable.dicts("containers", t, lowBound=0, cat='Continuous')

# Objective Function
total_cost = pulp.lpSum(data["UnloadCosts"][i-1] * amount[i] + 
                         data["HoldingCost"] * containers[i] + 
                         data["CraneCost"] * crane[i] for i in t)
problem += total_cost

# Constraints
problem += containers[1] == data["InitContainer"]

for i in t[1:]:
    problem += containers[i-1] + amount[i] - data["Demands"][i-1] == containers[i], f"Balance_Constraint_{i}"

for i in t:
    problem += amount[i] <= data["UnloadCapacity"][i-1], f"Unload_Capacity_Constraint_{i}"
    problem += amount[i] <= containers[i-1], f"Container_Availability_Constraint_{i}"
    problem += containers[i] <= data["MaxContainer"], f"Max_Container_Constraint_{i}"
    problem += crane[i] * data["CraneCapacity"] >= data["Demands"][i-1], f"Crane_Capacity_Constraint_{i}"
    problem += crane[i] <= data["NumCranes"], f"Max_Cranes_Constraint_{i}"

problem += containers[data["T"]] == 0, "Final_Container_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')