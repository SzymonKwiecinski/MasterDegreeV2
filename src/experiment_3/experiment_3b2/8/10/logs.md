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
To tackle this linear programming problem, we will create a mathematical model to minimize the total distance traveled by students from their neighborhoods to schools, while respecting the capacity constraints of each school for every grade. The following is the mathematical model expressed in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for School Assignment Problem}

\subsection*{Sets and Indices}
\begin{align*}
N & : \text{Number of neighborhoods} \\
S & : \text{Number of schools} \\
G & : \text{Number of grades}
\end{align*}

Let:
\begin{itemize}
    \item $n = 1, \ldots, N$: Index for neighborhoods
    \item $s = 1, \ldots, S$: Index for schools
    \item $g = 1, \ldots, G$: Index for grades
\end{itemize}

\subsection*{Parameters}
\begin{align*}
capacity_{s,g} & : \text{Capacity of school } s \text{ for grade } g \\
population_{n,g} & : \text{Population of grade } g \text{ in neighborhood } n \\
d_{n,s} & : \text{Distance from neighborhood } n \text{ to school } s
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
x_{n,s,g} & : \text{Number of students of grade } g \text{ in neighborhood } n \text{ assigned to school } s
\end{align*}

\subsection*{Objective Function}
Minimize the total distance traveled by all students:
\[
\text{Minimize } \sum_{n=1}^{N} \sum_{s=1}^{S} \sum_{g=1}^{G} d_{n,s} \cdot x_{n,s,g}
\]

\subsection*{Constraints}
\begin{enumerate}
    \item \text{Capacity constraints for each school and grade:}
    \[
    \sum_{n=1}^{N} x_{n,s,g} \leq capacity_{s,g}, \quad \forall s = 1, \ldots, S, \; \forall g = 1, \ldots, G
    \]
    
    \item \text{Population constraints for each neighborhood and grade:}
    \[
    \sum_{s=1}^{S} x_{n,s,g} = population_{n,g}, \quad \forall n = 1, \ldots, N, \; \forall g = 1, \ldots, G
    \]

    \item \text{Non-negativity constraint:}
    \[
    x_{n,s,g} \geq 0, \quad \forall n = 1, \ldots, N, \; \forall s = 1, \ldots, S, \; \forall g = 1, \ldots, G
    \]
\end{enumerate}

\end{document}
```

This model ensures that all students are assigned to a school such that the sum of distances is minimized, while not exceeding school capacities and fulfilling student population needs. The decision variables \( x_{n,s,g} \) indicate the assignment of students by grade and neighborhood to schools.

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

\subsection*{Sets and Indices}
\begin{align*}
N & : \text{Number of neighborhoods} \\
S & : \text{Number of schools} \\
G & : \text{Number of grades}
\end{align*}

Let:
\begin{itemize}
    \item $n = 1, \ldots, N$: Index for neighborhoods
    \item $s = 1, \ldots, S$: Index for schools
    \item $g = 1, \ldots, G$: Index for grades
\end{itemize}

\subsection*{Parameters}
\begin{align*}
capacity_{s,g} & : \text{Capacity of school } s \text{ for grade } g \\
population_{n,g} & : \text{Population of grade } g \text{ in neighborhood } n \\
d_{n,s} & : \text{Distance from neighborhood } n \text{ to school } s
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
x_{n,s,g} & : \text{Number of students of grade } g \text{ in neighborhood } n \text{ assigned to school } s
\end{align*}

\subsection*{Objective Function}
Minimize the total distance traveled by all students:
\[
\text{Minimize } \sum_{n=1}^{N} \sum_{s=1}^{S} \sum_{g=1}^{G} d_{n,s} \cdot x_{n,s,g}
\]

\subsection*{Constraints}
\begin{enumerate}
    \item \text{Capacity constraints for each school and grade:}
    \[
    \sum_{n=1}^{N} x_{n,s,g} \leq capacity_{s,g}, \quad \forall s = 1, \ldots, S, \; \forall g = 1, \ldots, G
    \]
    
    \item \text{Population constraints for each neighborhood and grade:}
    \[
    \sum_{s=1}^{S} x_{n,s,g} = population_{n,g}, \quad \forall n = 1, \ldots, N, \; \forall g = 1, \ldots, G
    \]

    \item \text{Non-negativity constraint:}
    \[
    x_{n,s,g} \geq 0, \quad \forall n = 1, \ldots, N, \; \forall s = 1, \ldots, S, \; \forall g = 1, \ldots, G
    \]
\end{enumerate}

\end{document}</MATH_MODEL>
<DATA>
{'S': 3, 'G': 2, 'N': 4, 'Capacity': [[15, 20], [20, 15], [5, 17]], 'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data
data = {
    'S': 3, 
    'G': 2, 
    'N': 4, 
    'Capacity': [[15, 20], [20, 15], [5, 17]], 
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

#### Define the problem
problem = pulp.LpProblem("SchoolAssignmentProblem", pulp.LpMinimize)

#### Indices
N = data['N']
S = data['S']
G = data['G']

#### Decision Variables
x = pulp.LpVariable.dicts("x", (range(1, N + 1), range(1, S + 1), range(1, G + 1)), lowBound=0, cat='Continuous')

#### Objective Function
problem += pulp.lpSum(data['Distance'][n-1][s-1] * x[n][s][g] for n in range(1, N + 1) for s in range(1, S + 1) for g in range(1, G + 1))

#### Constraints
#### Capacity constraints
for s in range(1, S + 1):
    for g in range(1, G + 1):
        problem += pulp.lpSum(x[n][s][g] for n in range(1, N + 1)) <= data['Capacity'][s-1][g-1]

#### Population constraints
for n in range(1, N + 1):
    for g in range(1, G + 1):
        problem += pulp.lpSum(x[n][s][g] for s in range(1, S + 1)) == data['Population'][n-1][g-1]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

