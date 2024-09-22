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
To solve this problem, we need to formulate it as a Mixed Integer Programming (MIP) model. We will define the binary decision variables `isoperated_{k, i}` to represent whether mine \( k \) is operated in year \( i \), and continuous decision variables `amount_{k, i}` to represent the amount of ore produced by mine \( k \) in year \( i \). The objective is to maximize the net present value of the profit over the years, considering royalties and production limits, while meeting ore quality requirements.

Here's the mathematical model represented in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\usepackage{amssymb}
\begin{document}

\section*{Mathematical Model}

\subsection*{Sets and Indices}
\begin{align*}
& K: \text{Set of mines, indexed by } k, \, k = 1, \ldots, n\_mines \\
& I: \text{Set of years, indexed by } i
\end{align*}

\subsection*{Parameters}
\begin{align*}
& n\_maxwork \in \mathbb{Z}_+: \text{Maximum number of mines that can be operated in any year} \\
& \text{royalty}_{k} \in \mathbb{R}_+: \text{Yearly royalty for mine } k \\
& \text{limit}_{k} \in \mathbb{R}_+: \text{Production limit of mine } k \text{ per year} \\
& \text{quality}_{k} \in \mathbb{R}_+: \text{Quality of ore from mine } k \\
& \text{requiredquality}_{i} \in \mathbb{R}_+: \text{Required ore quality in year } i \\
& \text{price} \in \mathbb{R}_+: \text{Revenue per ton of ore sold} \\
& \text{discount} \in [0, 1]: \text{Discount rate per annum}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
& \text{isoperated}_{k,i} \in \{0, 1\}: \text{1 if mine } k \text{ is operated in year } i, \text{0 otherwise} \\
& \text{amount}_{k,i} \in \mathbb{R}_+: \text{Amount of ore produced by mine } k \text{ in year } i
\end{align*}

\subsection*{Objective Function}
Maximize the net present value (NPV) of profit:
\begin{align*}
\max \sum_{i \in I} \frac{1}{(1 + \text{discount})^i} \left( \text{price} \times \sum_{k=1}^{n\_mines} \text{amount}_{k,i} - \sum_{k=1}^{n\_mines} \text{royalty}_{k} \times \text{isoperated}_{k,i} \right)
\end{align*}

\subsection*{Constraints}
\begin{align*}
& \sum_{k=1}^{n\_mines} \text{isoperated}_{k,i} \leq n\_maxwork, \quad \forall i \in I \quad \text{(maximum mines per year)} \\
& \text{amount}_{k,i} \leq \text{limit}_{k} \times \text{isoperated}_{k,i}, \quad \forall k \in K, \, \forall i \in I \quad \text{(production limit)} \\
& \sum_{k=1}^{n\_mines} \text{quality}_{k} \times \text{amount}_{k,i} = \text{requiredquality}_{i} \times \sum_{k=1}^{n\_mines} \text{amount}_{k,i}, \quad \forall i \in I \quad \text{(quality requirement)} \\
& \text{isoperated}_{k,i} = 1 \quad \text{implies} \quad \text{isoperated}_{k,i-1} = 1, \, \forall k \in K, \, \forall i \in I, \, i > 1 \quad \text{(opening requirement)}
\end{align*}

