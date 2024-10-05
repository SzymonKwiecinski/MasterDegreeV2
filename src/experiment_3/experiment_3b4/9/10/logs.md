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
To model the given problem as a Linear Programming (LP) problem, we will define the decision variables, objective function, and constraints.

**Decision Variables:**

Let \(x_{n,s,g}\) be the number of students of grade \(g\) in neighborhood \(n\) assigned to school \(s\).

**Objective Function:**

Minimize the total distance traveled by all students, which is given by:

\[
\text{Minimize} \quad \sum_{n=1}^{N} \sum_{s=1}^{S} \sum_{g=1}^{G} d_{n,s} \cdot x_{n,s,g}
\]

**Constraints:**

1. **Capacity Constraint:** The number of students assigned to each school \(s\) for each grade \(g\) must not exceed the capacity of that school for that grade.

   \[
   \sum_{n=1}^{N} x_{n,s,g} \leq \text{capacity}_{s,g} \quad \forall s, \forall g
   \]

2. **Population Constraint:** All students from each neighborhood \(n\) for each grade \(g\) must be assigned to some school.

   \[
   \sum_{s=1}^{S} x_{n,s,g} = \text{population}_{n,g} \quad \forall n, \forall g
   \]

3. **Non-negativity Constraint:** The number of students assigned to any school must be non-negative.

   \[
   x_{n,s,g} \geq 0 \quad \forall n, \forall s, \forall g
   \]

Here is the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables}
Let \( x_{n,s,g} \) be the number of students of grade \( g \) in neighborhood \( n \) assigned to school \( s \).

\subsection*{Objective Function}
Minimize the total distance traveled by all students:
\[
\text{Minimize} \quad \sum_{n=1}^{N} \sum_{s=1}^{S} \sum_{g=1}^{G} d_{n,s} \cdot x_{n,s,g}
\]

\subsection*{Constraints}

1. Capacity Constraint:
\[
\sum_{n=1}^{N} x_{n,s,g} \leq \text{capacity}_{s,g} \quad \forall s, \forall g
\]

2. Population Constraint:
\[
\sum_{s=1}^{S} x_{n,s,g} = \text{population}_{n,g} \quad \forall n, \forall g
\]

3. Non-negativity Constraint:
\[
x_{n,s,g} \geq 0 \quad \forall n, \forall s, \forall g
\]

\end{document}
```

This model can be solved using a linear programming solver to obtain the optimal assignment of students to schools while minimizing the total distance traveled. The solution will provide the values of \( x_{n,s,g} \) for all \( n \), \( s \), and \( g \), as well as the total distance traveled.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables}
Let \( x_{n,s,g} \) be the number of students of grade \( g \) in neighborhood \( n \) assigned to school \( s \).

\subsection*{Objective Function}
Minimize the total distance traveled by all students:
\[
\text{Minimize} \quad \sum_{n=1}^{N} \sum_{s=1}^{S} \sum_{g=1}^{G} d_{n,s} \cdot x_{n,s,g}
\]

\subsection*{Constraints}

1. Capacity Constraint:
\[
\sum_{n=1}^{N} x_{n,s,g} \leq \text{capacity}_{s,g} \quad \forall s, \forall g
\]

2. Population Constraint:
\[
\sum_{s=1}^{S} x_{n,s,g} = \text{population}_{n,g} \quad \forall n, \forall g
\]

3. Non-negativity Constraint:
\[
x_{n,s,g} \geq 0 \quad \forall n, \forall s, \forall g
\]

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
    'Distance': [
        [5.2, 4.0, 3.1],
        [3.8, 5.5, 6.1],
        [4.2, 3.5, 5.0],
        [5.0, 4.1, 3.2]
    ]
}

#### Indices
S = data['S']
G = data['G']
N = data['N']
Capacity = data['Capacity']
Population = data['Population']
Distance = data['Distance']

#### Variables
x = pulp.LpVariable.dicts("x", (range(N), range(S), range(G)), lowBound=0, cat=pulp.LpContinuous)

#### Problem
problem = pulp.LpProblem("Student_Assignment", pulp.LpMinimize)

#### Objective Function
problem += pulp.lpSum(Distance[n][s] * x[n][s][g] for n in range(N) for s in range(S) for g in range(G)), "Total_Distance"

#### Constraints

#### Capacity Constraint
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for n in range(N)) <= Capacity[s][g], f"Capacity_Constraint_S{s}_G{g}"

#### Population Constraint
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for s in range(S)) == Population[n][g], f"Population_Constraint_N{n}_G{g}"

#### Solve the problem
problem.solve()

#### Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

