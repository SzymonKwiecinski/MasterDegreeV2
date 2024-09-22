import pulp
import json

# Data provided in JSON format
data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}

# Indices
I = len(data['numdepot'])  # Number of depots
J = len(data['numport'])    # Number of ports

# Create the problem variable
problem = pulp.LpProblem("Container_Transportation", pulp.LpMinimize)

# Decision Variables
number = pulp.LpVariable.dicts("number", (range(I), range(J)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum((number[i][j] / 2) * data['price'] * data['distance'][i][j] for i in range(I) for j in range(J)), "Total_Cost"

# Constraints
# Container availability at depots
for i in range(I):
    problem += pulp.lpSum(number[i][j] for j in range(J)) <= data['numdepot'][i], f"Depot_Capacity_{i+1}"

# Container requirement at ports
for j in range(J):
    problem += pulp.lpSum(number[i][j] for i in range(I)) >= data['numport'][j], f"Port_Requirement_{j+1}"

# Solve the problem
problem.solve()

# Output the results
result = {f'number_{i+1}_{j+1}': number[i][j].varValue for i in range(I) for j in range(J)}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')