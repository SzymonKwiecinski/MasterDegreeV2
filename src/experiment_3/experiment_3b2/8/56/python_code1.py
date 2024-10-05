import pulp
import json

# Given data in JSON format
data = '{"west_time": [[3.5, 4.5], [4, 4], [5, 4]], "north_time": [[10, 10, 9], [9, 9, 12]]}'
data_dict = json.loads(data)

# Parameters
west_time = data_dict['west_time']  # Time to move west
north_time = data_dict['north_time']  # Time to move north

N = len(north_time) + 1  # Number of Streets (including start)
W = len(west_time[0]) + 1  # Number of Avenues (including start)
m = 1  # Number of moves (can be adjusted if needed)

# Create the LP problem
problem = pulp.LpProblem("Minimize_Total_Travel_Time", pulp.LpMinimize)

# Decision variables
x_west = pulp.LpVariable.dicts("x_west", (range(N), range(W-1)), cat=pulp.LpBinary)
x_north = pulp.LpVariable.dicts("x_north", (range(N-1), range(W)), cat=pulp.LpBinary)

# Objective function
problem += (
    pulp.lpSum(west_time[n][w] * x_west[n][w] for n in range(N) for w in range(W-1)) +
    pulp.lpSum(north_time[n][w] * x_north[n][w] for n in range(N-1) for w in range(W))
)

# Constraints
# Constraint 1
problem += (pulp.lpSum(x_west[0][w] for w in range(W-1)) + 
             pulp.lpSum(x_north[n][0] for n in range(N-1)) == m)

# Constraint 2
problem += (pulp.lpSum(x_west[N-1][w] for w in range(W-1)) + 
             pulp.lpSum(x_north[N-2][w] for w in range(W)) == m)

# Constraint 3
for n in range(N - 1):  # Adjusted range to avoid KeyError
    problem += (pulp.lpSum(x_west[n][w] for w in range(W-1)) + 
                 pulp.lpSum(x_north[n][0] for n in range(N-1)) <= 1)

# Constraint 4
for w in range(W):  
    problem += (pulp.lpSum(x_north[n][w] for n in range(N-1)) + 
                 x_west[0][w] <= 1)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')