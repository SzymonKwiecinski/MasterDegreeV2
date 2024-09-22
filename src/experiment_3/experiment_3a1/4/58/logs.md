# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MIP

PROBLEM INFO:

- A division of an auto parts manufacturer produces \var{P} different parts using \var{M} different machines.
- Batch of 100 part \var{p} requires \var{time_{m,p}} hours on machine \var{m}.
- The division incurs a charge of \var{cost_{m}} per hour for using machine \var{m}.
- Machine \var{m} has an availability of up to \var{available_{m}} hours per month.
- The division sells part \var{p} in batches of 100 at price of \var{price_{p}} per batch.
- Machine \var{1} requires a setup time of \var{setup_time_{p}} hours before it can be used for each part \var{p}.
- Other machines do not require a setup time.
- There are no minimum production quantities for any part.

INPUT FORMAT: 

{
    "time_required": [[time_{m,p} for p in 1, ..., P] for m in 1, ..., M],
    "machine_costs": [cost_{m} for m in 1, ..., M],
    "availability": [available_{m} for m in 1, ..., M],
    "prices": [price_{p} for p in 1, ..., P],
    "setup_time": [setup_time_{p} for p in 1, ..., P]
}

OBJECTIVE: How many batches of each part should the manufacturer produce each month to maximize profit?

OUTPUT INFO:

- the number of batches of each part produced \var{batches_{p}}.
- \var{setup_flags_{p}} indicates whether \var{part_{p}} is set up or not.
- \var{total_profit} represents the total profit obtained for the month.

OUTPUT FORMAT:

{
    "batches": [batches_{p} for p in 1, ..., P],
    "setup_flags": [setup_flag_{p} for p in 1, ..., P],
    "total_profit": total_profit
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Mathematical Model for Auto Parts Production}
\author{}
\date{}
\maketitle

\section*{Variables}
\begin{itemize}
    \item Let \(batches_{p}\) be the number of batches produced for part \(p\), where \(p = 1, \ldots, P\).
    \item Let \(setup\_flags_{p}\) be a binary variable indicating whether part \(p\) is set up (\(setup\_flags_{p} = 1\)) or not (\(setup\_flags_{p} = 0\)).
    \item Let \(total\_profit\) represent the total profit obtained for the month.
\end{itemize}

\section*{Parameters}
\begin{itemize}
    \item \(time_{m,p}\): time required on machine \(m\) to produce one batch of part \(p\).
    \item \(cost_{m}\): cost per hour for using machine \(m\).
    \item \(available_{m}\): available hours per month for machine \(m\).
    \item \(price_{p}\): selling price per batch of part \(p\).
    \item \(setup\_time_{p}\): setup time required for machine 1 to produce part \(p\).
\end{itemize}

\section*{Objective Function}
\[
\text{Maximize } total\_profit = \sum_{p=1}^{P} (price_{p} \cdot batches_{p}) - \sum_{m=1}^{M} \left( cost_{m} \cdot \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \right)
\]

\section*{Constraints}
\begin{align*}
1. & \quad \sum_{p=1}^{P} (time_{1,p} \cdot batches_{p}) + \sum_{p=1}^{P} (setup\_flags_{p} \cdot setup\_time_{p}) \leq available_{1} \\
2. & \quad \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \leq available_{m}, \quad \forall m = 2, \ldots, M \\
3. & \quad batches_{p} \geq 0, \quad \forall p = 1, \ldots, P \\
4. & \quad setup\_flags_{p} \in \{0, 1\}, \quad \forall p = 1, \ldots, P
\end{align*}

\section*{Output}
The output of the model will provide:
\begin{itemize}
    \item \(batches = [batches_{p} \text{ for } p = 1, \ldots, P]\)
    \item \(setup\_flags = [setup\_flags_{p} \text{ for } p = 1, \ldots, P]\)
    \item \(total\_profit\)
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

\title{Mathematical Model for Auto Parts Production}
\author{}
\date{}
\maketitle

