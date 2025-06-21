import pandas as pd
import subprocess
import seaborn as sns
import matplotlib.pyplot as plt
import xlwt
import tools

# def main():
#     print("Hello from grade-parser!")


if __name__ == "__main__":
    # main()

    weight_list = [30, 45, 5, 5, 5, 5, 5]
    column_list = ["midterm", "final", "HW_1", "HW_2", "HW_3", "HW_4", "attendance"]

    # define bins and labels
    bins = [0, 20, 26, 33, 40, 46, 53, 60, 65, 70, 75, 85, 95, 100]
    labs = [
        "A+",
        "A",
        "A-",
        "B+",
        "B",
        "B-",
        "C+",
        "C",
        "C-",
        "D+",
        "D",
        "D-",
        "F",
    ]
    labs.reverse()
    # Load your datasets
    df_2_orig = pd.read_csv("gc_2025CMN17.10BS103a02_fullgc_2025-06-20-14-17-04.csv")

    df_3_orig = pd.read_csv("gc_2025CMN17.10BS103a03_fullgc_2025-06-20-14-15-47.csv")

    # rename columns for easy access
    df_2 = df_2_orig[
        [
            "First Name",
            "Username",
            "midterm [Total Pts: 100 Score] |92376",
            "final [Total Pts: 120 Score] |92377",
            "hw_1 [Total Pts: 100 Score] |92372",
            "hw_2 [Total Pts: 100 Score] |92373",
            "hw_3 [Total Pts: 120 Score] |92374",
            "hw_4 [Total Pts: 100 Score] |92375",
            "Attendance [Total Pts: 100 Score] |91625",
            "letter_grade [Total Pts: 100 Letter] |93621",
        ]
    ]
    df_2 = df_2.rename(
        columns={
            "midterm [Total Pts: 100 Score] |92376": "midterm",
            "final [Total Pts: 120 Score] |92377": "final",
            "hw_1 [Total Pts: 100 Score] |92372": "HW_1",
            "hw_2 [Total Pts: 100 Score] |92373": "HW_2",
            "hw_3 [Total Pts: 120 Score] |92374": "HW_3",
            "hw_4 [Total Pts: 100 Score] |92375": "HW_4",
            "Attendance [Total Pts: 100 Score] |91625": "attendance",
            "letter_grade [Total Pts: 100 Letter] |93621": "letter_grade",
        }
    )

    df_3 = df_3_orig[
        [
            "First Name",
            "Username",
            "midterm [Total Pts: 100 Score] |92380",
            "final [Total Pts: 120 Score] |92381",
            "hw_1 [Total Pts: 100 Score] |92370",
            "hw_2 [Total Pts: 100 Score] |92371",
            "hw_3 [Total Pts: 120 Score] |92378",
            "hw_4 [Total Pts: 100 Score] |92379",
            "Attendance [Total Pts: 100 Score] |92017",
            "letter_grade [Total Pts: 100 Letter] |93620",
        ]
    ]
    df_3 = df_3.rename(
        columns={
            "midterm [Total Pts: 100 Score] |92380": "midterm",
            "final [Total Pts: 120 Score] |92381": "final",
            "hw_1 [Total Pts: 100 Score] |92370": "HW_1",
            "hw_2 [Total Pts: 100 Score] |92371": "HW_2",
            "hw_3 [Total Pts: 120 Score] |92378": "HW_3",
            "hw_4 [Total Pts: 100 Score] |92379": "HW_4",
            "Attendance [Total Pts: 100 Score] |92017": "attendance",
            "letter_grade [Total Pts: 100 Letter] |93620": "letter_grade",
        }
    )
    sec = 3
    if sec == 2:
        section_dataframe = df_2
        section_dataframe_orig = df_2_orig
    else:
        section_dataframe = df_3
        section_dataframe_orig = df_3_orig

    final_df = tools.grader(section_dataframe, column_list, weight_list, bins, labs)
    merged = tools.merger(section_dataframe_orig, final_df)

    # # show the dataframes
    if sec == 2:
        with open("weighted_2.csv", "w", encoding="utf-8", newline="") as f:
            final_df.to_csv(f, index=False)
        # subprocess.run(
        #     ["vd", "-f", "csv", "-"],
        #     input=final_df.to_csv(index=True),
        #     text=True,
        # )
    else:
        with open("weighted_3.csv", "w", encoding="utf-8", newline="") as f:
            final_df.to_csv(f, index=False)
        # subprocess.run(
        #     ["vd", "-f", "csv", "-"],
        #     input=final_df.to_csv(index=True),
        #     text=True,
        # )

    # # Create histogram
    plt.style.use("bmh")
    plt.rcParams.update({"font.size": 12, "figure.dpi": 100})
    sns.histplot(
        merged[section_dataframe_orig.columns[-1]],
        color="orange",
        bins=10,
        kde=True,
        edgecolor="black",
    )

    # Customize plot
    plt.title("Distribution of Letter Grades")
    plt.xlabel("Grade")
    plt.ylabel("Number of Students")
    plt.tight_layout()
    # plt.show()

    # load xls

    if sec == 2:
        announced_grades_df = pd.read_excel("test_2.xls")
        midterm_column = "Unnamed: 10"
        final_column = "Unnamed: 11"
        letter_column = "Unnamed: 20"
    else:
        announced_grades_df = pd.read_excel("test_3.xls")
        midterm_column = "Unnamed: 10"
        final_column = "Unnamed: 11"
        letter_column = "Unnamed: 20"

    # merging the final df to the announced grades, I was lazy to use a for loop or sth similar so called the same functio with different arguments three time. the approach is shit but it works
    merged_announced = tools.merger_announced(
        tools.merger_announced(
            tools.merger_announced(
                announced_grades_df, final_df, "midterm", midterm_column
            ),
            final_df,
            "final",
            final_column,
        ),
        final_df,
        "letter_grade",
        letter_column,
    )

    if sec == 2:
        tools.save_as_xls(merged_announced, "announced_2.xls")
    else:
        tools.save_as_xls(merged_announced, "announced_3.xls")
