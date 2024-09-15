# START: OR_ModelCreator 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. You receive task description between <TASK_DESCRIPTION> and </TASK_DESCRIPTION>. You receive target objective between <OBJECTIVE> and </OBJECTIVE>. You receive description of constraints between <CONSTRAINTS> and </CONSTRAINTS>. You receive all 'parameters' which you have to use in model with symbol and shape between <PARAMETERS> and </PARAMETERS>. 
## START MESSAGE 0 
### ROLE: Role.USER
<TASK_DESCRIPTION>: Identifying the shortest route for a traveler to visit a certain number of towns and return to the original starting town.</TASK_DESCRIPTION>.
<OBJECTIVE>: Minimize the total travel distance for the route </OBJECTIVE>
<CONSTRAINTS>
<CONSTRAINT>The traveler must visit each town exactly once</CONSTRAINT>
<CONSTRAINT>The traveler must return to StartCity after visiting all other towns</CONSTRAINT>
<CONSTRAINT>The distance between any two towns is non-negative</CONSTRAINT>
</CONSTRAINTS>
<PARAMETERS>
<PARAMETER>
<DEFINITION>Number of towns to visit</DEFINITION>
<SYMBOL>N</SYMBOL>
<SHAPE>constant</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Index of the start city</DEFINITION>
<SYMBOL>StartCity</SYMBOL>
<SHAPE>constant</SHAPE>
 </PARAMETER>  
<PARAMETER>
<DEFINITION>Distance from city i to city j</DEFINITION>
<SYMBOL>Distances</SYMBOL>
<SHAPE>['N', 'N']</SHAPE>
 </PARAMETER>
</PARAMETERS>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\usepackage{amssymb}

\begin{document}

\section*{Mathematical Model for the Traveling Salesman Problem}

\subsection*{Parameters}
\begin{itemize}
    \item $N$: Number of towns to visit.
    \item $StartCity$: Index of the start city.
    \item $Distances_{ij}$: Distance from city $i$ to city $j$, for $i, j \in \{1, 2, \ldots, N\}$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_{ij}$: Binary variable that is 1 if the route goes directly from city $i$ to city $j$, and 0 otherwise.
    \item $u_i$: Auxiliary variable to eliminate subtours, for $i \in \{1, 2, \ldots, N\}$.
\end{itemize}

\subsection*{Objective Function}
Minimize the total travel distance:
\[
\min \sum_{i=1}^{N} \sum_{j=1}^{N} Distances_{ij} \cdot x_{ij}
\]

\subsection*{Constraints}
\begin{enumerate}
    \item Each town must be visited exactly once:
    \[
    \sum_{j=1, j \neq i}^{N} x_{ij} = 1 \quad \forall i \in \{1, 2, \ldots, N\}
    \]
    \[
    \sum_{i=1, i \neq j}^{N} x_{ij} = 1 \quad \forall j \in \{1, 2, \ldots, N\}
    \]

    \item The traveler must return to the StartCity after visiting all other towns:
    \[
    \sum_{j=1, j \neq StartCity}^{N} x_{StartCity, j} = 1
    \]
    \[
    \sum_{i=1, i \neq StartCity}^{N} x_{i, StartCity} = 1
    \]

    \item Eliminate subtours (Miller-Tucker-Zemlin formulation):
    \[
    u_i - u_j + N \cdot x_{ij} \leq N-1 \quad \forall i, j \in \{2, 3, \ldots, N\}, i \neq j
    \]
    \[
    1 \leq u_i \leq N-1 \quad \forall i \in \{2, 3, \ldots, N\}
    \]

    \item Binary constraints:
    \[
    x_{ij} \in \{0, 1\} \quad \forall i, j \in \{1, 2, \ldots, N\}
    \]
\end{enumerate}

\end{document}
```

# START: PythonProgrammerCreator 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Print at the end the objective between <OBJ></OBJ> Do not include 'pip install' in script. Assume every python package is installed like in this example `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
```latex
\documentclass{article}
\usepackage{amsmath}
\usepackage{amssymb}

\begin{document}

\section*{Mathematical Model for the Traveling Salesman Problem}

\subsection*{Parameters}
\begin{itemize}
    \item $N$: Number of towns to visit.
    \item $StartCity$: Index of the start city.
    \item $Distances_{ij}$: Distance from city $i$ to city $j$, for $i, j \in \{1, 2, \ldots, N\}$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_{ij}$: Binary variable that is 1 if the route goes directly from city $i$ to city $j$, and 0 otherwise.
    \item $u_i$: Auxiliary variable to eliminate subtours, for $i \in \{1, 2, \ldots, N\}$.
\end{itemize}

\subsection*{Objective Function}
Minimize the total travel distance:
\[
\min \sum_{i=1}^{N} \sum_{j=1}^{N} Distances_{ij} \cdot x_{ij}
\]

\subsection*{Constraints}
\begin{enumerate}
    \item Each town must be visited exactly once:
    \[
    \sum_{j=1, j \neq i}^{N} x_{ij} = 1 \quad \forall i \in \{1, 2, \ldots, N\}
    \]
    \[
    \sum_{i=1, i \neq j}^{N} x_{ij} = 1 \quad \forall j \in \{1, 2, \ldots, N\}
    \]

    \item The traveler must return to the StartCity after visiting all other towns:
    \[
    \sum_{j=1, j \neq StartCity}^{N} x_{StartCity, j} = 1
    \]
    \[
    \sum_{i=1, i \neq StartCity}^{N} x_{i, StartCity} = 1
    \]

    \item Eliminate subtours (Miller-Tucker-Zemlin formulation):
    \[
    u_i - u_j + N \cdot x_{ij} \leq N-1 \quad \forall i, j \in \{2, 3, \ldots, N\}, i \neq j
    \]
    \[
    1 \leq u_i \leq N-1 \quad \forall i \in \{2, 3, \ldots, N\}
    \]

    \item Binary constraints:
    \[
    x_{ij} \in \{0, 1\} \quad \forall i, j \in \{1, 2, \ldots, N\}
    \]
\end{enumerate}

\end{document}
```
<DATA>
{'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}
</DATA>

## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data
data = json.loads('{"N": 6, "Distances": [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], "StartCity": 0}')

N = data['N']
Distances = data['Distances']
StartCity = data['StartCity']

#### Create the problem
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')
u = pulp.LpVariable.dicts("u", range(N), lowBound=1, upBound=N-1)

#### Objective Function
problem += pulp.lpSum(Distances[i][j] * x[i][j] for i in range(N) for j in range(N))

#### Constraints
#### Each town must be visited exactly once
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N) if j != i) == 1
    problem += pulp.lpSum(x[j][i] for j in range(N) if j != i) == 1

#### The traveler must return to the StartCity after visiting all other towns
problem += pulp.lpSum(x[StartCity][j] for j in range(N) if j != StartCity) == 1
problem += pulp.lpSum(x[i][StartCity] for i in range(N) if i != StartCity) == 1

#### Eliminate subtours (Miller-Tucker-Zemlin formulation)
for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + N * x[i][j] <= N - 1

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

