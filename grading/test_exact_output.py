import io
import os
import pandas as pd
from grading.crypt_answers import decrypt
from grading import KEY

DECIMAL_PLACES = 5
N_MISMATCHES = 5

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def test_exact_output(answer_path, files):
    filelist = files.replace("[", "").replace("]", "").split(",")
    answerlist = answer_path.replace("[", "").replace("]", "").split(",")
    
    for answer, f in zip(answerlist, filelist): 
        answer_bytes = decrypt(encryptedpath=answer, key=KEY)
        answer_df: pd.DataFrame = pd.read_sas(io.BytesIO(answer_bytes), format="sas7bdat").round(DECIMAL_PLACES)

        # Finally, check the answers.
        # First, check that all the columns are present.
        # Alteration 2023-09-19: case insensitive input needed.
        # Alteration 2023-11-19: added columns to check
        cols_to_check = answer_df.columns.str.lower()

        student_file = f"results/{f}.sas7bdat"
        assert os.path.exists(student_file), f"File '{student_file}' is missing from results folder. Does the file exist?"
        
        student_df = pd.read_sas(student_file, format="sas7bdat").round(DECIMAL_PLACES)
        answer_student_columns = set(student_df.columns.str.lower())

        assert all(
            col in answer_student_columns for col in cols_to_check), f"Not all columns are present for {f}: {set(cols_to_check) - answer_student_columns}."

        
        # Reassign column names to get around capitalization issues.
        answer_df.columns = answer_df.columns.str.lower()
        answer_key_to_check: pd.DataFrame = answer_df[cols_to_check]

        student_df.columns = student_df.columns.str.lower()

        # Subset to the relevant columns
        student_to_check: pd.DataFrame = student_df[answer_key_to_check.columns]


        # Check rows match
        assert answer_key_to_check.shape == student_to_check.shape, f"Rows mismatch: answer key expects {answer_key_to_check.shape[0]} rows, but received {student_to_check.shape[0]} rows."

        # Outer Left merge to identify where student answer differs
        merged = pd.merge(left=answer_key_to_check, right=student_to_check, on=list(cols_to_check), how="outer", indicator="Exist")

        # Find where differences exist.
        if not (merged["Exist"] == "both").all(): 
            
            answer_rows = merged[merged["Exist"] == "left_only"].reset_index().drop(columns=["index", "Exist"])
            student_rows = merged[merged["Exist"] == "right_only"].reset_index().drop(columns=["index", "Exist"])

            # Added 08-27-2024: drop matching
            
            merged = merged.drop(columns="Exist")
            
            row_matches = answer_rows.isin(student_rows)
            mismatched_cols = ~row_matches.all(axis=0)

            expected_answer: pd.DataFrame = answer_rows.loc[:, mismatched_cols]
            mismatched_student: pd.DataFrame = student_rows.loc[:, mismatched_cols]

            assert mismatched_student.empty, f"Records were miscoded in {f}. Your answer:\n{mismatched_student}\n\nAnswer key:\n{expected_answer}\n\n"
        
        assert (merged["Exist"] == "both").all()
