import subprocess
import tools


def main():
    # Load your LMS datasets
    df_orig = "gc_2025CMN17.10BS103a02_fullgc_2025-06-20-14-17-04.csv"
    announced_grades_path = "test_2.xls"
    lms_graded = tools.lms_grader(df_orig)

    # save the dataframes
    with open("weighted_2.csv", "w", encoding="utf-8", newline="") as f:
        lms_graded[0].to_csv(f, index=False)
    subprocess.run(
        ["vd", "-f", "csv", "-"],
        input=lms_graded[0].to_csv(index=True),
        text=True,
    )

    ann_2 = tools.lms_to_announced(announced_grades_path, df_orig, "announced_2.xls")
    # subprocess.run(["vd", "-f", "csv", "-"], input=ann_2.to_csv(index=False), text=True)

    # plot the grade distribution
    tools.hist_plotter(lms_graded[0])


if __name__ == "__main__":
    main()
