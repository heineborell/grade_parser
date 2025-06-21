import pandas as pd
import subprocess
import seaborn as sns
import matplotlib.pyplot as plt
import tools


def main():
    # Load your LMS datasets
    df_2_orig = "gc_2025CMN17.10BS103a02_fullgc_2025-06-20-14-17-04.csv"
    announced_grades_path = "test_2.xls"

    # # show the dataframes
    with open("weighted_2.csv", "w", encoding="utf-8", newline="") as f:
        tools.lms_grader(df_2_orig)[0].to_csv(f, index=False)
    # subprocess.run(
    #     ["vd", "-f", "csv", "-"],
    #     input=tools.lms_grader(df_2_orig)[1].to_csv(index=True),
    #     text=True,
    # )

    ann = tools.lms_to_announced(announced_grades_path, df_2_orig, "announced_2.xls")
    subprocess.run(["vd", "-f", "csv", "-"], input=ann.to_csv(index=False), text=True)

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


if __name__ == "__main__":
    main()
