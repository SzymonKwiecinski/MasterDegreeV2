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
To model the given problem, we need to define the decision variables, objective function, and constraints. Let's break it down:

**Decision Variables:**
- \( x_p \): Number of batches of part \( p \) to produce, for \( p = 1, \ldots, P \).
- \( e_m \): Extra time purchased for machine \( m \), for \( m = 1, \ldots, M \).

**Objective Function:**
The objective is to maximize the profit. Profit is defined as the total revenue from selling the parts minus the costs of operating the machines (including any extra time purchased). The total revenue is the sum over all parts of the number of batches times the price per batch. The cost includes the time cost for each machine used and the extra time cost if any machine requires more hours than available.

Objective Function:
\[
\text{Maximize} \quad Z = \sum_{p=1}^{P} \text{price}_{p} \cdot x_p - \sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \left( \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \right) + \text{extra\_cost}_{m} \cdot e_m \right)
\]

**Constraints:**
1. **Minimum Production Requirements:**
   \[
   x_p \geq \text{min\_batches}_{p}, \quad \forall p = 1, \ldots, P
   \]

2. **Machine Time Constraints:**
   \[
   \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_{m} + e_m, \quad \forall m = 1, \ldots, M
   \]

3. **Extra Time Constraints:**
   \[
   0 \leq e_m \leq \text{max\_extra}_{m}, \quad \forall m = 1, \ldots, M
   \]

4. **Non-Negativity Constraints:**
   \[
   x_p \geq 0, \quad \forall p = 1, \ldots, P
   \]
   \[
   e_m \geq 0, \quad \forall m = 1, \ldots, M
   \]

Now, let's write this as a LaTeX document:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables}
\begin{align*}
x_p &: \text{Number of batches of part } p, \quad \forall p = 1, \ldots, P \\
e_m &: \text{Extra time purchased for machine } m, \quad \forall m = 1, \ldots, M
\end{align*}

\subsection*{Objective Function}
\[
\text{Maximize} \quad Z = \sum_{p=1}^{P} \text{price}_{p} \cdot x_p - \sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \left( \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \right) + \text{extra\_cost}_{m} \cdot e_m \right)
\]

\subsection*{Constraints}
\paragraph{Minimum Production Requirements:}
\[
x_p \geq \text{min\_batches}_{p}, \quad \forall p = 1, \ldots, P
\]

\paragraph{Machine Time Constraints:}
\[
\sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_{m} + e_m, \quad \forall m = 1, \ldots, M
\]

\paragraph{Extra Time Constraints:}
\[
0 \leq e_m \leq \text{max\_extra}_{m}, \quad \forall m = 1, \ldots, M
\]

\paragraph{Non-Negativity Constraints:}
\[
x_p \geq 0, \quad \forall p = 1, \ldots, P
\]
\[
e_m \geq 0, \quad \forall m = 1, \ldots, M
\]

\end{document}
```

This formulation will help you determine the optimal number of batches for each part and any extra machine hours needed to maximize profit.

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
\begin{align*}
x_p &: \text{Number of batches of part } p, \quad \forall p = 1, \ldots, P \\
e_m &: \text{Extra time purchased for machine } m, \quad \forall m = 1, \ldots, M
\end{align*}

\subsection*{Objective Function}
\[
\text{Maximize} \quad Z = \sum_{p=1}^{P} \text{price}_{p} \cdot x_p - \sum_{m=1}^{M} \left( \text{cost}_{m} \cdot \left( \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \right) + \text{extra\_cost}_{m} \cdot e_m \right)
\]

\subsection*{Constraints}
\paragraph{Minimum Production Requirements:}
\[
x_p \geq \text{min\_batches}_{p}, \quad \forall p = 1, \ldots, P
\]

\paragraph{Machine Time Constraints:}
\[
\sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{available}_{m} + e_m, \quad \forall m = 1, \ldots, M
\]

\paragraph{Extra Time Constraints:}
\[
0 \leq e_m \leq \text{max\_extra}_{m}, \quad \forall m = 1, \ldots, M
\]

\paragraph{Non-Negativity Constraints:}
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

#### Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

machines = range(len(data['machine_costs']))
parts = range(len(data['prices']))

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("Batches", parts, lowBound=0, cat='Continuous')
e = pulp.LpVariable.dicts("Extra_Time", machines, lowBound=0, cat='Continuous')

#### Objective Function
profit_term = pulp.lpSum([data['prices'][p] * x[p] for p in parts])
cost_term = pulp.lpSum([data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * x[p] for p in parts) + data['extra_costs'][m] * e[m] for m in machines])

problem += profit_term - cost_term

#### Constraints
#### Minimum Production Requirements
for p in parts:
    problem += x[p] >= data['min_batches'][p], f"Min_Batches_{p}"

#### Machine Time Constraints
for m in machines:
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in parts) <= data['availability'][m] + e[m], f"Time_Constraint_{m}"

#### Extra Time Constraints
for m in machines:
    problem += e[m] <= data['max_extra'][m], f"Max_Extra_Time_{m}"

#### Solve
problem.solve()

#### Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

