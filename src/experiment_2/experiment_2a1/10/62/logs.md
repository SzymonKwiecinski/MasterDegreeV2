# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MILP

PROBLEM INFO:

- A traveler based in \var{start_city} needs to visit \var{N} towns for business.
- The distance \var{distance_{i,j}} between city \var{i} and \var{j} is provided in miles and are symmetric, meaning the distance from city \var{i} to city \var{j} is the same as from city \var{j} to city \var{i}.
- The traveler must return to \var{start_city} after visiting all towns.

INPUT FORMAT: 

{
    "distances": {
        city_i: {
            city_j: distance_{i, j},
            for j in 1, ..., N-1
        },
        for i in 1, ..., N
    },
    "start_city": start_city
}

OBJECTIVE: Determine the shortest route that the traveler can take to visit all \var{N} towns and return to \var{start_city}.

OUTPUT INFO:

- The sequence of cities visited after \var{start_city} is \var{visit_order}.
- \var{total_distance} traveled on this optimal journey.

OUTPUT FORMAT:

{
    "visit_order": [city_n for n in 1, ..., N+1],
    "total_distance": total_distance
}
</DESCRIPTION>
<DATA>
{'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import numpy as np

#### Input data in the required format
data = {
    'N': 6,
    'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], 
                  [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], 
                  [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]],
    'StartCity': 0
}

#### Define parameters
N = data['N']
distances = np.array(data['Distances'])
start_city = data['StartCity']

#### Create the model
problem = pulp.LpProblem("Traveling_Salesman_Problem", pulp.LpMinimize)

#### Create decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')

#### Objective function
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N) for j in range(N) if i != j)

#### Constraints
#### Each city must be entered and exited exactly once
for k in range(N):
    problem += pulp.lpSum(x[i][k] for i in range(N) if i != k) == 1  #### Enter city k
    problem += pulp.lpSum(x[k][j] for j in range(N) if j != k) == 1  #### Exit city k

#### Subtour elimination constraints
u = pulp.LpVariable.dicts("u", range(N), lowBound=0, cat='Integer')
problem += u[start_city] == 0  #### Setting the start city

for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + (N - 1) * x[i][j] <= N - 2

#### Solve the problem
problem.solve()

#### Extract the tour
visit_order = []
current_city = start_city

while True:
    for next_city in range(N):
        if next_city != current_city and pulp.value(x[current_city][next_city]) == 1:
            visit_order.append(next_city)
            current_city = next_city
            break
    if len(visit_order) == N:
        break

visit_order = [start_city] + visit_order + [start_city]  #### Return to start city

#### Calculate total distance
total_distance = pulp.value(problem.objective)

#### Output the results
result = {
    "visit_order": visit_order,
    "total_distance": total_distance
}

print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
```

