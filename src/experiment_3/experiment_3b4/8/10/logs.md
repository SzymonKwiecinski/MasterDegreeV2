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
To tackle this problem, we will formulate it as a Linear Programming (LP) model. The objective is to minimize the total distance traveled by all students while adhering to the constraints of school capacities and complete assignment of students from each neighborhood for each grade.

Let's define the decision variable \( x_{n,s,g} \) as the number of students of grade \( g \) from neighborhood \( n \) assigned to school \( s \).

The LP model for this problem is as follows:

Objective:
Minimize the total distance traveled by all students.
\[
\text{Minimize } \sum_{n=1}^{N} \sum_{s=1}^{S} \sum_{g=1}^{G} d_{n,s} \cdot x_{n,s,g}
\]

Subject to the following constraints:

1. All students from each neighborhood for each grade must be assigned:
\[
\sum_{s=1}^{S} x_{n,s,g} = \text{population}_{n,g}, \quad \forall n = 1, \ldots, N, \, \forall g = 1, \ldots, G
\]

2. School capacity constraints for each grade:
\[
\sum_{n=1}^{N} x_{n,s,g} \leq \text{capacity}_{s,g}, \quad \forall s = 1, \ldots, S, \, \forall g = 1, \ldots, G
\]

3. Non-negativity constraints:
\[
x_{n,s,g} \geq 0, \quad \forall n = 1, \ldots, N, \, \forall s = 1, \ldots, S, \, \forall g = 1, \ldots, G
\]

Below is the corresponding code snippet in LaTeX using an environment suitable for expressing linear programming models:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Objective:}
Minimize the total distance traveled by all students:
\[
\text{Minimize } \sum_{n=1}^{N} \sum_{s=1}^{S} \sum_{g=1}^{G} d_{n,s} \cdot x_{n,s,g}
\]

\subsection*{Constraints:}

1. All students from each neighborhood for each grade must be assigned:
\[
\sum_{s=1}^{S} x_{n,s,g} = \text{population}_{n,g}, \quad \forall n = 1, \ldots, N, \, \forall g = 1, \ldots, G
\]

2. School capacity constraints for each grade:
\[
\sum_{n=1}^{N} x_{n,s,g} \leq \text{capacity}_{s,g}, \quad \forall s = 1, \ldots, S, \, \forall g = 1, \ldots, G
\]

3. Non-negativity constraints:
\[
x_{n,s,g} \geq 0, \quad \forall n = 1, \ldots, N, \, \forall s = 1, \ldots, S, \, \forall g = 1, \ldots, G
\]

\end{document}
```

This Linear Programming formulation optimally assigns students to schools across different neighborhoods and grades while minimizing the aggregate distance traveled. To solve this LP problem, you can use numerical solvers like CPLEX, Gurobi, or open-source solvers such as GLPK or the `scipy.optimize.linprog` function in Python.

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

\subsection*{Objective:}
Minimize the total distance traveled by all students:
\[
\text{Minimize } \sum_{n=1}^{N} \sum_{s=1}^{S} \sum_{g=1}^{G} d_{n,s} \cdot x_{n,s,g}
\]

\subsection*{Constraints:}

1. All students from each neighborhood for each grade must be assigned:
\[
\sum_{s=1}^{S} x_{n,s,g} = \text{population}_{n,g}, \quad \forall n = 1, \ldots, N, \, \forall g = 1, \ldots, G
\]

2. School capacity constraints for each grade:
\[
\sum_{n=1}^{N} x_{n,s,g} \leq \text{capacity}_{s,g}, \quad \forall s = 1, \ldots, S, \, \forall g = 1, \ldots, G
\]

3. Non-negativity constraints:
\[
x_{n,s,g} \geq 0, \quad \forall n = 1, \ldots, N, \, \forall s = 1, \ldots, S, \, \forall g = 1, \ldots, G
\]

\end{document}</MATH_MODEL>
<DATA>
{'S': 3, 'G': 2, 'N': 4, 'Capacity': [[15, 20], [20, 15], [5, 17]], 'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Extract data
data = {'S': 3, 'G': 2, 'N': 4, 'Capacity': [[15, 20], [20, 15], [5, 17]], 
        'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 
        'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]}

S = data['S']
G = data['G']
N = data['N']
capacity = data['Capacity']
population = data['Population']
distance = data['Distance']

#### Initialize the problem
problem = pulp.LpProblem("School_Assignment_Minimize_Distance", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(S), range(G)), lowBound=0, cat='Continuous')

#### Objective function: Minimize total distance
problem += pulp.lpSum(distance[n][s] * x[n][s][g] for n in range(N) for s in range(S) for g in range(G))

#### Constraints
#### Population assignment constraints
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for s in range(S)) == population[n][g]

#### School capacity constraints
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for n in range(N)) <= capacity[s][g]

#### Solve the problem
problem.solve()

#### Result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


