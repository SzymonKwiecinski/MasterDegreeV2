# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO: 

- Consider a school district with \var{N} neighborhoods, \var{S} schools, and \var{G} grades at each school.
- Each school \var{s} has a capacity of \var{capacity_{s,g}} for grade \var{g}. 
- In each neighborhood \var{n}, the student population of grade \var{g} is \var{population_{n,g}}. 
- Finally, the distance of school \var{s} from neighborhood \var{n} is \var{d_{i,j}}.

INPUT FORMAT: 

{
    "capacity": [[capacity_{s,g} for g in 1, ..., G] for s in 1, ..., S],
    "population": [[population_{n,g} for g in 1, ..., G] for n in 1, ..., N],
    "distance": [[d_{n,s} for s in 1, ..., S] for n in 1, ..., N]
}

OBJECTIVE: We want to assign all students to schools, while minimizing the total distance traveled by all students. We may ignore the fact that numbers of students must be integers.

OUTPUT INFO:
- the output should show optimal \var{x_{n,s,g}} for all \var{n}, \var{s}, \var{g} (i.e., the number of students of grade \var{g} in neighborhood \var{n} assigned to school \var{s}).
- the output should also include \var{total_distance}, the total distance traveled by all students.

OUTPUT FORMAT:

{
    "assignment": [[[x_{n,s,g} for g in 1, ..., G] for s in 1, ..., S] for n in 1, ..., N],
    "total_distance": total_distance
}

</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for School Assignment Problem}

\subsection*{Parameters}
\begin{itemize}
    \item Let $N$ be the number of neighborhoods.
    \item Let $S$ be the number of schools.
    \item Let $G$ be the number of grades at each school.
    \item Let $capacity_{s,g}$ be the capacity of school $s$ for grade $g$.
    \item Let $population_{n,g}$ be the student population of neighborhood $n$ for grade $g$.
    \item Let $d_{n,s}$ be the distance of school $s$ from neighborhood $n$.
\end{itemize}

\subsection*{Decision Variables}
Let $x_{n,s,g}$ be the number of students of grade $g$ in neighborhood $n$ assigned to school $s$.

\subsection*{Objective Function}
We want to minimize the total distance traveled by all students:
\[
\text{Minimize } Z = \sum_{n=1}^{N} \sum_{s=1}^{S} \sum_{g=1}^{G} d_{n,s} \cdot x_{n,s,g}
\]

\subsection*{Constraints}
\begin{itemize}
    \item \textbf{Capacity Constraints:} The total number of students assigned to each school for each grade cannot exceed the school's capacity:
    \[
    \sum_{n=1}^{N} x_{n,s,g} \leq capacity_{s,g}, \quad \forall s, g
    \]
    
    \item \textbf{Population Constraints:} All students in each neighborhood for each grade must be assigned to schools:
    \[
    \sum_{s=1}^{S} x_{n,s,g} = population_{n,g}, \quad \forall n, g
    \]

    \item \textbf{Non-negativity Constraints:} The number of students assigned cannot be negative:
    \[
    x_{n,s,g} \geq 0, \quad \forall n, s, g
    \]
\end{itemize}

\subsection*{Output}
We seek to find:
\begin{itemize}
    \item The assignment of students: $x_{n,s,g}$ for all $n$, $s$, and $g$.
    \item The total distance traveled by all students, represented as $\text{total\_distance}$.
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

\section*{Linear Programming Model for School Assignment Problem}

\subsection*{Parameters}
\begin{itemize}
    \item Let $N$ be the number of neighborhoods.
    \item Let $S$ be the number of schools.
    \item Let $G$ be the number of grades at each school.
    \item Let $capacity_{s,g}$ be the capacity of school $s$ for grade $g$.
    \item Let $population_{n,g}$ be the student population of neighborhood $n$ for grade $g$.
    \item Let $d_{n,s}$ be the distance of school $s$ from neighborhood $n$.
\end{itemize}

\subsection*{Decision Variables}
Let $x_{n,s,g}$ be the number of students of grade $g$ in neighborhood $n$ assigned to school $s$.

\subsection*{Objective Function}
We want to minimize the total distance traveled by all students:
\[
\text{Minimize } Z = \sum_{n=1}^{N} \sum_{s=1}^{S} \sum_{g=1}^{G} d_{n,s} \cdot x_{n,s,g}
\]

\subsection*{Constraints}
\begin{itemize}
    \item \textbf{Capacity Constraints:} The total number of students assigned to each school for each grade cannot exceed the school's capacity:
    \[
    \sum_{n=1}^{N} x_{n,s,g} \leq capacity_{s,g}, \quad \forall s, g
    \]
    
    \item \textbf{Population Constraints:} All students in each neighborhood for each grade must be assigned to schools:
    \[
    \sum_{s=1}^{S} x_{n,s,g} = population_{n,g}, \quad \forall n, g
    \]

    \item \textbf{Non-negativity Constraints:} The number of students assigned cannot be negative:
    \[
    x_{n,s,g} \geq 0, \quad \forall n, s, g
    \]
\end{itemize}

\subsection*{Output}
We seek to find:
\begin{itemize}
    \item The assignment of students: $x_{n,s,g}$ for all $n$, $s$, and $g$.
    \item The total distance traveled by all students, represented as $\text{total\_distance}$.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'S': 3, 'G': 2, 'N': 4, 'Capacity': [[15, 20], [20, 15], [5, 17]], 'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Extract data from the JSON format
data = {
    'S': 3,
    'G': 2,
    'N': 4,
    'Capacity': [[15, 20], [20, 15], [5, 17]],
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]],
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

S = data['S']
G = data['G']
N = data['N']
capacity = data['Capacity']
population = data['Population']
distance = data['Distance']

#### Create the linear programming problem
problem = pulp.LpProblem("School_Assignment_Problem", pulp.LpMinimize)

#### Decision variables
x_vars = pulp.LpVariable.dicts("x", 
                               ((n, s, g) for n in range(N) for s in range(S) for g in range(G)), 
                               lowBound=0, cat='Continuous')

#### Objective function
problem += pulp.lpSum(distance[n][s] * x_vars[(n, s, g)] for n in range(N) for s in range(S) for g in range(G))

#### Capacity constraints
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x_vars[(n, s, g)] for n in range(N)) <= capacity[s][g], f"Capacity_Constraint_s{s}_g{g}"

#### Population constraints
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x_vars[(n, s, g)] for s in range(S)) == population[n][g], f"Population_Constraint_n{n}_g{g}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


