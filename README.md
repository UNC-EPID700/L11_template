# L11

Date Assigned: 2024-10-02

Using the built-in dataset `SASHELP.HEART`, save the 5, 10, 15, 20, 25, and 30 year risk of a composite outcome of CHD Diagnosis or Death from any cause. Place the new datasets into the `results` folder with the name `heart_5y`, `heart_10y`, ..., `heart_30y` and call the risk indicators `risk_5y`, `risk_10y`, ..., `risk_30y`. Use Macro Variables to reduce the overall number of times you rewrite code. 

- Update the `%INCLUDE` statements in the file `code/create_datasets.sas` so that the code file `code/L11.sas` runs. Do not change any of the `%LET` statements.
- Towards creating the risk indicator:
  - Code the example without a macro variable first - say, for the 5 year risk.
  - Because there is no LTFU, then `risk_5y` will be 1 when `(AgeCHDdiag - AgeAtStart) <= 5` or `(AgeAtDeath - AgeAtStart) <= 5`, and 0 otherwise. Remember to check for missingness!
  - Save this into a permanent dataset called `heart_5y`.
  - To extract a macro variable, replace any reference to the duration (in this case, `5`) with our macro variable (`&years.`). Be sure to do this everywhere - the DATA step name, the subtraction step, and the new variable name.
  - Brownie points for checking your code and checking that it runs correctly.
- When you are finished, run the entire `code/create_datasets.sas` file one more time. Place the resulting datasets into the `results` folder.


## Grading

10 points for each correct dataset; 40 points for using macros. The 40 point check will be automated; if you used macro variables and it is giving you fits, know that I will change it later. 


