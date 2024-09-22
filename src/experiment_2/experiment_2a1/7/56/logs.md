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
import json
import pulp

#### Input data
data = {'west_time': [[3.5, 4.5], [4, 4], [5, 4]], 'north_time': [[10, 10, 9], [9, 9, 12]]}

#### Extracting dimensions and times
west_time = data['west_time']
north_time = data['north_time']

N = len(west_time)  #### Number of streets (rows)
W = len(west_time[0]) + 1  #### Number of avenues (columns)

#### Create a linear programming problem
problem = pulp.LpProblem("DeliveryTimeMinimization", pulp.LpMinimize)

#### Decision variables
time_vars = pulp.LpVariable.dicts("time", (range(N), range(W)), lowBound=0)

#### Objective function: minimize the time to reach the bottom-right corner
problem += time_vars[N-1][W-1], "TotalTime"

#### Constraints for the grid
#### Fill the time for the first row (only can come from the left)
for w in range(W):
    if w == 0:
        time_vars[0][w] = west_time[0][0]  #### Starting point takes the first west_time
    else:
        problem += time_vars[0][w] == time_vars[0][w-1] + west_time[0][w-1]

#### Fill the time for the first column (only can come from above)
for n in range(N):
    if n == 0:
        time_vars[n][0] = 0  #### Starting point has no time
    else:
        problem += time_vars[n][0] == time_vars[n-1][0] + north_time[n-1][0]

#### Fill the rest of the grid
for n in range(1, N):
    for w in range(1, W):
        problem += time_vars[n][w] == pulp.lpSum([time_vars[n-1][w] + north_time[n-1][w], 
                                                    time_vars[n][w-1] + west_time[n][w-1]])

#### Solve the problem
problem.solve()

#### Retrieve total_time and paths
total_time = pulp.value(problem.objective)
paths = []

n, w = N - 1, W - 1

#### Backtracking to find the path
while n > 0 or w > 0:
    paths.append((n + 1, w + 1))  #### Store the path as 1-indexed
    if n == 0:  #### Only can go west
        w -= 1
    elif w == 0:  #### Only can go north
        n -= 1
    else:
        if time_vars[n][w] == time_vars[n - 1][w] + north_time[n - 1][w]:
            n -= 1
        else:
            w -= 1

#### Add the start point
paths.append((1, 1))
paths.reverse()

#### Output the result
result = {
    "paths": paths,
    "total_time": total_time
}

print(result)
print(f' (Objective Value): <OBJ>{total_time}</OBJ>')
```

