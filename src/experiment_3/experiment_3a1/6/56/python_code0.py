import pulp
import json

# Data provided in JSON format
data = json.loads('{"west_time": [[3.5, 4.5], [4, 4], [5, 4]], "north_time": [[10, 10, 9], [9, 9, 12]]}')

# Extracting the dimensions and times
west_time = data['west_time']
north_time = data['north_time']
N = len(north_time) + 1  # adding start point
W = len(west_time[0]) + 1  # adding start point

# Create a linear programming problem
problem = pulp.LpProblem("Delivery_Person_Path_Optimization", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(1, N) for w in range(1, W)), cat='Binary')

# Objective Function
problem += pulp.lpSum(north_time[n-1][w-1] * x[(n, w)] + west_time[n-1][w-2] * x[(n-1, w)] 
                      for n in range(1, N) for w in range(2, W)), "Total_Travel_Time"

# Constraints
# Flow Conservation
for n in range(1, N):
    for w in range(1, W):
        problem += (pulp.lpSum(x[(n, w)] for w in range(1, W)) - 
                     pulp.lpSum(x[(n-1, w)] for w in range(1, W)) == 0)

# Start and end points
problem += (x[(1, 1)] == 1, "Start_Point")
problem += (x[(N-1, W-1)] == 1, "End_Point")

# Solve the problem
problem.solve()

# Output the objective value and the paths
paths = [(n, w) for (n, w) in x if x[(n, w)].varValue == 1]

print(f'Paths: {paths}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')