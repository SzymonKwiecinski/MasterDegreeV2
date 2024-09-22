# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MIP
PROBLEM INFO:

- A mining company is going to continue operating in a certain area for the next years. 
- There are \var{n_mines} mines in this area, but it can operate at most \var{n_maxwork} in any one year. 
- Although a mine may not operate in a certain year, it is still necessary to keep it ‘open’, in the sense that royalties are payable, if it be operated in a future year. 
- Clearly, if a mine is not going to be worked again, it can be permanently closed down and no more royalties need be paid. 
- The yearly royalties payable on each mine kept ‘open’ is \var{royalty_{k}} for mine \var{k}.
- There is an upper limit to the amount of ore, which can be extracted from each mine in a year. 
- The upper limit for mine \var{k} is \var{limit_{k}}.
- The ore from the different mines is of varying quality.
- This quality is measured on a scale so that blending ores together results in a linear combination of the quality measurements, for example, if equal quantities of two ores were combined, the resultant ore would have a quality measurement half way between
that of the ingredient ores. 
- The quality of ore from mine \var{k} is \var{quality_{k}}.
- In each year, it is necessary to combine the total outputs from each mine to produce a blended ore of exactly some stipulated quality.
- In year \var{i}, the required quality is \var{requiredquality_{i}}.
- The final blended ore sells for \var{price} ton each year. 
- Revenue and expenditure for future years must be discounted at a rate of \var{discount} per annum.

INPUT FORMAT:

{
    "n_mines": n_mines,
    "n_maxwork": n_maxwork,
    "royalty": [royalty_{k} for k in 1,...,K],
    "limit": [limit_{k} for k in 1,...,K],
    "quality": [quality_{k} for k in 1,...,K],
    "requiredquality": [requiredquality_{i} for i in 1,...,I],
    "price": price,
    "discount": discount
}


OBJECTIVE: To maximize profit, which mines should be operated each year and how much should they produce?

OUTPUT INFO:

- \var{isoperated} represents whether each mine is operated in each year
- \var{amount} represents the amount of ore produced by each mine in each year

OUTPUT FORMAT:

{
    "isoperated": [[isoperated_{k, i} for i in 1,...,I] for k in 1,...K]
    "amount": [[amount_{k, i} for i in 1,...,I] for k in 1,...K]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To solve this problem, we need to construct a Mixed-Integer Programming (MIP) model that will help us determine which mines to operate in each year and how much ore to produce to maximize profit. Here is the mathematical formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\usepackage{amssymb}

\begin{document}

\section*{Mixed-Integer Programming Formulation}

\subsection*{Indices and Sets}
\begin{align*}
k & : \text{Index for mines, } k = 1, 2, \ldots, n_{\text{mines}} \\
i & : \text{Index for years, } i = 1, 2, \ldots, I \\
\end{align*}

\subsection*{Parameters}
\begin{align*}
\text{n\_maxwork} & : \text{Maximum number of mines that can operate in one year} \\
\text{royalty}_k & : \text{Yearly royalty payable for keeping mine } k \text{ open} \\
\text{limit}_k & : \text{Maximum amount of ore that can be extracted from mine } k \text{ in a year} \\
\text{quality}_k & : \text{Quality measurement of ore from mine } k \\
\text{requiredquality}_i & : \text{Required quality of blended ore in year } i \\
\text{price} & : \text{Selling price per ton of ore} \\
\text{discount} & : \text{Discount rate for future profits} \\
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
\text{isoperated}_{k,i} & : 
\begin{cases} 
1, & \text{if mine } k \text{ is operated in year } i \\
0, & \text{otherwise}
\end{cases} \\
\text{amount}_{k,i} & : \text{Amount of ore produced by mine } k \text{ in year } i \\
\end{align*}

\subsection*{Objective Function}
Maximize the discounted profit:
\begin{align*}
\max \; & \sum_{i=1}^{I} \frac{1}{(1 + \text{discount})^i} \left( \sum_{k=1}^{n_{\text{mines}}} \text{price} \times \text{amount}_{k,i} - \text{royalty}_k \times \text{isoperated}_{k,i} \right)
\end{align*}

\subsection*{Constraints}
\begin{align*}
\text{Quality Constraint:} & \quad \sum_{k=1}^{n_{\text{mines}}} \text{quality}_k \times \text{amount}_{k,i} = \text{requiredquality}_i \times \sum_{k=1}^{n_{\text{mines}}} \text{amount}_{k,i}, \quad \forall i \\
\text{Production Limit:} & \quad \text{amount}_{k,i} \leq \text{limit}_k \times \text{isoperated}_{k,i}, \quad \forall k, \forall i \\
\text{Maximum Operating Mines:} & \quad \sum_{k=1}^{n_{\text{mines}}} \text{isoperated}_{k,i} \leq \text{n\_maxwork}, \quad \forall i \\
\end{align*}

\end{document}
```

This LaTeX code describes an MIP model with:
- Decision variables for whether a mine is operated and how much it produces.
- An objective function to maximize the discounted profit from selling ore, subtracting royalties.
- Constraints to ensure the blended ore meets quality requirements, production does not exceed mine limits, and at most a fixed number of mines operate each year.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\usepackage{amssymb}

\begin{document}

\section*{Mixed-Integer Programming Formulation}

\subsection*{Indices and Sets}
\begin{align*}
k & : \text{Index for mines, } k = 1, 2, \ldots, n_{\text{mines}} \\
i & : \text{Index for years, } i = 1, 2, \ldots, I \\
\end{align*}

\subsection*{Parameters}
\begin{align*}
\text{n\_maxwork} & : \text{Maximum number of mines that can operate in one year} \\
\text{royalty}_k & : \text{Yearly royalty payable for keeping mine } k \text{ open} \\
\text{limit}_k & : \text{Maximum amount of ore that can be extracted from mine } k \text{ in a year} \\
\text{quality}_k & : \text{Quality measurement of ore from mine } k \\
\text{requiredquality}_i & : \text{Required quality of blended ore in year } i \\
\text{price} & : \text{Selling price per ton of ore} \\
\text{discount} & : \text{Discount rate for future profits} \\
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
\text{isoperated}_{k,i} & : 
\begin{cases} 
1, & \text{if mine } k \text{ is operated in year } i \\
0, & \text{otherwise}
\end{cases} \\
\text{amount}_{k,i} & : \text{Amount of ore produced by mine } k \text{ in year } i \\
\end{align*}

\subsection*{Objective Function}
Maximize the discounted profit:
\begin{align*}
\max \; & \sum_{i=1}^{I} \frac{1}{(1 + \text{discount})^i} \left( \sum_{k=1}^{n_{\text{mines}}} \text{price} \times \text{amount}_{k,i} - \text{royalty}_k \times \text{isoperated}_{k,i} \right)
\end{align*}

\subsection*{Constraints}
\begin{align*}
\text{Quality Constraint:} & \quad \sum_{k=1}^{n_{\text{mines}}} \text{quality}_k \times \text{amount}_{k,i} = \text{requiredquality}_i \times \sum_{k=1}^{n_{\text{mines}}} \text{amount}_{k,i}, \quad \forall i \\
\text{Production Limit:} & \quad \text{amount}_{k,i} \leq \text{limit}_k \times \text{isoperated}_{k,i}, \quad \forall k, \forall i \\
\text{Maximum Operating Mines:} & \quad \sum_{k=1}^{n_{\text{mines}}} \text{isoperated}_{k,i} \leq \text{n\_maxwork}, \quad \forall i \\
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'n_mines': 4, 'n_maxwork': 3, 'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 'quality': [1.0, 0.7, 1.5, 0.5], 'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 'price': 10, 'discount': 0.1}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'n_mines': 4,
    'n_maxwork': 3,
    'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0],
    'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0],
    'quality': [1.0, 0.7, 1.5, 0.5],
    'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0],
    'price': 10,
    'discount': 0.1
}

n_mines = data['n_mines']
n_maxwork = data['n_maxwork']
royalty = data['royalty']
limit = data['limit']
quality = data['quality']
requiredquality = data['requiredquality']
price = data['price']
discount = data['discount']
I = len(requiredquality)

#### Initialize problem
problem = pulp.LpProblem("Maximize_Discounted_Profit", pulp.LpMaximize)

#### Decision Variables
isoperated = pulp.LpVariable.dicts("isoperated", ((k, i) for k in range(n_mines) for i in range(I)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", ((k, i) for k in range(n_mines) for i in range(I)), lowBound=0, cat='Continuous')

#### Objective Function
problem += pulp.lpSum((1 / (1 + discount) ** i) * (pulp.lpSum(price * amount[k, i] - royalty[k] * isoperated[k, i] for k in range(n_mines)))
                      for i in range(I))

#### Constraints

#### Quality Constraint
for i in range(I):
    problem += (pulp.lpSum(quality[k] * amount[k, i] for k in range(n_mines)) == 
                requiredquality[i] * pulp.lpSum(amount[k, i] for k in range(n_mines)))

#### Production Limit
for k in range(n_mines):
    for i in range(I):
        problem += amount[k, i] <= limit[k] * isoperated[k, i]

#### Maximum Operating Mines
for i in range(I):
    problem += pulp.lpSum(isoperated[k, i] for k in range(n_mines)) <= n_maxwork

#### Solve the problem
status = problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