\section*{Variables}
\begin{itemize}
    \item Let \(batches_{p}\) be the number of batches produced for part \(p\), where \(p = 1, \ldots, P\).
    \item Let \(setup\_flags_{p}\) be a binary variable indicating whether part \(p\) is set up (\(setup\_flags_{p} = 1\)) or not (\(setup\_flags_{p} = 0\)).
    \item Let \(total\_profit\) represent the total profit obtained for the month.
\end{itemize}

\section*{Parameters}
\begin{itemize}
    \item \(time_{m,p}\): time required on machine \(m\) to produce one batch of part \(p\).
    \item \(cost_{m}\): cost per hour for using machine \(m\).
    \item \(available_{m}\): available hours per month for machine \(m\).
    \item \(price_{p}\): selling price per batch of part \(p\).
    \item \(setup\_time_{p}\): setup time required for machine 1 to produce part \(p\).
\end{itemize}

\section*{Objective Function}
\[
\text{Maximize } total\_profit = \sum_{p=1}^{P} (price_{p} \cdot batches_{p}) - \sum_{m=1}^{M} \left( cost_{m} \cdot \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \right)
\]

\section*{Constraints}
\begin{align*}
1. & \quad \sum_{p=1}^{P} (time_{1,p} \cdot batches_{p}) + \sum_{p=1}^{P} (setup\_flags_{p} \cdot setup\_time_{p}) \leq available_{1} \\
2. & \quad \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \leq available_{m}, \quad \forall m = 2, \ldots, M \\
3. & \quad batches_{p} \geq 0, \quad \forall p = 1, \ldots, P \\
4. & \quad setup\_flags_{p} \in \{0, 1\}, \quad \forall p = 1, \ldots, P
\end{align*}

\section*{Output}
The output of the model will provide:
\begin{itemize}
    \item \(batches = [batches_{p} \text{ for } p = 1, \ldots, P]\)
    \item \(setup\_flags = [setup\_flags_{p} \text{ for } p = 1, \ldots, P]\)
    \item \(total\_profit\)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'setup_time': [12, 8, 4, 0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data from JSON
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "setup_time": [12, 8, 4, 0]}')

#### Define the parameters based on the input data
time_required = data['time_required']  #### time[m][p]
machine_costs = data['machine_costs']  #### cost[m]
availability = data['availability']      #### available[m]
prices = data['prices']                  #### price[p]
setup_time = data['setup_time']          #### setup_time[p]

#### Number of parts and machines
P = len(prices)      #### Number of parts
M = len(machine_costs)  #### Number of machines

#### Create the problem
problem = pulp.LpProblem("Auto_Parts_Production", pulp.LpMaximize)

#### Define decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')
setup_flags = pulp.LpVariable.dicts("setup_flags", range(P), cat='Binary')

#### Objective function
profit_expr = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
              pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M))

problem += profit_expr, "Total_Profit"

#### Constraints
#### Machine 1 constraint (includes setup time)
problem += (pulp.lpSum(time_required[0][p] * batches[p] for p in range(P)) +
             pulp.lpSum(setup_flags[p] * setup_time[p] for p in range(P))) <= availability[0], "Machine_1_Availability")

#### Other machine constraints
for m in range(1, M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Machine_{m+1}_Availability"

#### Setup flags and batches constraints
for p in range(P):
    problem += batches[p] >= 0, f"Batches_NonNegativity_{p+1}"
    problem += setup_flags[p] >= 0, f"SetupFlags_0_1_{p+1}"
    problem += setup_flags[p] <= 1, f"SetupFlags_0_1_Upper_{p+1}"

#### Solve the problem
problem.solve()

#### Output results
batches_result = [batches[p].varValue for p in range(P)]
setup_flags_result = [setup_flags[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

print(f'Batches: {batches_result}')
print(f'Setup Flags: {setup_flags_result}')
print(f'Total Profit: {total_profit}')
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')
```

