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

\textbf{Sets:}
\begin{itemize}
    \item $N$: Set of neighborhoods
    \item $S$: Set of schools
    \item $G$: Set of grades
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $capacity_{s,g}$: Capacity of school $s$ for grade $g$
    \item $population_{n,g}$: Student population in neighborhood $n$ for grade $g$
    \item $d_{n,s}$: Distance from neighborhood $n$ to school $s$
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $x_{n,s,g}$: Number of students of grade $g$ in neighborhood $n$ assigned to school $s$
\end{itemize}

\textbf{Objective Function:}
\begin{equation}
    \text{Minimize } Z = \sum_{n \in N} \sum_{s \in S} \sum_{g \in G} d_{n,s} \cdot x_{n,s,g}
\end{equation}

\textbf{Subject to Constraints:}

1. Capacity Constraints for Schools:
\begin{equation}
    \sum_{n \in N} x_{n,s,g} \leq capacity_{s,g} \quad \forall s \in S, \forall g \in G
\end{equation}

2. Student Population Constraints:
\begin{equation}
    \sum_{s \in S} x_{n,s,g} = population_{n,g} \quad \forall n \in N, \forall g \in G
\end{equation}

3. Non-negativity Constraints:
\begin{equation}
    x_{n,s,g} \geq 0 \quad \forall n \in N, \forall s \in S, \forall g \in G
\end{equation}

\textbf{Output:}
The solution will provide:
\begin{itemize}
    \item Optimized assignment $x_{n,s,g}$ for all $n$, $s$, and $g$
    \item Total distance traveled by all students: $total\_distance = Z$
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

\textbf{Sets:}
\begin{itemize}
    \item $N$: Set of neighborhoods
    \item $S$: Set of schools
    \item $G$: Set of grades
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $capacity_{s,g}$: Capacity of school $s$ for grade $g$
    \item $population_{n,g}$: Student population in neighborhood $n$ for grade $g$
    \item $d_{n,s}$: Distance from neighborhood $n$ to school $s$
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $x_{n,s,g}$: Number of students of grade $g$ in neighborhood $n$ assigned to school $s$
\end{itemize}

\textbf{Objective Function:}
\begin{equation}
    \text{Minimize } Z = \sum_{n \in N} \sum_{s \in S} \sum_{g \in G} d_{n,s} \cdot x_{n,s,g}
\end{equation}

\textbf{Subject to Constraints:}

1. Capacity Constraints for Schools:
\begin{equation}
    \sum_{n \in N} x_{n,s,g} \leq capacity_{s,g} \quad \forall s \in S, \forall g \in G
\end{equation}

2. Student Population Constraints:
\begin{equation}
    \sum_{s \in S} x_{n,s,g} = population_{n,g} \quad \forall n \in N, \forall g \in G
\end{equation}

3. Non-negativity Constraints:
\begin{equation}
    x_{n,s,g} \geq 0 \quad \forall n \in N, \forall s \in S, \forall g \in G
\end{equation}

\textbf{Output:}
The solution will provide:
\begin{itemize}
    \item Optimized assignment $x_{n,s,g}$ for all $n$, $s$, and $g$
    \item Total distance traveled by all students: $total\_distance = Z$
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'S': 3, 'G': 2, 'N': 4, 'Capacity': [[15, 20], [20, 15], [5, 17]], 'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'S': 3,
    'G': 2,
    'N': 4,
    'Capacity': [[15, 20], [20, 15], [5, 17]],
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]],
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

#### Indices
S = range(data['S'])
G = range(data['G'])
N = range(data['N'])

#### Model
problem = pulp.LpProblem("School_Assignment_Problem", pulp.LpMinimize)

#### Decision Variables
x = [[[pulp.LpVariable(f"x_{n}_{s}_{g}", lowBound=0, cat='Continuous') for g in G] for s in S] for n in N]

#### Objective Function
problem += pulp.lpSum(data['Distance'][n][s] * x[n][s][g] for n in N for s in S for g in G)

#### Subject to Constraints

#### Capacity Constraints
for s in S:
    for g in G:
        problem += pulp.lpSum(x[n][s][g] for n in N) <= data['Capacity'][s][g]

#### Student Population Constraints
for n in N:
    for g in G:
        problem += pulp.lpSum(x[n][s][g] for s in S) == data['Population'][n][g]

#### Solve the problem
problem.solve()

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

