# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
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


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Sets}
\begin{itemize}
    \item Let \( C = \{ 1, 2, \ldots, N \} \) be the set of towns.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{distance}_{i,j} \): Distance between town \( i \) and town \( j \).
    \item \( \text{start\_city} \): The starting town for the traveler.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_{i,j} \): Binary variable that is 1 if the traveler travels directly from town \( i \) to town \( j \), and 0 otherwise.
\end{itemize}

\subsection*{Objective Function}
The objective is to minimize the total distance traveled:
\[
\text{minimize } Z = \sum_{i \in C} \sum_{j \in C} \text{distance}_{i,j} \cdot x_{i,j}
\]

\subsection*{Constraints}
\begin{align*}
1. & \quad \sum_{j \in C} x_{\text{start\_city},j} = 1 \quad \text{(from start city to one town)} \\
2. & \quad \sum_{j \in C} x_{j,\text{start\_city}} = 1 \quad \text{(return to start city)} \\
3. & \quad \sum_{j \in C} x_{i,j} = 1 \quad \forall i \in C \setminus \{\text{start\_city}\} \\
4. & \quad \sum_{i \in C} x_{i,j} = 1 \quad \forall j \in C \setminus \{\text{start\_city}\} \\
5. & \quad x_{i,j} \in \{0, 1\} \quad \forall i,j \in C
\end{align*}

\subsection*{Output}
The output will be structured as follows:
\begin{itemize}
    \item \texttt{visit\_order}: The sequence of cities visited after \texttt{start\_city}.
    \item \texttt{total\_distance}: The total distance traveled on the optimal journey.
\end{itemize}

\end{document}
```

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Sets}
\begin{itemize}
    \item Let \( C = \{ 1, 2, \ldots, N \} \) be the set of towns.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{distance}_{i,j} \): Distance between town \( i \) and town \( j \).
    \item \( \text{start\_city} \): The starting town for the traveler.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_{i,j} \): Binary variable that is 1 if the traveler travels directly from town \( i \) to town \( j \), and 0 otherwise.
\end{itemize}

\subsection*{Objective Function}
The objective is to minimize the total distance traveled:
\[
\text{minimize } Z = \sum_{i \in C} \sum_{j \in C} \text{distance}_{i,j} \cdot x_{i,j}
\]

\subsection*{Constraints}
\begin{align*}
1. & \quad \sum_{j \in C} x_{\text{start\_city},j} = 1 \quad \text{(from start city to one town)} \\
2. & \quad \sum_{j \in C} x_{j,\text{start\_city}} = 1 \quad \text{(return to start city)} \\
3. & \quad \sum_{j \in C} x_{i,j} = 1 \quad \forall i \in C \setminus \{\text{start\_city}\} \\
4. & \quad \sum_{i \in C} x_{i,j} = 1 \quad \forall j \in C \setminus \{\text{start\_city}\} \\
5. & \quad x_{i,j} \in \{0, 1\} \quad \forall i,j \in C
\end{align*}

\subsection*{Output}
The output will be structured as follows:
\begin{itemize}
    \item \texttt{visit\_order}: The sequence of cities visited after \texttt{start\_city}.
    \item \texttt{total\_distance}: The total distance traveled on the optimal journey.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'N': 6,
    'Distances': [
        [0, 182, 70, 399, 56, 214],
        [182, 0, 255, 229, 132, 267],
        [70, 255, 0, 472, 127, 287],
        [399, 229, 472, 0, 356, 484],
        [56, 132, 127, 356, 0, 179],
        [214, 267, 287, 484, 179, 0]
    ],
    'StartCity': 0
}

#### Initialize problem
problem = pulp.LpProblem("Traveling_Salesman_Problem", pulp.LpMinimize)

#### Sets and Parameters
N = data['N']
distances = data['Distances']
start_city = data['StartCity']
cities = list(range(N))

#### Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in cities for j in cities), cat="Binary")

#### Objective Function
problem += pulp.lpSum(distances[i][j] * x[i, j] for i in cities for j in cities), "Total Distance"

#### Constraints
#### 1. From start city to one town
problem += pulp.lpSum(x[start_city, j] for j in cities) == 1

#### 2. Return to start city
problem += pulp.lpSum(x[j, start_city] for j in cities) == 1

#### 3. Each town is visited exactly once
for i in cities:
    if i != start_city:
        problem += pulp.lpSum(x[i, j] for j in cities) == 1

#### 4. Each town is left exactly once
for j in cities:
    if j != start_city:
        problem += pulp.lpSum(x[i, j] for i in cities) == 1

#### Solve the problem
problem.solve()

#### Output Results
visit_order = []
current_city = start_city
visited = set()
visited.add(current_city)

for _ in range(N-1):
    for j in cities:
        if j not in visited and pulp.value(x[current_city, j]) == 1:
            visit_order.append(j)
            visited.add(j)
            current_city = j
            break

total_distance = pulp.value(problem.objective)

#### Print Objective
print(f'(Objective Value): <OBJ>{total_distance}</OBJ>')
```


