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
N = len(data['north_time']) + 1  #### number of north streets
W = len(data['west_time'][0]) + 1  #### number of west avenues

#### Create a linear programming problem
problem = pulp.LpProblem("Minimize_Delivery_Time", pulp.LpMinimize)

#### Decision Variables
#### x[n][w] = time taken to reach the intersection of (street n, avenue w)
x = pulp.LpVariable.dicts("x", ((n, w) for n in range(1, N + 1) for w in range(1, W + 1)), lowBound=0)

#### Objective Function
#### The time to reach the last intersection (N, W) is the objective
problem += x[N, W], "Total_Time"

#### Constraints
#### Initialize the first intersection
problem += x[1, 1] == 0, "Start_Point"

#### Fill constraints for moving north and west
for n in range(1, N + 1):
    for w in range(1, W + 1):
        if n > 1:  #### can move north
            problem += x[n, w] >= x[n - 1, w] + data['north_time'][n - 2][w - 1], f"North_Move_{n}_{w}"
        if w > 1:  #### can move west
            problem += x[n, w] >= x[n, w - 1] + data['west_time'][n - 1][w - 2], f"West_Move_{n}_{w}"

#### Solve the problem
problem.solve()

#### Collecting paths
paths = []
current_n, current_w = N, W

while current_n > 1 or current_w > 1:
    if current_n > 1 and (current_w == 1 or x[current_n, current_w].value() == x[current_n - 1, current_w].value() + data['north_time'][current_n - 2][current_w - 1]):
        paths.append((current_n - 1, current_w))
        current_n -= 1
    else:
        paths.append((current_n, current_w - 1))
        current_w -= 1

#### Since we built the path backwards, reverse it
paths.reverse()

#### Output the results
total_time = pulp.value(problem.objective)
output = {
    "paths": paths,
    "total_time": total_time
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_time}</OBJ>')
```

