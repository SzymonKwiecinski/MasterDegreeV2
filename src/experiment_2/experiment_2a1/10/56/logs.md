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

#### Extracting dimensions
N = len(data['west_time'])  #### number of north streets
W = len(data['west_time'][0]) + 1  #### number of avenues (W-1 blocks in west_time)
M = N + W - 2  #### total moves required (N-1 north and W-1 west)

#### Create the LP problem
problem = pulp.LpProblem("Delivery_Optimization", pulp.LpMinimize)

#### Decision variables for the path taken (n, w)
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(N) for w in range(W)), cat='Binary')

#### Objective function: minimize the total time
total_time = pulp.lpSum(x[n, w] * (data['north_time'][n][w] if n < N-1 else 0) +
                        x[n, w] * (data['west_time'][n][w-1] if w > 0 else 0) 
                        for n in range(N) for w in range(W))
problem += total_time

#### Constraints
#### Starting point
problem += x[0, 0] == 1  #### Start at (0, 0)

#### End point
problem += pulp.lpSum(x[N-1, w] for w in range(W)) == 1  #### End at the last row
problem += pulp.lpSum(x[n, W-1] for n in range(N)) == 1  #### End at the last column

#### Induction constraints for movement
for n in range(N):
    for w in range(W):
        if n < N - 1:
            problem += x[n, w] <= pulp.lpSum(x[n + 1, w]), "North_Constraint_%d_%d" % (n, w)
        if w > 0:
            problem += x[n, w] <= pulp.lpSum(x[n, w - 1]), "West_Constraint_%d_%d" % (n, w)

#### Solve the problem
problem.solve()

#### Extracting the paths and total time
paths = [(n + 1, w + 1) for n in range(N) for w in range(W) if pulp.value(x[n, w]) == 1]
total_travel_time = pulp.value(problem.objective)

#### Output in the required format
output = {
    "paths": paths,
    "total_time": total_travel_time
}

#### Print required objective value
print(f' (Objective Value): <OBJ>{total_travel_time}</OBJ>')
```

