import pulp
import json

# Data input
data = json.loads('{"NumTerminals": 3, "NumDestinations": 4, "Cost": [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]], "Demand": [65, 70, 50, 45], "Supply": [150, 100, 100]}')

# Parameters
num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']
cost = data['Cost']
demand = data['Demand']
supply = data['Supply']

# Create problem
problem = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("route", (range(num_terminals), range(num_destinations)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(cost[i][j] * x[i][j] for i in range(num_terminals) for j in range(num_destinations)), "Total_Cost"

# Supply Constraints
for i in range(num_terminals):
    problem += pulp.lpSum(x[i][j] for j in range(num_destinations)) <= supply[i], f"Supply_Constraint_{i}"

# Demand Constraints
for j in range(num_destinations):
    problem += pulp.lpSum(x[i][j] for i in range(num_terminals)) >= demand[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')