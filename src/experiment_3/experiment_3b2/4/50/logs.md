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
- The division sells part \var{p} in batches of 100 at price of \var{price_{p}} per batch.
- The division must produce at least \var{min_batches_{p}} batches of part \var{p} each month to fulfill a contract.
- Extra available time for machine \var{m} can be acquired at $\var{extra_costs_{m}}/hour. 
- Up to \var{max_extra_{m}} hours can be purchased for each machine \var{m}.

INPUT FORMAT: 

{
    "time_required": [[time_{m,p} for p in 1, ..., P] for m in 1, ..., M],
    "machine_costs": [cost_{m} for m in 1, ..., M],
    "availability": [available_{m} for m in 1, ..., M],
    "prices": [price_{p} for p in 1, ..., P],
    "min_batches": [min_batches_{p} for p in 1, ..., P],
    "extra_costs": [extra_cost_{m} for m in 1, ..., M],
    "max_extra": [max_extra_{m} for m in 1, ..., M]
}

OBJECTIVE: How many batches of each part should the manufacturer produce each month to maximize profit?

OUTPUT INFO:

- the number of batches of each part produced \var{batches_{p}}.
- \var{extra_time} denotes the additional hours purchased for each machine \var{m}.
- \var{total_profit} represents the total profit obtained for the month.

OUTPUT FORMAT:

{
    "batches": [batches_{p} for p in 1, ..., P],
    "extra_time": [extra_time_{p} for p in 1, ..., P],
    "total_profit": total_profit
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To solve this linear programming problem, we need to define our decision variables, objective function, and constraints. Let's formulate the mathematical model in LaTeX.

**Decision Variables:**
- Let \( x_p \) be the number of batches of part \( p \) produced in a month, where \( p = 1, \ldots, P \).
- Let \( e_m \) be the extra hours purchased for machine \( m \), where \( m = 1, \ldots, M \).

**Objective Function:**
We aim to maximize the total profit, which is the difference between the revenue from selling the parts and the costs associated with using and purchasing time on the machines. The profit is calculated as:

\[
\text{Profit} = \sum_{p=1}^{P} \text{price}_p \cdot x_p - \sum_{m=1}^{M} \text{cost}_m \cdot (\sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p + e_m) - \sum_{m=1}^{M} \text{extra\_cost}_m \cdot e_m
\]

**Constraints:**
1. Time constraints for each machine \( m \):
   \[
   \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_m + e_m, \quad \forall m = 1, \ldots, M
   \]
   
2. Minimum production constraints for each part \( p \):
   \[
   x_p \geq \text{min\_batches}_p, \quad \forall p = 1, \ldots, P
   \]

3. Extra time constraints for each machine \( m \):
   \[
   0 \leq e_m \leq \text{max\_extra}_m, \quad \forall m = 1, \ldots, M
   \]

**Non-negativity constraints:**
\[
x_p \geq 0, \quad \forall p = 1, \ldots, P
\]
\[
e_m \geq 0, \quad \forall m = 1, \ldots, M
\]

Let's present this in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_p \): Number of batches of part \( p \) produced \((p = 1, \ldots, P)\).
    \item \( e_m \): Extra hours purchased for machine \( m \) \((m = 1, \ldots, M)\).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Profit} = \sum_{p=1}^{P} \text{price}_p \cdot x_p - \sum_{m=1}^{M} \text{cost}_m \cdot \left(\sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p + e_m \right) - \sum_{m=1}^{M} \text{extra\_cost}_m \cdot e_m
\]

\subsection*{Constraints}
\begin{enumerate}
    \item Time constraints for each machine \( m \):
    \[
    \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_m + e_m, \quad \forall m = 1, \ldots, M
    \]
    
    \item Minimum production constraints for each part \( p \):
    \[
    x_p \geq \text{min\_batches}_p, \quad \forall p = 1, \ldots, P
    \]

    \item Extra time constraints for each machine \( m \):
    \[
    0 \leq e_m \leq \text{max\_extra}_m, \quad \forall m = 1, \ldots, M
    \]
\end{enumerate}

\subsection*{Non-negativity Constraints}
\[
x_p \geq 0, \quad \forall p = 1, \ldots, P
\]
\[
e_m \geq 0, \quad \forall m = 1, \ldots, M
\]

\end{document}
```

This formulation clarifies the decision variables, objective function, and constraints needed to solve the problem using linear programming techniques. The goal is to determine the optimal number of batches for each part and the extra time for machines to maximize the division's profit.

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

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_p \): Number of batches of part \( p \) produced \((p = 1, \ldots, P)\).
    \item \( e_m \): Extra hours purchased for machine \( m \) \((m = 1, \ldots, M)\).
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Profit} = \sum_{p=1}^{P} \text{price}_p \cdot x_p - \sum_{m=1}^{M} \text{cost}_m \cdot \left(\sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p + e_m \right) - \sum_{m=1}^{M} \text{extra\_cost}_m \cdot e_m
\]

\subsection*{Constraints}
\begin{enumerate}
    \item Time constraints for each machine \( m \):
    \[
    \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_m + e_m, \quad \forall m = 1, \ldots, M
    \]
    
    \item Minimum production constraints for each part \( p \):
    \[
    x_p \geq \text{min\_batches}_p, \quad \forall p = 1, \ldots, P
    \]

    \item Extra time constraints for each machine \( m \):
    \[
    0 \leq e_m \leq \text{max\_extra}_m, \quad \forall m = 1, \ldots, M
    \]
\end{enumerate}

\subsection*{Non-negativity Constraints}
\[
x_p \geq 0, \quad \forall p = 1, \ldots, P
\]
\[
e_m \geq 0, \quad \forall m = 1, \ldots, M
\]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "extra_costs": [0, 15, 22.5], "max_extra": [0, 80, 80]}')

#### Define model
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Define variables
P = len(data['prices'])  #### Number of parts
M = len(data['machine_costs'])  #### Number of machines

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0)
e = pulp.LpVariable.dicts("e", range(M), lowBound=0)

#### Objective function
profit = pulp.lpSum(data['prices'][p] * x[p] for p in range(P)) - \
         pulp.lpSum(data['machine_costs'][m] * (pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) + e[m]) for m in range(M)) - \
         pulp.lpSum(data['extra_costs'][m] * e[m] for m in range(M))

problem += profit

#### Constraints
#### Time constraints for each machine
for m in range(M):
    problem += (pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m] + e[m]), f"Time_Constraint_Machine_{m}"

#### Minimum production constraints for each part
for p in range(P):
    problem += (x[p] >= data['min_batches'][p]), f"Min_Production_Constraint_Part_{p}"

#### Extra time constraints for each machine
for m in range(M):
    problem += (0 <= e[m] <= data['max_extra'][m]), f"Extra_Time_Constraint_Machine_{m}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

