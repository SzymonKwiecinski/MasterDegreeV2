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
To create a mathematical model for this Linear Programming problem, we need to define our decision variables, objective function, and constraints. Here's the LaTeX representation of the problem:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mathematical Model}

Let \( x_p \) represent the number of batches of part \( p \) produced. The objective is to maximize the total profit, which is given by:

\[
\text{Profit} = \sum_{p=1}^{P} (\text{price}_p \times x_p) - \sum_{m=1}^{M} \text{cost}_m \left( \sum_{p=1}^{P} \text{time}_{m,p} \times x_p \right)
\]

\subsection*{Objective Function}

Maximize:
\[
Z = \sum_{p=1}^{P} \left( \text{price}_p \times x_p \right) - \sum_{m=1}^{M} \left( \text{cost}_m \sum_{p=1}^{P} \text{time}_{m,p} \times x_p \right)
\]

\subsection*{Constraints}

1. Availability constraint for Machines 1 to \( M-2 \):
\[
\sum_{p=1}^{P} \text{time}_{m,p} \times x_p \leq \text{available}_m, \quad \forall m = 1, \ldots, M-2
\]

2. Combined availability constraint for Machines \( M-1 \) and \( M \):
\[
\sum_{p=1}^{P} \text{time}_{M-1,p} \times x_p + \sum_{p=1}^{P} \text{time}_{M,p} \times x_p \leq \text{available}_{M-1} + \text{available}_M
\]

3. Minimum production constraint for each part:
\[
x_p \geq \text{min\_batches}_p, \quad \forall p = 1, \ldots, P
\]

4. Non-negativity constraint:
\[
x_p \geq 0, \quad \forall p = 1, \ldots, P
\]

\subsection*{Decision Variables}
- \( x_p \): Number of batches of part \( p \) produced for \( p = 1, 2, \ldots, P \).

\end{document}
```

In this model, the objective function maximizes the profit, which is the revenue from selling the parts minus the cost incurred from using the machines. The constraints ensure that the machine availability is not exceeded, while combining the availability for the last two machines as specified. The minimum production constraints ensure fulfillment of contractual obligations.

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

Let \( x_p \) represent the number of batches of part \( p \) produced. The objective is to maximize the total profit, which is given by:

\[
\text{Profit} = \sum_{p=1}^{P} (\text{price}_p \times x_p) - \sum_{m=1}^{M} \text{cost}_m \left( \sum_{p=1}^{P} \text{time}_{m,p} \times x_p \right)
\]

\subsection*{Objective Function}

Maximize:
\[
Z = \sum_{p=1}^{P} \left( \text{price}_p \times x_p \right) - \sum_{m=1}^{M} \left( \text{cost}_m \sum_{p=1}^{P} \text{time}_{m,p} \times x_p \right)
\]

\subsection*{Constraints}

1. Availability constraint for Machines 1 to \( M-2 \):
\[
\sum_{p=1}^{P} \text{time}_{m,p} \times x_p \leq \text{available}_m, \quad \forall m = 1, \ldots, M-2
\]

2. Combined availability constraint for Machines \( M-1 \) and \( M \):
\[
\sum_{p=1}^{P} \text{time}_{M-1,p} \times x_p + \sum_{p=1}^{P} \text{time}_{M,p} \times x_p \leq \text{available}_{M-1} + \text{available}_M
\]

3. Minimum production constraint for each part:
\[
x_p \geq \text{min\_batches}_p, \quad \forall p = 1, \ldots, P
\]

4. Non-negativity constraint:
\[
x_p \geq 0, \quad \forall p = 1, \ldots, P
\]

\subsection*{Decision Variables}
- \( x_p \): Number of batches of part \( p \) produced for \( p = 1, 2, \ldots, P \).

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

#### Extracting the data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

#### Number of parts and machines
P = len(prices)
M = len(machine_costs)

#### Problem setup
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{p}', lowBound=0, cat='Continuous') for p in range(P)]

#### Objective Function
profit = pulp.lpSum(prices[p] * x[p] for p in range(P))
costs = pulp.lpSum(
    machine_costs[m] * pulp.lpSum(time_required[m][p] * x[p] for p in range(P))
    for m in range(M)
)
problem += profit - costs, "Total_Profit"

#### Constraints

#### Availability constraints for Machines 1 to M-2
for m in range(M-2):
    problem += pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) <= availability[m], f"Machine_{m+1}_Availability"

#### Combined availability constraint for Machines M-1 and M
problem += pulp.lpSum(time_required[M-2][p] * x[p] for p in range(P)) + \
           pulp.lpSum(time_required[M-1][p] * x[p] for p in range(P)) <= availability[M-2] + availability[M-1], "Combined_Machines_Availability"

#### Minimum production constraint for each part
for p in range(P):
    problem += x[p] >= min_batches[p], f"Min_Production_{p+1}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

