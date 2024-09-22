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

#### Extract data from json
west_time = data['west_time']
north_time = data['north_time']
N = len(west_time)  #### Number of streets (rows)
W = len(west_time[0]) + 1  #### Number of avenues (columns)

#### Define the problem
problem = pulp.LpProblem("Delivery_Person_Path", pulp.LpMinimize)

#### Decision Variables
#### x[n][w] = 1 if the person is at intersection (w, n)
x = pulp.LpVariable.dicts("x", (range(N), range(W)), 0, 1, pulp.LpBinary)

#### Objective Function
problem += pulp.lpSum(x[0][0] * 0)  #### Start point has no cost (time)
for n in range(N):
    for w in range(W):
        if w < W - 1:  #### west move
            problem += pulp.lpSum(x[n][w] for n in range(N)) <= pulp.lpSum(x[n][w + 1] * west_time[n][w] for n in range(N))
        if n < N - 1:  #### north move
            problem += pulp.lpSum(x[n][w] for w in range(W)) <= pulp.lpSum(x[n + 1][w] * north_time[n][w] for w in range(W))

#### Constraints
#### Start at (0,0)
problem += x[0][0] == 1
#### End at (N-1, W-1)
problem += pulp.lpSum(x[N-1][W-1]) == 1

#### Solve the problem
problem.solve()

#### Extract the paths taken
paths = []
for n in range(N):
    for w in range(W):
        if x[n][w].value() == 1:
            paths.append((n+1, w+1))

#### Calculate total time taken
total_time = pulp.value(problem.objective)

#### Output the results
output = {
    "paths": paths,
    "total_time": total_time
}

print(output)
print(f' (Objective Value): <OBJ>{total_time}</OBJ>')
```

