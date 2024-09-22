# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO:

- A delivery person starts at the intersection of \var{1}th Avenue and \var{1}th Street and needs to reach the intersection of \var{W}th Avenue and \var{N}th Street.
- The path between these two points forms a \var{N-1} × \var{W-1} grid.
- Each block on the grid has a unique walking time due to varying pedestrian traffic during rush hour.
- The delivery person can only walk north or west.
- The journey can be broken down into \var{m} stages, where at each stage the delivery person decides to walk either north or west.
- When at the intersection of \var{w}th Avenue and \var{n}th Street, the time to move to the intersection of \var{w+1}th Avenue and \var{n}th Stree is \var{west_time_{n,w}}.
- When at the intersection of \var{w}th Avenue and \var{n}th Street, the time to move to the intersection of \var{w}th Avenue and \var{n+1}th Stree is \var{north_time_{n,w}}.

INPUT FORMAT:

{
    "west_time": [[west_{n,w} for w in 1, ..., W-1] for n in 1, ..., N],
    "north_time": [[north_{n,w} for w in 1, ..., W] for n in 1, ..., N-1],
}

OBJECTIVE: Determine the optimal path the delivery person should take to ensure the package is delivered in the least amount of time.

OUTPUT INFO:

- \var{total_time} represents total time taken to travel this path
- \var{paths} represents the flow going through the corresponding path

OUTPUT FORMAT:

{
    "paths": [(street_{n}, avenue_{w}) for id in 1, ..., m]
    "total_time": total_travel_time
}
</DESCRIPTION>
<DATA>
{'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

W = len(data['west_time'][0]) + 1  #### Number of avenues
N = len(data['north_time']) + 1     #### Number of streets

#### Create the LP problem
problem = pulp.LpProblem("Delivery_Time_Minimization", pulp.LpMinimize)

#### Decision variables
#### Use dictionaries to store the variables for the paths
north_vars = pulp.LpVariable.dicts("North", ((n, w) for n in range(N - 1) for w in range(W)), cat='Binary')
west_vars = pulp.LpVariable.dicts("West", ((n, w) for n in range(N) for w in range(W - 1)), cat='Binary')

#### Objective function: Minimizing total time
total_time = pulp.lpSum(north_vars[n, w] * data['north_time'][n][w] for n in range(N - 1) for w in range(W)) + \
             pulp.lpSum(west_vars[n, w] * data['west_time'][n][w] for n in range(N) for w in range(W - 1))

problem += total_time

#### Constraints to ensure one decision at each intersection
for n in range(N):
    for w in range(W):
        if n < N - 1 and w < W - 1:
            problem += (north_vars[n, w] + west_vars[n, w] == 1, f"Stage_{n}_{w}")

#### Ensure to start at (0,0) and end at (N-1, W-1)
problem += (pulp.lpSum(west_vars[0, w] for w in range(W - 1)) == 1, "Start_Condition")
problem += (pulp.lpSum(north_vars[n, 0] for n in range(N - 1)) == 1, "Start_Condition_North")

#### Solve the problem
problem.solve()

#### Collect the paths taken
paths = []
for n in range(N - 1):
    for w in range(W):
        if north_vars[n, w].varValue > 0:
            paths.append((n + 2, w + 1))  #### +2 and +1 to adjust for 1-based indexing
for n in range(N):
    for w in range(W - 1):
        if west_vars[n, w].varValue > 0:
            paths.append((n + 1, w + 2))  #### +1 and +2 to adjust for 1-based indexing

#### Total travel time
total_travel_time = pulp.value(problem.objective)

#### Output the results
output = {
    "paths": paths,
    "total_time": total_travel_time
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

