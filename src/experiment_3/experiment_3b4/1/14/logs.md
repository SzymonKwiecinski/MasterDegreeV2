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
To model the problem as a Linear Programming (LP) problem, we need to define decision variables, the objective function, and constraints. Below is the formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\title{Linear Programming Model for Maximizing Net Income}
\author{Operations Research Model}
\date{}
\maketitle

\section*{Problem Formulation}

Given the input parameters:
\begin{itemize}
    \item $P$: number of products
    \item $\text{cash}$: available cash
    \item $\text{hour}_i$: machine hours required per unit of product $i$
    \item $\text{cost}_i$: production cost per unit of product $i$
    \item $\text{price}_i$: selling price per unit of product $i$
    \item $\text{investPercentage}_i$: fraction of sales revenue reinvested for product $i$
    \item $\text{upgradeHours}$: additional machine hours available after upgrade
    \item $\text{upgradeCost}$: cost of upgrading machine capacity
    \item $\text{availableHours}$: current machine hours available
\end{itemize}

Define decision variables:
\begin{itemize}
    \item $x_i$: production quantity of product $i$ for $i = 1, \ldots, P$
    \item $y$: binary variable for machine upgrade ($y = 1$ if upgrade, $y = 0$ if no upgrade)
\end{itemize}

The objective is to maximize the total net income:
\begin{align*}
    \text{Maximize } Z = \sum_{i=1}^{P} \left( (\text{price}_i - \text{cost}_i - \text{investPercentage}_i \cdot \text{price}_i) \cdot x_i \right) - y \cdot \text{upgradeCost}
\end{align*}

Subject to the constraints:
\begin{itemize}
    \item Cash availability constraint:
    \begin{align*}
        \sum_{i=1}^{P} \text{cost}_i \cdot x_i \leq \text{cash} + \sum_{i=1}^{P} \text{investPercentage}_i \cdot \text{price}_i \cdot x_i
    \end{align*}
    \item Machine capacity constraint:
    \begin{align*}
        \sum_{i=1}^{P} \text{hour}_i \cdot x_i \leq \text{availableHours} + y \cdot \text{upgradeHours}
    \end{align*}
    \item Non-negativity and binary constraints:
    \begin{align*}
        x_i &\geq 0 \quad \text{for all } i = 1, \ldots, P \\
        y &\in \{0, 1\}
    \end{align*}
\end{itemize}

\section*{Conclusion}

The above LP should be solved to determine the optimal production quantities $x_i$ for each product and whether or not to upgrade the machine capacity ($y$). The solution will maximize the total net income $Z$.

\end{document}
```

This LaTeX model describes the linear programming problem for maximizing net income, considering cash and machine capacity constraints, and the decision on whether to upgrade machine hours. The objective function accounts for the net income from sales, subtracting production and investment costs, and the potential upgrade cost.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\title{Linear Programming Model for Maximizing Net Income}
\author{Operations Research Model}
\date{}
\maketitle

\section*{Problem Formulation}

Given the input parameters:
\begin{itemize}
    \item $P$: number of products
    \item $\text{cash}$: available cash
    \item $\text{hour}_i$: machine hours required per unit of product $i$
    \item $\text{cost}_i$: production cost per unit of product $i$
    \item $\text{price}_i$: selling price per unit of product $i$
    \item $\text{investPercentage}_i$: fraction of sales revenue reinvested for product $i$
    \item $\text{upgradeHours}$: additional machine hours available after upgrade
    \item $\text{upgradeCost}$: cost of upgrading machine capacity
    \item $\text{availableHours}$: current machine hours available
\end{itemize}

Define decision variables:
\begin{itemize}
    \item $x_i$: production quantity of product $i$ for $i = 1, \ldots, P$
    \item $y$: binary variable for machine upgrade ($y = 1$ if upgrade, $y = 0$ if no upgrade)
\end{itemize}

The objective is to maximize the total net income:
\begin{align*}
    \text{Maximize } Z = \sum_{i=1}^{P} \left( (\text{price}_i - \text{cost}_i - \text{investPercentage}_i \cdot \text{price}_i) \cdot x_i \right) - y \cdot \text{upgradeCost}
\end{align*}

Subject to the constraints:
\begin{itemize}
    \item Cash availability constraint:
    \begin{align*}
        \sum_{i=1}^{P} \text{cost}_i \cdot x_i \leq \text{cash} + \sum_{i=1}^{P} \text{investPercentage}_i \cdot \text{price}_i \cdot x_i
    \end{align*}
    \item Machine capacity constraint:
    \begin{align*}
        \sum_{i=1}^{P} \text{hour}_i \cdot x_i \leq \text{availableHours} + y \cdot \text{upgradeHours}
    \end{align*}
    \item Non-negativity and binary constraints:
    \begin{align*}
        x_i &\geq 0 \quad \text{for all } i = 1, \ldots, P \\
        y &\in \{0, 1\}
    \end{align*}
\end{itemize}

\section*{Conclusion}

The above LP should be solved to determine the optimal production quantities $x_i$ for each product and whether or not to upgrade the machine capacity ($y$). The solution will maximize the total net income $Z$.

\end{document}</MATH_MODEL>
<DATA>
{'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data extracted from the JSON provided
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

#### Problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['P'])]
y = pulp.LpVariable('y', cat='Binary')

#### Objective Function
profit_terms = [(data['Price'][i] - data['Cost'][i] - data['InvestPercentage'][i] * data['Price'][i]) * x[i] for i in range(data['P'])]
problem += pulp.lpSum(profit_terms) - y * data['UpgradeCost']

#### Cash availability constraint
cash_constraint = [
    data['Cost'][i] * x[i] for i in range(data['P'])
]
invest_revenue = [
    data['InvestPercentage'][i] * data['Price'][i] * x[i] for i in range(data['P'])
]
problem += pulp.lpSum(cash_constraint) <= data['Cash'] + pulp.lpSum(invest_revenue)

#### Machine capacity constraint
machine_hours = [
    data['Hour'][i] * x[i] for i in range(data['P'])
]
problem += pulp.lpSum(machine_hours) <= data['AvailableHours'] + y * data['UpgradeHours']

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

