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

#### Parse the input data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}
west_time = data['west_time']
north_time = data['north_time']

#### Grid dimensions
N = len(north_time) + 1  #### Number of streets
W = len(west_time[0]) + 1  #### Number of avenues

#### Create the LP problem
problem = pulp.LpProblem("Minimize_Walking_Time", pulp.LpMinimize)

#### Decision variables
xwest = pulp.LpVariable.dicts("xwest", ((n, w) for n in range(1, N+1) for w in range(1, W)), cat='Binary')
xnorth = pulp.LpVariable.dicts("xnorth", ((n, w) for n in range(1, N) for w in range(1, W+1)), cat='Binary')

#### Objective function
problem += (
    pulp.lpSum(west_time[n-1][w-1] * xwest[n, w] for n in range(1, N+1) for w in range(1, W) if w < W) +
    pulp.lpSum(north_time[n-1][w-1] * xnorth[n, w] for n in range(1, N) for w in range(1, W+1) if n < N)
), "Total Travel Time"

#### Flow constraints
for n in range(1, N+1):
    for w in range(1, W+1):
        incoming_flow = (
            xwest[n, w-1] if w > 1 else 0
        ) + (
            xnorth[n-1, w] if n > 1 else 0
        )
        outgoing_flow = (
            xwest[n, w] if w < W else 0
        ) + (
            xnorth[n, w] if n < N else 0
        )
        if n == 1 and w == 1:
            problem += outgoing_flow == 1, f"Start at intersection ({n},{w})"
        elif n == N and w == W:
            problem += incoming_flow == 1, f"End at intersection ({n},{w})"
        else:
            problem += incoming_flow == outgoing_flow, f"Flow conservation at ({n},{w})"

#### Solve the problem
problem.solve()

#### Extract solution
paths = []
for n in range(1, N+1):
    for w in range(1, W):
        if pulp.value(xwest[n, w]) == 1:
            paths.append((n, w))
for n in range(1, N):
    for w in range(1, W+1):
        if pulp.value(xnorth[n, w]) == 1:
            paths.append((n, w))

total_time = pulp.value(problem.objective)

#### Output format
output = {
    "paths": paths,
    "total_time": total_time
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

