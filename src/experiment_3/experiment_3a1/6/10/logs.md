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

\textbf{Parameters:}
\begin{itemize}
    \item \( N \): Number of neighborhoods
    \item \( S \): Number of schools
    \item \( G \): Number of grades
    \item \( capacity_{s,g} \): Capacity of school \( s \) for grade \( g \)
    \item \( population_{n,g} \): Student population of grade \( g \) in neighborhood \( n \)
    \item \( d_{n,s} \): Distance from neighborhood \( n \) to school \( s \)
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item \( x_{n,s,g} \): Number of students of grade \( g \) in neighborhood \( n \) assigned to school \( s \)
\end{itemize}

\textbf{Objective Function:}
We want to minimize the total distance traveled by all students:
\[
\text{Minimize } Z = \sum_{n=1}^{N} \sum_{s=1}^{S} \sum_{g=1}^{G} d_{n,s} \cdot x_{n,s,g}
\]

\textbf{Subject to:}

\begin{itemize}
    \item \textbf{Capacity Constraints:}
    \[
    \sum_{n=1}^{N} \sum_{g=1}^{G} x_{n,s,g} \leq capacity_{s,g}, \quad \forall s \in \{1, \ldots, S\}, \forall g \in \{1, \ldots, G\}
    \]
    
    \item \textbf{Population Constraints:}
    \[
    \sum_{s=1}^{S} x_{n,s,g} = population_{n,g}, \quad \forall n \in \{1, \ldots, N\}, \forall g \in \{1, \ldots, G\}
    \]

    \item \textbf{Non-negativity Constraints:}
    \[
    x_{n,s,g} \geq 0, \quad \forall n \in \{1, \ldots, N\}, \forall s \in \{1, \ldots, S\}, \forall g \in \{1, \ldots, G\}
    \]
\end{itemize}

\textbf{Output:}
\begin{itemize}
    \item Optimal assignment: \( x_{n,s,g} \) for all \( n, s, g \)
    \item Total distance: \( total\_distance \)
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

\textbf{Parameters:}
\begin{itemize}
    \item \( N \): Number of neighborhoods
    \item \( S \): Number of schools
    \item \( G \): Number of grades
    \item \( capacity_{s,g} \): Capacity of school \( s \) for grade \( g \)
    \item \( population_{n,g} \): Student population of grade \( g \) in neighborhood \( n \)
    \item \( d_{n,s} \): Distance from neighborhood \( n \) to school \( s \)
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item \( x_{n,s,g} \): Number of students of grade \( g \) in neighborhood \( n \) assigned to school \( s \)
\end{itemize}

\textbf{Objective Function:}
We want to minimize the total distance traveled by all students:
\[
\text{Minimize } Z = \sum_{n=1}^{N} \sum_{s=1}^{S} \sum_{g=1}^{G} d_{n,s} \cdot x_{n,s,g}
\]

\textbf{Subject to:}

\begin{itemize}
    \item \textbf{Capacity Constraints:}
    \[
    \sum_{n=1}^{N} \sum_{g=1}^{G} x_{n,s,g} \leq capacity_{s,g}, \quad \forall s \in \{1, \ldots, S\}, \forall g \in \{1, \ldots, G\}
    \]
    
    \item \textbf{Population Constraints:}
    \[
    \sum_{s=1}^{S} x_{n,s,g} = population_{n,g}, \quad \forall n \in \{1, \ldots, N\}, \forall g \in \{1, \ldots, G\}
    \]

    \item \textbf{Non-negativity Constraints:}
    \[
    x_{n,s,g} \geq 0, \quad \forall n \in \{1, \ldots, N\}, \forall s \in \{1, \ldots, S\}, \forall g \in \{1, \ldots, G\}
    \]
\end{itemize}

\textbf{Output:}
\begin{itemize}
    \item Optimal assignment: \( x_{n,s,g} \) for all \( n, s, g \)
    \item Total distance: \( total\_distance \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'S': 3, 'G': 2, 'N': 4, 'Capacity': [[15, 20], [20, 15], [5, 17]], 'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Provided data in JSON format
data = '''
{
    "S": 3,
    "G": 2,
    "N": 4,
    "Capacity": [[15, 20], [20, 15], [5, 17]],
    "Population": [[7, 19], [4, 12], [9, 2], [6, 8]],
    "Distance": [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}
'''
data = json.loads(data)

#### Problem initialization
problem = pulp.LpProblem("School_Assignment_Problem", pulp.LpMinimize)

#### Variables
x = pulp.LpVariable.dicts("x", (range(data['N']), range(data['S']), range(data['G'])), lowBound=0, cat='Continuous')

#### Objective function
problem += pulp.lpSum(data['Distance'][n][s] * x[n][s][g] for n in range(data['N']) for s in range(data['S']) for g in range(data['G'])), "Total_Distance"

#### Capacity Constraints
for s in range(data['S']):
    for g in range(data['G']):
        problem += pulp.lpSum(x[n][s][g] for n in range(data['N'])) <= data['Capacity'][s][g], f"Capacity_{s}_{g}"

#### Population Constraints
for n in range(data['N']):
    for g in range(data['G']):
        problem += pulp.lpSum(x[n][s][g] for s in range(data['S'])) == data['Population'][n][g], f"Population_{n}_{g}"

#### Solve the problem
problem.solve()

#### Output results
for n in range(data['N']):
    for s in range(data['S']):
        for g in range(data['G']):
            print(f"x[{n},{s},{g}] = {x[n][s][g].varValue}")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

