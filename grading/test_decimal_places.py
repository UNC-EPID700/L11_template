import io
import os
import pandas as pd
from cryptography.fernet import Fernet

from crypt_answers import decrypt

DECIMAL_PLACES = 5
N_MISMATCHES = 5
ATOL = 5e-3

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def test_decimal_places(key, answer_path, files, cols):
    for answer, f in zip(answer_path, files): 
        
        answer_bytes = decrypt(encryptedpath=answer, key=key)
        answer_df: pd.DataFrame = pd.read_sas(io.BytesIO(answer_bytes), format="sas7bdat").round(DECIMAL_PLACES)

        # Finally, check the answers.
        # First, check that all the columns are present.
        # Alteration 2023-09-19: case insensitive input needed.
        # Alteration 2023-11-19: added columns to check
        if cols is None: 
            cols_to_check = answer_df.columns.str.lower()
        else: 
            cols_to_check = [s.strip() for s in cols.replace(
                "[", "").replace("]", "").split(",")]

        student_file = f"results/{f}.sas7bdat"
        assert os.path.exists(student_file), f"File '{student_file}' is missing from results folder. Does the file exist?"
        
        student_df = pd.read_sas(student_file, format="sas7bdat")
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

        # For Decimal Places, look at different
        df_below_delta = (answer_key_to_check - student_to_check).abs() <= ATOL

        if not df_below_delta.all(): 
            mismatched_cols = ~df_below_delta.all(axis=0)
            mismatched_rows = ~df_below_delta.all(axis=1)

            expected_answer: pd.DataFrame = answer_key_to_check.loc[mismatched_rows, mismatched_cols]
            mismatched_student: pd.DataFrame = student_to_check.loc[mismatched_rows, mismatched_cols]

            assert mismatched_student.empty, f"Records were miscoded in {f}. Your answer:\n{mismatched_student}\n\nAnswer key:\n{expected_answer}\n\n"
        

        assert df_below_delta.all()
        
    
       