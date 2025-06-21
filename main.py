import pandas as pd
import subprocess
import seaborn as sns
import matplotlib.pyplot as plt
import tools

# def main():
#     print("Hello from grade-parser!")


if __name__ == "__main__":
    # main()

    # Load your LMS datasets
    df_2_orig = pd.read_csv("gc_2025CMN17.10BS103a02_fullgc_2025-06-20-14-17-04.csv")

    df_3_orig = pd.read_csv("gc_2025CMN17.10BS103a03_fullgc_2025-06-20-14-15-47.csv")

    sec = 3
    if sec == 2:
        final_df = tools.lms_grader(df_2_orig)[0]
        merged = tools.lms_grader(df_2_orig)[1]
    else:
        final_df = tools.lms_grader(df_3_orig)[0]
        merged = tools.lms_grader(df_3_orig)[1]

    # # show the dataframes
    if sec == 2:
        with open("weighted_2.csv", "w", encoding="utf-8", newline="") as f:
            final_df.to_csv(f, index=False)
        subprocess.run(
            ["vd", "-f", "csv", "-"],
            input=final_df.to_csv(index=True),
            text=True,
        )
    else:
        with open("weighted_3.csv", "w", encoding="utf-8", newline="") as f:
            final_df.to_csv(f, index=False)
        subprocess.run(
            ["vd", "-f", "csv", "-"],
            input=merged.to_csv(index=True),
            text=True,
        )

    #
    # # # Create histogram
    # plt.style.use("bmh")
    # plt.rcParams.update({"font.size": 12, "figure.dpi": 100})
    # sns.histplot(
    #     merged[section_dataframe_orig.columns[-1]],
    #     color="orange",
    #     bins=10,
    #     kde=True,
    #     edgecolor="black",
    # )
    #
    # # Customize plot
    # plt.title("Distribution of Letter Grades")
    # plt.xlabel("Grade")
    # plt.ylabel("Number of Students")
    # plt.tight_layout()
    # # plt.show()
    #
    # # load xls
    #
    # if sec == 2:
    #     announced_grades_df = pd.read_excel("test_2.xls")
    #     midterm_column = "Unnamed: 10"
    #     final_column = "Unnamed: 11"
    #     letter_column = "Unnamed: 20"
    # else:
    #     announced_grades_df = pd.read_excel("test_3.xls")
    #     midterm_column = "Unnamed: 10"
    #     final_column = "Unnamed: 11"
    #     letter_column = "Unnamed: 20"
    #
    # # merging the final df to the announced grades, I was lazy to use a for loop or sth similar so called the same functio with different arguments three time. the approach is shit but it works
    # merged_announced = tools.merger_announced(
    #     tools.merger_announced(
    #         tools.merger_announced(
    #             announced_grades_df, final_df, "midterm", midterm_column
    #         ),
    #         final_df,
    #         "final",
    #         final_column,
    #     ),
    #     final_df,
    #     "letter_grade",
    #     letter_column,
    # )
    #
    # if sec == 2:
    #     tools.save_as_xls(merged_announced, "announced_2.xls")
    # else:
    #     tools.save_as_xls(merged_announced, "announced_3.xls")
