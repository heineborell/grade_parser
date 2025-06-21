import pandas as pd
import xlwt


# get the column ids from original dataframe to replace them with simpler readeable ones
def get_column_ids(orig_columns, column_name):
    id = [i for i, item in enumerate(orig_columns) if item.startswith(column_name)]
    assert len(id) == 1, "sth wrong with renaming the dataframe columns!"
    return id[0]


# actually replacing the columns names (don't remember if this is really needed but factoring the code I didn't bother to think about this in detail, whatever...)
def column_clean(original_df):
    orig_columns = list(original_df.columns)
    # rename columns for easy access
    df = original_df.rename(
        columns={
            orig_columns[get_column_ids(orig_columns, "midterm")]: "midterm",
            orig_columns[get_column_ids(orig_columns, "final")]: "final",
            orig_columns[get_column_ids(orig_columns, "hw_1")]: "HW_1",
            orig_columns[get_column_ids(orig_columns, "hw_2")]: "HW_2",
            orig_columns[get_column_ids(orig_columns, "hw_3")]: "HW_3",
            orig_columns[get_column_ids(orig_columns, "hw_4")]: "HW_4",
            orig_columns[get_column_ids(orig_columns, "Attendance")]: "attendance",
            orig_columns[get_column_ids(orig_columns, "letter_grade")]: "letter_grade",
        }
    )
    return df


# takes a list of columns and their weights then calculate weighted avg
def weighter(df, list_of_columns, list_of_weights):
    df["weighted_avg"] = 0
    for i, j in enumerate(list_of_columns):
        df["weighted_avg"] = df["weighted_avg"] + (list_of_weights[i] / 100) * df[j]


# gets the weighted avgs and bins them to letter grades
def grader(df, list_of_columns, list_of_weights, bins, labs):
    # calculate weighted_avg column
    weighter(df, list_of_columns, list_of_weights)
    # truncate grades that are higher than 100
    df["weighted_avg"] = df["weighted_avg"].clip(upper=100)
    # assign letter_grades
    df["letter_grade"] = pd.cut(
        df["weighted_avg"], bins=bins, labels=labs, include_lowest=True
    )
    # students with missing midterm or final gets F
    df.loc[df["letter_grade"].isna(), "letter_grade"] = "F"
    df.loc[df["midterm"].isna(), "midterm"] = 0
    df.loc[df["final"].isna(), "final"] = 0
    return df


# I didn't wanna use the df I created during weighted_avg so I merge the weighted_avg results to the already downloaded list from LMS (which is called original)
def merger(original, letter):
    merged = original.merge(
        letter[["Username", "letter_grade"]], on="Username", how="left", validate="1:1"
    )
    merged[original.columns[-1]] = merged["letter_grade"]
    merged.drop(["letter_grade"], axis=1, inplace=True)
    return merged


def merger_announced(original, letter, column_name, merged_column_name):
    letter = letter.rename(columns={"Username": original.columns[0]})
    letter[original.columns[0]] = letter[original.columns[0]].astype(str)
    # print({type(i) for i in letter[original.columns[0]]})
    merged = original.merge(
        letter[[original.columns[0], column_name]],
        on=original.columns[0],
        how="left",
        validate="1:1",
    )
    merged.iloc[2:, merged.columns.get_loc(merged_column_name)] = merged.iloc[
        2:, merged.columns.get_loc(column_name)
    ]
    merged.drop([column_name], axis=1, inplace=True)
    merged[merged_column_name] = merged[merged_column_name].astype(str)
    if merged_column_name == "Unnamed: 20":
        merged.loc[merged[merged_column_name] == "A", merged_column_name] = "A0"
        merged.loc[merged[merged_column_name] == "B", merged_column_name] = "B0"
        merged.loc[merged[merged_column_name] == "C", merged_column_name] = "C0"
        merged.loc[merged[merged_column_name] == "D", merged_column_name] = "D0"

    return merged


def save_as_xls(df, filename):
    wb = xlwt.Workbook()
    ws = wb.add_sheet("Sheet1")

    # Write only the first column header
    first_col_name = str(df.columns[0])
    ws.write(0, 0, first_col_name)

    # Write data starting from row 1 if first column header is written
    for row_num, row in enumerate(df.itertuples(index=False), start=1):
        for col_num, value in enumerate(row):
            if pd.isna(value):
                continue  # Leave blank
            if row_num > 3 and col_num < 15 and value == "nan":
                continue
            if row_num > 3 and col_num > 15 and value == "nan":
                value = "W"
            ws.write(row_num, col_num, value)

    wb.save(filename)
