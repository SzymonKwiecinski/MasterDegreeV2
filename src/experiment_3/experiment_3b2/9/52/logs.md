# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO:

- A small electric utility operates \var{P} power plants to supply electricity to \var{C} cities.
- Each power plant has a capacity of \var{supply_{p}} million kwh.
- Each city has a peak demand of \var{demand_{c}} million kwh, which must be met at the same time.
- Power plant \var{p} can send electricity to city \var{c} at a transmission cost of \var{transmission_{p,c}} $/million kwh.

INPUT FORMAT: 

{
    "supply": [supply_{p} for p in 1, ..., P],
    "demand": [demand_{c} for c in 1, ..., C],
    "transmission_costs": [[transmission_{p,c} for c in 1, ..., C] for p in 1, ..., P]
}

OBJECTIVE: How much electricity should each power plant send to each city to minimize the total transmission cost?

OUTPUT INFO:

- the amount of electricity power plant \var{p} sends to city \var{c} as \var{send_{p,c}} million kwh.
- \var{total_cost} displays the total transmission cost for the utility.

OUTPUT FORMAT:

{
    "send": [[send_{p,c} for c in 1, ..., C] for p in 1, ..., P],
    "total_cost": total_cost
}

</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To solve this linear programming problem, we need to minimize the total transmission cost while satisfying the supply constraints for each power plant and the demand constraints for each city.

Let's define the variables:
- \( \text{send}_{p,c} \) is the amount of electricity (in million kwh) sent from power plant \( p \) to city \( c \).

Objective Function:
The objective is to minimize the total transmission cost:
\[
\text{Minimize} \quad \sum_{p=1}^{P} \sum_{c=1}^{C} \text{transmission}_{p,c} \times \text{send}_{p,c}
\]

Subject to the constraints:
1. Supply Constraints for each power plant:
   \[
   \sum_{c=1}^{C} \text{send}_{p,c} \leq \text{supply}_{p}, \quad \forall p = 1, \ldots, P
   \]
2. Demand Constraints for each city:
   \[
   \sum_{p=1}^{P} \text{send}_{p,c} = \text{demand}_{c}, \quad \forall c = 1, \ldots, C
   \]
3. Non-negativity Constraints:
   \[
   \text{send}_{p,c} \geq 0, \quad \forall p = 1, \ldots, P, \quad \forall c = 1, \ldots, C
   \]

Here is the complete linear programming formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

\subsection*{Sets and Parameters}
\begin{align*}
P & : \text{Number of power plants} \\
C & : \text{Number of cities} \\
\text{supply}_p & : \text{Capacity of power plant } p \text{ (in million kwh)} \\
\text{demand}_c & : \text{Demand of city } c \text{ (in million kwh)} \\
\text{transmission}_{p,c} & : \text{Transmission cost from power plant } p \text{ to city } c \text{ (in \$/million kwh)}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
\text{send}_{p,c} & : \text{Electricity sent from power plant } p \text{ to city } c \text{ (in million kwh)}
\end{align*}

\subsection*{Objective Function}
Minimize the total transmission cost:
\[
\text{Minimize} \quad \sum_{p=1}^{P} \sum_{c=1}^{C} \text{transmission}_{p,c} \times \text{send}_{p,c}
\]

\subsection*{Constraints}
\begin{enumerate}
    \item \textbf{Supply Constraints for each power plant:}
    \[
    \sum_{c=1}^{C} \text{send}_{p,c} \leq \text{supply}_{p}, \quad \forall p = 1, \ldots, P
    \]
    
    \item \textbf{Demand Constraints for each city:}
    \[
    \sum_{p=1}^{P} \text{send}_{p,c} = \text{demand}_{c}, \quad \forall c = 1, \ldots, C
    \]
    
    \item \textbf{Non-negativity Constraints:}
    \[
    \text{send}_{p,c} \geq 0, \quad \forall p = 1, \ldots, P, \quad \forall c = 1, \ldots, C
    \]
\end{enumerate}

\end{document}
```

This formulation provides a clear and concise way to model the problem to find the optimal distribution of electricity from power plants to cities such that the total transmission cost is minimized while meeting all constraints.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

\subsection*{Sets and Parameters}
\begin{align*}
P & : \text{Number of power plants} \\
C & : \text{Number of cities} \\
\text{supply}_p & : \text{Capacity of power plant } p \text{ (in million kwh)} \\
\text{demand}_c & : \text{Demand of city } c \text{ (in million kwh)} \\
\text{transmission}_{p,c} & : \text{Transmission cost from power plant } p \text{ to city } c \text{ (in \$/million kwh)}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
\text{send}_{p,c} & : \text{Electricity sent from power plant } p \text{ to city } c \text{ (in million kwh)}
\end{align*}

\subsection*{Objective Function}
Minimize the total transmission cost:
\[
\text{Minimize} \quad \sum_{p=1}^{P} \sum_{c=1}^{C} \text{transmission}_{p,c} \times \text{send}_{p,c}
\]

\subsection*{Constraints}
\begin{enumerate}
    \item \textbf{Supply Constraints for each power plant:}
    \[
    \sum_{c=1}^{C} \text{send}_{p,c} \leq \text{supply}_{p}, \quad \forall p = 1, \ldots, P
    \]
    
    \item \textbf{Demand Constraints for each city:}
    \[
    \sum_{p=1}^{P} \text{send}_{p,c} = \text{demand}_{c}, \quad \forall c = 1, \ldots, C
    \]
    
    \item \textbf{Non-negativity Constraints:}
    \[
    \text{send}_{p,c} \geq 0, \quad \forall p = 1, \ldots, P, \quad \forall c = 1, \ldots, C
    \]
\end{enumerate}

\end{document}</MATH_MODEL>
<DATA>
{'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data input
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

#### Parameters
P = len(data['supply'])  #### Number of power plants
C = len(data['demand'])   #### Number of cities

#### Create the problem
problem = pulp.LpProblem("Minimize_Transmission_Cost", pulp.LpMinimize)

#### Decision variables
send = pulp.LpVariable.dicts("send", (range(P), range(C)), lowBound=0)

#### Objective function
problem += pulp.lpSum(data['transmission_costs'][p][c] * send[p][c] for p in range(P) for c in range(C))

#### Constraints 
#### Supply constraints
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= data['supply'][p]

#### Demand constraints
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) == data['demand'][c]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

