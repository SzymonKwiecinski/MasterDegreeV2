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
To create a linear programming model for this problem, we need to define decision variables, constraints, and the objective function. The decision variable for this problem is \( x_{n,s,g} \), which represents the number of students of grade \( g \) in neighborhood \( n \) assigned to school \( s \).

The objective function aims to minimize the total distance traveled by all students:

\[
\text{Minimize } \sum_{n=1}^{N} \sum_{s=1}^{S} \sum_{g=1}^{G} d_{n,s} \cdot x_{n,s,g}
\]

The constraints are:

1. Every student must be assigned to a school:
   \[
   \sum_{s=1}^{S} x_{n,s,g} = \text{population}_{n,g} \quad \forall n, g
   \]

2. The number of students assigned to a school for each grade must not exceed the school's capacity:
   \[
   \sum_{n=1}^{N} x_{n,s,g} \leq \text{capacity}_{s,g} \quad \forall s, g
   \]

3. Non-negativity constraint:
   \[
   x_{n,s,g} \geq 0 \quad \forall n, s, g
   \]

Here is the linear programming model for this problem in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

Minimize the total distance traveled by all students:

\[
\sum_{n=1}^{N} \sum_{s=1}^{S} \sum_{g=1}^{G} d_{n,s} \cdot x_{n,s,g}
\]

\textbf{Subject to:}

Every student must be assigned to a school:

\[
\sum_{s=1}^{S} x_{n,s,g} = \text{population}_{n,g} \quad \forall n, g
\]

Capacity constraints:

\[
\sum_{n=1}^{N} x_{n,s,g} \leq \text{capacity}_{s,g} \quad \forall s, g
\]

Non-negativity constraints:

\[
x_{n,s,g} \geq 0 \quad \forall n, s, g
\]

\end{document}
```

When implemented, this LP model will output the optimal values of \( x_{n,s,g} \) which represent the assignment of students to schools, and the minimized total distance, \( \text{total\_distance} \).

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

Minimize the total distance traveled by all students:

\[
\sum_{n=1}^{N} \sum_{s=1}^{S} \sum_{g=1}^{G} d_{n,s} \cdot x_{n,s,g}
\]

\textbf{Subject to:}

Every student must be assigned to a school:

\[
\sum_{s=1}^{S} x_{n,s,g} = \text{population}_{n,g} \quad \forall n, g
\]

Capacity constraints:

\[
\sum_{n=1}^{N} x_{n,s,g} \leq \text{capacity}_{s,g} \quad \forall s, g
\]

Non-negativity constraints:

\[
x_{n,s,g} \geq 0 \quad \forall n, s, g
\]

\end{document}</MATH_MODEL>
<DATA>
{'S': 3, 'G': 2, 'N': 4, 'Capacity': [[15, 20], [20, 15], [5, 17]], 'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the given JSON format
data = {
    'S': 3,
    'G': 2,
    'N': 4,
    'Capacity': [[15, 20], [20, 15], [5, 17]],
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]],
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

#### Create the problem
problem = pulp.LpProblem("Minimize_Student_Transport_Distance", pulp.LpMinimize)

#### Variables
x = pulp.LpVariable.dicts("x", (range(data['N']), range(data['S']), range(data['G'])), lowBound=0)

#### Objective function
problem += pulp.lpSum(data['Distance'][n][s] * x[n][s][g] for n in range(data['N']) for s in range(data['S']) for g in range(data['G']))

#### Constraints: Every student must be assigned to a school
for n in range(data['N']):
    for g in range(data['G']):
        problem += pulp.lpSum(x[n][s][g] for s in range(data['S'])) == data['Population'][n][g]

#### Capacity constraints
for s in range(data['S']):
    for g in range(data['G']):
        problem += pulp.lpSum(x[n][s][g] for n in range(data['N'])) <= data['Capacity'][s][g]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

