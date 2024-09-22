# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO: 

- A company produces and sells \var{P} different products. 
- The demand for each product is unlimited, but the company is constrained by cash availability and machine capacity.
- Each unit of the \var{i}-th product requires \var{hour_i} machine hours.
- There are \var{availableHours} machine hours available in the current production period.
- The production costs are \var{cost_i} per unit of the \var{i}-th product.
- The selling prices of the \var{i}-th product is \var{price_i} per unit.
- The available cash is \var{cash}.
- Furthermore, \var{investRate_i} of the sales revenues from the \var{i}-th product will be made available to finance operations during the current period.
- \var{investPercentage_i} is a number between 0 and 1
- The company could increase its available machine hours by \var{upgradeHours}, after spending \var{upgradeCost} for certain repairs. 
- The net income from each product is the revenue we get from selling it minus the production cost and the investment cost.

INPUT FORMAT:

{
    "cash": cash,
    "hour": [hour_i for i in 1, ..., P],
    "cost": [cost_i for i in 1, ..., P],
    "price": [price_i for i in 1, ..., P],
    "investPercentage": [investPercentage_i for i in 1, ..., P],
    "upgradeHours": upgradeHours,   
    "upgradeCost": upgradeCost,
    "availableHours": availableHours,
}

OBJECTIVE: We are aiming at maximizing total net income subject to the cash availability and machine capacity limitations

OUTPUT INFO:

- \var{net_income} shows the net income of the company
- \var{production_i} shows the production quantity of the \var{i}-th product
- \var{upgrade} is a boolean variable that shows whether the company should upgrade its machine capacity or not

OUTPUT FORMAT:

{
    "net_income": net_income,
    "production": [production_i for i in 1, ..., P],
    "upgrade": true/false,
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To formulate this problem as a linear programming model, we need to consider the constraints related to cash availability and machine capacity, as well as the objective of maximizing the total net income. 

Here's the mathematical model:

1. **Decision Variables:**
   - \( x_i \): the production quantity of the \( i \)-th product
   - \( u \): a binary variable indicating if the machine capacity is upgraded (1 if upgraded, 0 otherwise)

2. **Objective Function:**
   Maximize the total net income:
   \[
   \text{Maximize } Z = \sum_{i=1}^{P} \left(\text{price}_i \cdot x_i - \text{cost}_i \cdot x_i - \text{investPercentage}_i \cdot \text{price}_i \cdot x_i\right) - \text{upgradeCost} \cdot u
   \]

3. **Constraints:**
   - Cash availability:
     \[
     \sum_{i=1}^{P} \left(\text{cost}_i \cdot x_i\right) \leq \text{cash} + \sum_{i=1}^{P} \left(\text{investPercentage}_i \cdot \text{price}_i \cdot x_i\right)
     \]
   - Machine hours capacity:
     \[
     \sum_{i=1}^{P} \left(\text{hour}_i \cdot x_i\right) \leq \text{availableHours} + \text{upgradeHours} \cdot u
     \]
   - \( u \) is binary:
     \[
     u \in \{0, 1\}
     \]
   - Non-negativity:
     \[
     x_i \geq 0 \quad \text{for all } i
     \]

Let's put this model into a LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\textbf{Decision Variables:}
\begin{itemize}
    \item $x_i$: production quantity of the $i$-th product
    \item $u$: binary variable indicating machine capacity upgrade ($1$ if upgraded, $0$ otherwise)
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{i=1}^{P} \left(\text{price}_i \cdot x_i - \text{cost}_i \cdot x_i - \text{investPercentage}_i \cdot \text{price}_i \cdot x_i\right) - \text{upgradeCost} \cdot u
\]

\textbf{Subject to:}
\begin{align*}
    & \sum_{i=1}^{P} \left(\text{cost}_i \cdot x_i\right) \leq \text{cash} + \sum_{i=1}^{P} \left(\text{investPercentage}_i \cdot \text{price}_i \cdot x_i\right) \quad & (\text{Cash Constraint}) \\
    & \sum_{i=1}^{P} \left(\text{hour}_i \cdot x_i\right) \leq \text{availableHours} + \text{upgradeHours} \cdot u \quad & (\text{Machine Hours Constraint}) \\
    & u \in \{0, 1\} \quad & (\text{Binary Upgrade Variable}) \\
    & x_i \geq 0 \quad \text{for all } i \quad & (\text{Non-negativity Constraint})
\end{align*}

\end{document}
```

This LaTeX document models the problem, providing decision variables, objective function, and constraints. After solving this linear programming model, we can find the optimal production quantities \( x_i \) and whether to upgrade the machine capacity \( u \), which respectively determine the net income and the decision related to upgrading.

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
    \item $x_i$: production quantity of the $i$-th product
    \item $u$: binary variable indicating machine capacity upgrade ($1$ if upgraded, $0$ otherwise)
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{i=1}^{P} \left(\text{price}_i \cdot x_i - \text{cost}_i \cdot x_i - \text{investPercentage}_i \cdot \text{price}_i \cdot x_i\right) - \text{upgradeCost} \cdot u
\]

\textbf{Subject to:}
\begin{align*}
    & \sum_{i=1}^{P} \left(\text{cost}_i \cdot x_i\right) \leq \text{cash} + \sum_{i=1}^{P} \left(\text{investPercentage}_i \cdot \text{price}_i \cdot x_i\right) \quad & (\text{Cash Constraint}) \\
    & \sum_{i=1}^{P} \left(\text{hour}_i \cdot x_i\right) \leq \text{availableHours} + \text{upgradeHours} \cdot u \quad & (\text{Machine Hours Constraint}) \\
    & u \in \{0, 1\} \quad & (\text{Binary Upgrade Variable}) \\
    & x_i \geq 0 \quad \text{for all } i \quad & (\text{Non-negativity Constraint})
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'P': 2, 
    'Cash': 3000, 
    'Hour': [2, 6], 
    'Cost': [3, 2], 
    'Price': [6, 5], 
    'InvestPercentage': [0.4, 0.3], 
    'UpgradeHours': 2000, 
    'UpgradeCost': 400, 
    'AvailableHours': 2000
}

#### Create the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(data['P']), lowBound=0)  #### production quantity of products
u = pulp.LpVariable("u", cat='Binary')  #### binary variable for machine upgrade

#### Objective Function
problem += pulp.lpSum((data['Price'][i] * x[i] - 
                        data['Cost'][i] * x[i] - 
                        data['InvestPercentage'][i] * data['Price'][i] * x[i]) for i in range(data['P'])) - data['UpgradeCost'] * u, "Total_Profit"

#### Constraints
#### Cash Constraint
problem += pulp.lpSum(data['Cost'][i] * x[i] for i in range(data['P'])) <= data['Cash'] + \
            pulp.lpSum(data['InvestPercentage'][i] * data['Price'][i] * x[i] for i in range(data['P'])), "Cash_Constraint"

#### Machine Hours Constraint
problem += pulp.lpSum(data['Hour'][i] * x[i] for i in range(data['P'])) <= data['AvailableHours'] + data['UpgradeHours'] * u, "Machine_Hours_Constraint"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

