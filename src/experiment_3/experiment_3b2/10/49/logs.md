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

\section*{Mathematical Model}

Let \( P \) be the number of parts and \( M \) the number of machines.

\subsection*{Parameters}

\begin{itemize}
    \item \( \text{time\_required}_{m,p} \): Time in hours required on machine \( m \) to produce 100 parts of type \( p \).
    \item \( \text{machine\_costs}_m \): Cost in dollars per hour for using machine \( m \).
    \item \( \text{availability}_m \): Available hours per month for machine \( m \).
    \item \( \text{prices}_p \): Selling price per 100 parts of type \( p \).
    \item \( \text{min\_batches}_p \): Minimum number of batches of part \( p \) required to meet contractual obligations.
\end{itemize}

\subsection*{Decision Variables}

\begin{itemize}
    \item \( \text{batches}_p \): Number of batches of part \( p \) to produce.
\end{itemize}

\subsection*{Objective Function}

Maximize the profit, which is the revenue minus the cost of machine usage:

\[
\text{Maximize } \text{Profit} = \sum_{p=1}^{P} \left( \text{prices}_p \times \text{batches}_p \right) - \sum_{m=1}^{M} \left( \text{machine\_costs}_m \times \sum_{p=1}^{P} \text{time\_required}_{m,p} \times \text{batches}_p \right)
\]

\subsection*{Constraints}

\begin{itemize}
    \item Machine availability for machines 1 to \( M-2 \):
    \[
    \sum_{p=1}^{P} \text{time\_required}_{m,p} \times \text{batches}_p \leq \text{availability}_m \quad \forall m = 1, 2, \ldots, M-2
    \]
    
    \item Combined machine availability for machines \( M \) and \( M-1 \):
    \[
    \sum_{p=1}^{P} \text{time\_required}_{M,p} \times \text{batches}_p + \sum_{p=1}^{P} \text{time\_required}_{M-1,p} \times \text{batches}_p \leq \text{availability}_M + \text{availability}_{M-1}
    \]
    
    \item Minimum production requirements:
    \[
    \text{batches}_p \geq \text{min\_batches}_p \quad \forall p = 1, 2, \ldots, P
    \]
    
    \item Non-negativity:
    \[
    \text{batches}_p \geq 0 \quad \forall p = 1, 2, \ldots, P
    \]
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

\section*{Mathematical Model}

Let \( P \) be the number of parts and \( M \) the number of machines.

\subsection*{Parameters}

\begin{itemize}
    \item \( \text{time\_required}_{m,p} \): Time in hours required on machine \( m \) to produce 100 parts of type \( p \).
    \item \( \text{machine\_costs}_m \): Cost in dollars per hour for using machine \( m \).
    \item \( \text{availability}_m \): Available hours per month for machine \( m \).
    \item \( \text{prices}_p \): Selling price per 100 parts of type \( p \).
    \item \( \text{min\_batches}_p \): Minimum number of batches of part \( p \) required to meet contractual obligations.
\end{itemize}

\subsection*{Decision Variables}

\begin{itemize}
    \item \( \text{batches}_p \): Number of batches of part \( p \) to produce.
\end{itemize}

\subsection*{Objective Function}

Maximize the profit, which is the revenue minus the cost of machine usage:

\[
\text{Maximize } \text{Profit} = \sum_{p=1}^{P} \left( \text{prices}_p \times \text{batches}_p \right) - \sum_{m=1}^{M} \left( \text{machine\_costs}_m \times \sum_{p=1}^{P} \text{time\_required}_{m,p} \times \text{batches}_p \right)
\]

\subsection*{Constraints}

\begin{itemize}
    \item Machine availability for machines 1 to \( M-2 \):
    \[
    \sum_{p=1}^{P} \text{time\_required}_{m,p} \times \text{batches}_p \leq \text{availability}_m \quad \forall m = 1, 2, \ldots, M-2
    \]
    
    \item Combined machine availability for machines \( M \) and \( M-1 \):
    \[
    \sum_{p=1}^{P} \text{time\_required}_{M,p} \times \text{batches}_p + \sum_{p=1}^{P} \text{time\_required}_{M-1,p} \times \text{batches}_p \leq \text{availability}_M + \text{availability}_{M-1}
    \]
    
    \item Minimum production requirements:
    \[
    \text{batches}_p \geq \text{min\_batches}_p \quad \forall p = 1, 2, \ldots, P
    \]
    
    \item Non-negativity:
    \[
    \text{batches}_p \geq 0 \quad \forall p = 1, 2, \ldots, P
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

#### Problem setup
P = len(data['prices'])  #### number of parts
M = len(data['machine_costs'])  #### number of machines

#### Creating the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

#### Objective Function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) - \
         pulp.lpSum(data['machine_costs'][m] * 
                     pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) 
                     for m in range(M))

problem += profit, "Total_Profit"

#### Constraints for machines 1 to M-2
for m in range(M-2):
    problem += (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) 
                 <= data['availability'][m]), f"Machine_Availability_{m+1}"

#### Combined machine availability for machines M and M-1
problem += (pulp.lpSum(data['time_required'][M-1][p] * batches[p] for p in range(P)) + 
             pulp.lpSum(data['time_required'][M-2][p] * batches[p] for p in range(P)) 
             <= data['availability'][M-1] + data['availability'][M-2]), "Combined_Machine_Availability"

#### Minimum production requirements
for p in range(P):
    problem += batches[p] >= data['min_batches'][p], f"Min_Production_Requirement_{p+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

