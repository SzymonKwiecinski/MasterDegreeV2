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

\section*{Mathematical Model for the Traveling Salesman Problem (TSP)}

\subsection*{Sets}
\begin{itemize}
    \item $C$: Set of cities, where $C = \{0, 1, 2, \ldots, N\}$.
    \item $N$: Total number of towns to visit.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $distance_{i,j}$: Distance between city $i$ and city $j$.
    \item $start\_city$: The starting city of the traveler (denoted as city 0).
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item $x_{i,j}$: Binary variable, where $x_{i,j} = 1$ if the traveler travels directly from city $i$ to city $j$, and $0$ otherwise.
    \end{itemize}

\subsection*{Objective Function}
Minimize the total distance:
\[
\text{Minimize} \quad Z = \sum_{i \in C} \sum_{j \in C} distance_{i,j} \cdot x_{i,j}
\]

\subsection*{Constraints}
\begin{itemize}
    \item Each city must be entered and exited exactly once:
    \[
    \sum_{j \in C} x_{i,j} = 1, \quad \forall i \in C \setminus \{0\}
    \]
    \[
    \sum_{i \in C} x_{i,j} = 1, \quad \forall j \in C \setminus \{0\}
    \]

    \item Subtour elimination (Miller-Tucker-Zemlin formulation):
    \[
    u_i - u_j + N \cdot x_{i,j} \leq N-1, \quad \forall i,j \in C \setminus \{0\}, i \neq j
    \]
    where $u_i$ is the number of cities visited before city $i$.
    
    \item Binary constraints:
    \[
    x_{i,j} \in \{0, 1\}, \quad \forall i,j \in C
    \]
\end{itemize}

\subsection*{Output}
The output will provide:
\begin{itemize}
    \item $visit\_order$: The sequence of cities visited after $start\_city$.
    \item $total\_distance$: The total distance traveled on the optimal journey.
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

\section*{Mathematical Model for the Traveling Salesman Problem (TSP)}

\subsection*{Sets}
\begin{itemize}
    \item $C$: Set of cities, where $C = \{0, 1, 2, \ldots, N\}$.
    \item $N$: Total number of towns to visit.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $distance_{i,j}$: Distance between city $i$ and city $j$.
    \item $start\_city$: The starting city of the traveler (denoted as city 0).
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item $x_{i,j}$: Binary variable, where $x_{i,j} = 1$ if the traveler travels directly from city $i$ to city $j$, and $0$ otherwise.
    \end{itemize}

\subsection*{Objective Function}
Minimize the total distance:
\[
\text{Minimize} \quad Z = \sum_{i \in C} \sum_{j \in C} distance_{i,j} \cdot x_{i,j}
\]

\subsection*{Constraints}
\begin{itemize}
    \item Each city must be entered and exited exactly once:
    \[
    \sum_{j \in C} x_{i,j} = 1, \quad \forall i \in C \setminus \{0\}
    \]
    \[
    \sum_{i \in C} x_{i,j} = 1, \quad \forall j \in C \setminus \{0\}
    \]

    \item Subtour elimination (Miller-Tucker-Zemlin formulation):
    \[
    u_i - u_j + N \cdot x_{i,j} \leq N-1, \quad \forall i,j \in C \setminus \{0\}, i \neq j
    \]
    where $u_i$ is the number of cities visited before city $i$.
    
    \item Binary constraints:
    \[
    x_{i,j} \in \{0, 1\}, \quad \forall i,j \in C
    \]
\end{itemize}

\subsection*{Output}
The output will provide:
\begin{itemize}
    \item $visit\_order$: The sequence of cities visited after $start\_city$.
    \item $total\_distance$: The total distance traveled on the optimal journey.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267],
                              [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484],
                              [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 
        'StartCity': 0}

#### Extract values from data
N = data['N']
Distances = data['Distances']
start_city = data['StartCity']

#### Create the problem instance
problem = pulp.LpProblem("Traveling_Salesman_Problem", pulp.LpMinimize)

#### Define sets
C = list(range(N + 1))

#### Define variables
x = pulp.LpVariable.dicts("x", (C, C), 0, 1, pulp.LpBinary)
u = pulp.LpVariable.dicts("u", C[1:], 0, N-1)

#### Objective function
problem += pulp.lpSum(Distances[i][j] * x[i][j] for i in C for j in C), "Total_Distance"

#### Constraints
#### Each city must be entered and exited exactly once (except the starting city)
for i in C[1:]:
    problem += pulp.lpSum(x[i][j] for j in C) == 1, f"Exit_City_{i}"
    problem += pulp.lpSum(x[j][i] for j in C) == 1, f"Enter_City_{i}"

#### Subtour elimination constraints
for i in C[1:]:
    for j in C[1:]:
        if i != j:
            problem += u[i] - u[j] + N * x[i][j] <= N - 1, f"Subtour_Elimination_{i}_{j}"

#### Solve the problem
problem.solve()

#### Extract the visit order
visit_order = []
for i in C:
    for j in C:
        if pulp.value(x[i][j]) == 1 and i == start_city:
            visit_order.append(j)

#### Calculate total distance
total_distance = pulp.value(problem.objective)

#### Output results
print(f'Visit Order: {visit_order}')
print(f'Total Distance: {total_distance}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

