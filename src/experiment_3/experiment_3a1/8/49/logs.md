# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO:

- A division of an auto parts manufacturer produces \var{P} different parts using \var{M} different machines.
- Batch of 100 part \var{p} requires \var{time_{m,p}} hours on machine \var{m}.
- The division incurs a charge of \var{cost_{m}} per hour for using machine \var{m}.
- Machine \var{m} has an availability of up to \var{available_{m}} hours per month.
- Machine \var{M} and Machine \var{M-1} can share availability.
- Individual availability conditions for Machine \var{M} and Machine \var{M-1} can be disregarded.
- The division sells part \var{p} in batches of 100 at price of \var{price_{p}} per batch.
- The division must produce at least \var{min_batches_{p}} batches of part \var{p} each month to fulfill a contract.

INPUT FORMAT: 

{
    "time_required": [[time_{m,p} for p in 1, ..., P] for m in 1, ..., M],
    "machine_costs": [cost_{m} for m in 1, ..., M],
    "availability": [available_{m} for m in 1, ..., M],
    "prices": [price_{p} for p in 1, ..., P],
    "min_batches": [min_batches_{p} for p in 1, ..., P]
}

OBJECTIVE: How many batches of each part should the manufacturer produce each month to maximize profit?

OUTPUT INFO:

- the number of batches of each part produced \var{batches_{p}}.
- \var{total_profit} represents the total profit obtained for the month.

OUTPUT FORMAT:

{
    "batches": [batches_{p} for p in 1, ..., P],
    "total_profit": total_profit
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Variables}
Let \( x_p \) represent the number of batches produced for part \( p \) for \( p = 1, 2, \ldots, P \).

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{time}_{m,p} \): Time required on machine \( m \) to produce a batch of part \( p \) (in hours).
    \item \( \text{cost}_{m} \): Cost per hour of using machine \( m \).
    \item \( \text{available}_{m} \): Availability of machine \( m \) (in hours).
    \item \( \text{price}_{p} \): Selling price per batch of part \( p \).
    \item \( \text{min\_batches}_{p} \): Minimum number of batches required for part \( p \).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Total Profit} = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot x_p - \sum_{m=1}^{M} \text{cost}_{m} \cdot \frac{\text{time}_{m,p} \cdot x_p}{100} \right)
\]

\subsection*{Constraints}
1. **Minimum production requirement**:
\[
x_p \geq \text{min\_batches}_{p}, \quad \forall p = 1, \ldots, P
\]

2. **Machine availability**:
\[
\sum_{p=1}^{P} \sum_{m=1}^{M} \text{time}_{m,p} \cdot x_p \leq \sum_{m=1}^{M} \text{available}_{m}
\]

3. **Non-negativity**:
\[
x_p \geq 0, \quad \forall p = 1, \ldots, P
\]

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

\section*{Linear Programming Model}

\subsection*{Variables}
Let \( x_p \) represent the number of batches produced for part \( p \) for \( p = 1, 2, \ldots, P \).

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{time}_{m,p} \): Time required on machine \( m \) to produce a batch of part \( p \) (in hours).
    \item \( \text{cost}_{m} \): Cost per hour of using machine \( m \).
    \item \( \text{available}_{m} \): Availability of machine \( m \) (in hours).
    \item \( \text{price}_{p} \): Selling price per batch of part \( p \).
    \item \( \text{min\_batches}_{p} \): Minimum number of batches required for part \( p \).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Total Profit} = \sum_{p=1}^{P} \left( \text{price}_{p} \cdot x_p - \sum_{m=1}^{M} \text{cost}_{m} \cdot \frac{\text{time}_{m,p} \cdot x_p}{100} \right)
\]

\subsection*{Constraints}
1. **Minimum production requirement**:
\[
x_p \geq \text{min\_batches}_{p}, \quad \forall p = 1, \ldots, P
\]

2. **Machine availability**:
\[
\sum_{p=1}^{P} \sum_{m=1}^{M} \text{time}_{m,p} \cdot x_p \leq \sum_{m=1}^{M} \text{available}_{m}
\]

3. **Non-negativity**:
\[
x_p \geq 0, \quad \forall p = 1, \ldots, P
\]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10]
}

#### Extracting parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

#### Define parameters
P = len(prices)  #### Number of parts
M = len(machine_costs)  #### Number of machines

#### Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Define decision variables
x = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

#### Define the objective function
total_profit = pulp.lpSum([prices[p] * x[p] - 
                            pulp.lpSum([machine_costs[m] * (time_required[m][p] * x[p] / 100) 
                                         for m in range(M)]) 
                            for p in range(P)])

problem += total_profit, "Total_Profit"

#### Constraints
#### Minimum production requirement
for p in range(P):
    problem += x[p] >= min_batches[p], f"MinProductionRequirement_part_{p}"

#### Machine availability constraint
problem += (pulp.lpSum([pulp.lpSum([time_required[m][p] * x[p] for p in range(P)]) 
                                 for m in range(M)]) <= 
                     pulp.lpSum(availability), "Machine_Availability")

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

