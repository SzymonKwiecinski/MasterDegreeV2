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
- Machine \var{1} is being outsourced so that the manufacturer must pay for the labor.
- The labor costs $\var{standard_cost}/h up to \var{overtime_hour} hours, after which it costs $\var{overtime_cost}/h due to overtime.
- Individual availability conditions for Machine \var{1} can be disregarded.
- The desired profit should surpass \var{min_profit}.

INPUT FORMAT: 

{
    "time_required": [[time_{m,p} for p in 1, ..., P] for m in 1, ..., M],
    "machine_costs": [cost_{m} for m in 1, ..., M],
    "availability": [available_{m} for m in 1, ..., M],
    "prices": [price_{p} for p in 1, ..., P],
    "min_batches": [min_batches_{p} for p in 1, ..., P],
    "standard_cost": standard_cost,
    "overtime_cost": overtime_cost,
    "overtime_hour": overtime_hour,
    "min_profit": min_profit
}

OBJECTIVE: Determine the quantity of batches for each part the manufacturer should produce every month, ensuring all constraints are met.

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

\textbf{Decision Variables:}
\begin{itemize}
    \item Let \( b_p \) = Number of batches produced of part \( p \) for \( p = 1, 2, \ldots, P \).
\end{itemize}

\textbf{Objective Function:}
\begin{align*}
    \text{Maximize } Z & = \sum_{p=1}^{P} (price_p \cdot b_p) - \sum_{m=1}^{M} \left( cost_m \cdot \sum_{p=1}^{P} (time_{m,p} \cdot b_p) \right) \\
    & - \text{Labor Cost for Machine 1}
\end{align*}

Where the labor cost associated with Machine 1 is given by:
\[
\text{Labor Cost} = \begin{cases} 
standard\_cost \cdot (t) & \text{if } t \leq overtime\_hour \\
standard\_cost \cdot overtime\_hour + overtime\_cost \cdot (t - overtime\_hour) & \text{if } t > overtime\_hour 
\end{cases}
\]
with \( t = \sum_{p=1}^{P} (time_{1,p} \cdot b_p) \).

\textbf{Constraints:}
\begin{align*}
    \sum_{p=1}^{P} (time_{m,p} \cdot b_p) & \leq available_m, \quad \forall m = 2, \ldots, M \\
    b_p & \geq min\_batches_p, \quad \forall p = 1, \ldots, P \\
    Z & \geq min\_profit
\end{align*}

\textbf{Non-negativity:}
\[
b_p \geq 0, \quad \forall p = 1, \ldots, P
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

\textbf{Decision Variables:}
\begin{itemize}
    \item Let \( b_p \) = Number of batches produced of part \( p \) for \( p = 1, 2, \ldots, P \).
\end{itemize}

\textbf{Objective Function:}
\begin{align*}
    \text{Maximize } Z & = \sum_{p=1}^{P} (price_p \cdot b_p) - \sum_{m=1}^{M} \left( cost_m \cdot \sum_{p=1}^{P} (time_{m,p} \cdot b_p) \right) \\
    & - \text{Labor Cost for Machine 1}
\end{align*}

Where the labor cost associated with Machine 1 is given by:
\[
\text{Labor Cost} = \begin{cases} 
standard\_cost \cdot (t) & \text{if } t \leq overtime\_hour \\
standard\_cost \cdot overtime\_hour + overtime\_cost \cdot (t - overtime\_hour) & \text{if } t > overtime\_hour 
\end{cases}
\]
with \( t = \sum_{p=1}^{P} (time_{1,p} \cdot b_p) \).

\textbf{Constraints:}
\begin{align*}
    \sum_{p=1}^{P} (time_{m,p} \cdot b_p) & \leq available_m, \quad \forall m = 2, \ldots, M \\
    b_p & \geq min\_batches_p, \quad \forall p = 1, \ldots, P \\
    Z & \geq min\_profit
\end{align*}

\textbf{Non-negativity:}
\[
b_p \geq 0, \quad \forall p = 1, \ldots, P
\]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'standard_cost': 20, 'overtime_cost': 30, 'overtime_hour': 400, 'min_profit': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
Based on the provided mathematical model and data, here is the Python script using the Pulp library for linear programming:

```python
import pulp

#### Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'standard_cost': 20,
    'overtime_cost': 30,
    'overtime_hour': 400,
    'min_profit': 5000
}

#### Constants
P = len(data['prices'])  #### Number of parts
M = len(data['availability'])  #### Number of machines

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
b = pulp.LpVariable.dicts("b", range(P), lowBound=0)  #### Number of batches for each part

#### Objective function: 
#### Maximize Z = sum(price_p * b_p) - sum(cost_m * sum(time_{m,p} * b_p)) - Labor Cost for Machine 1

#### Labor cost for Machine 1
t = pulp.lpSum(data['time_required'][0][p] * b[p] for p in range(P))  #### Total time on Machine 1
labor_cost = pulp.LpVariable("labor_cost")
problem += (pulp.lpSum(data['prices'][p] * b[p] for p in range(P)) -
             pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * b[p] for p in range(P)) for m in range(1, M)) -
             pulp.ifThen(t <= data['overtime_hour'],
                         labor_cost == data['standard_cost'] * t,
                         labor_cost == data['standard_cost'] * data['overtime_hour'] + data['overtime_cost'] * (t - data['overtime_hour'])))

#### Constraints
#### Machine Availability Constraints
for m in range(1, M):
    problem += pulp.lpSum(data['time_required[m][p]'] * b[p] for p in range(P)) <= data['availability'][m], f"Availability_constraint_machine_{m+1}"

#### Minimum batches for each part
for p in range(P):
    problem += b[p] >= data['min_batches'][p], f"Min_batches_constraint_part_{p+1}"

#### Minimum profit constraint
problem += (pulp.lpSum(data['prices'][p] * b[p] for p in range(P)) -
             pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * b[p] for p in range(P)) for m in range(1, M)) -
             labor_cost >= data['min_profit'], "Min_profit_constraint")

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

In this script:

1. We define the decision variable `b` for the number of batches produced for each part.
2. We set up the objective function including the revenue from the prices of the parts, the costs associated with each machine, and the labor costs from Machine 1.
3. We create constraints for machine availability, minimum batches per part, and the minimum profit condition.
4. Finally, we solve the linear programming problem and print the objective value as required.