\end{document}
```

This model aims to maximize the total discounted profit from the operation of the mines over the years, subject to constraints on the number of mines operating, production limits, and required quality of ore. The royalty payments are only made for mines that are kept open for potential future operation.

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

\section*{Mathematical Model}

\subsection*{Sets and Indices}
\begin{align*}
& K: \text{Set of mines, indexed by } k, \, k = 1, \ldots, n\_mines \\
& I: \text{Set of years, indexed by } i
\end{align*}

\subsection*{Parameters}
\begin{align*}
& n\_maxwork \in \mathbb{Z}_+: \text{Maximum number of mines that can be operated in any year} \\
& \text{royalty}_{k} \in \mathbb{R}_+: \text{Yearly royalty for mine } k \\
& \text{limit}_{k} \in \mathbb{R}_+: \text{Production limit of mine } k \text{ per year} \\
& \text{quality}_{k} \in \mathbb{R}_+: \text{Quality of ore from mine } k \\
& \text{requiredquality}_{i} \in \mathbb{R}_+: \text{Required ore quality in year } i \\
& \text{price} \in \mathbb{R}_+: \text{Revenue per ton of ore sold} \\
& \text{discount} \in [0, 1]: \text{Discount rate per annum}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
& \text{isoperated}_{k,i} \in \{0, 1\}: \text{1 if mine } k \text{ is operated in year } i, \text{0 otherwise} \\
& \text{amount}_{k,i} \in \mathbb{R}_+: \text{Amount of ore produced by mine } k \text{ in year } i
\end{align*}

\subsection*{Objective Function}
Maximize the net present value (NPV) of profit:
\begin{align*}
\max \sum_{i \in I} \frac{1}{(1 + \text{discount})^i} \left( \text{price} \times \sum_{k=1}^{n\_mines} \text{amount}_{k,i} - \sum_{k=1}^{n\_mines} \text{royalty}_{k} \times \text{isoperated}_{k,i} \right)
\end{align*}

\subsection*{Constraints}
\begin{align*}
& \sum_{k=1}^{n\_mines} \text{isoperated}_{k,i} \leq n\_maxwork, \quad \forall i \in I \quad \text{(maximum mines per year)} \\
& \text{amount}_{k,i} \leq \text{limit}_{k} \times \text{isoperated}_{k,i}, \quad \forall k \in K, \, \forall i \in I \quad \text{(production limit)} \\
& \sum_{k=1}^{n\_mines} \text{quality}_{k} \times \text{amount}_{k,i} = \text{requiredquality}_{i} \times \sum_{k=1}^{n\_mines} \text{amount}_{k,i}, \quad \forall i \in I \quad \text{(quality requirement)} \\
& \text{isoperated}_{k,i} = 1 \quad \text{implies} \quad \text{isoperated}_{k,i-1} = 1, \, \forall k \in K, \, \forall i \in I, \, i > 1 \quad \text{(opening requirement)}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'n_mines': 4, 'n_maxwork': 3, 'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0], 'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0], 'quality': [1.0, 0.7, 1.5, 0.5], 'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0], 'price': 10, 'discount': 0.1}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data input
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

#### Initialize the problem
problem = pulp.LpProblem("Maximize_NPV", pulp.LpMaximize)

#### Decision Variables
isoperated = pulp.LpVariable.dicts("isoperated", (range(data['n_mines']), range(len(data['requiredquality']))), cat='Binary')
amount = pulp.LpVariable.dicts("amount", (range(data['n_mines']), range(len(data['requiredquality']))), lowBound=0)

#### Objective Function: Maximize NPV
nv_terms = []
for i in range(len(data['requiredquality'])):
    present_value = (data['price'] * pulp.lpSum(amount[k][i] for k in range(data['n_mines'])) - 
                     pulp.lpSum(data['royalty'][k] * isoperated[k][i] for k in range(data['n_mines']))) / ((1 + data['discount']) ** i)
    nv_terms.append(present_value)
problem += pulp.lpSum(nv_terms)

#### Constraints
#### Maximum number of mines operated per year
for i in range(len(data['requiredquality'])):
    problem += pulp.lpSum(isoperated[k][i] for k in range(data['n_mines'])) <= data['n_maxwork']

#### Production limits
for k in range(data['n_mines']):
    for i in range(len(data['requiredquality'])):
        problem += amount[k][i] <= data['limit'][k] * isoperated[k][i]

#### Quality requirement
for i in range(len(data['requiredquality'])):
    problem += pulp.lpSum(data['quality'][k] * amount[k][i] for k in range(data['n_mines'])) == data['requiredquality'][i] * pulp.lpSum(amount[k][i] for k in range(data['n_mines']))

#### Opening requirement
for k in range(data['n_mines']):
    for i in range(1, len(data['requiredquality'])):
        problem += isoperated[k][i] <= isoperated[k][i-1]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

