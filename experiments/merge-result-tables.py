import sys
import pandas as pd


def read_md_table(file_path):
    df = pd.read_csv(
        file_path,
        sep='|',
        skiprows=[1],
    ).dropna(
        axis=1,
        how='all'
    )
    df.columns = df.columns.str.strip()
    df.drop(columns=["size"], inplace=True)
    return df


# def highlight_max(s):
#     print(s)
#     is_max = s == s.max()
#     return ["*" + str(v) + "*" if is_max else v for v in s]


def main():
    if len(sys.argv) <= 1:
        print("Usage: python merge-result-tables.py results-*.md > combined-results.md")
        sys.exit(1)

    dfs = []
    for fpath in sys.argv[1:]:
        column_name = fpath.split("-", maxsplit=1)[1].rsplit(".")[0].split(":")[0]
        dfs.append(
            read_md_table(fpath).rename(
                columns={"mean": column_name}
            )
        )

    joined_df = dfs[0]
    for tmp_df in dfs[1:]:
        joined_df = joined_df.merge(tmp_df,
                                    on=["language", "field"],
                                    how='outer'
                                    )

    # styled_table = joined_df.apply(highlight_max, subset=joined_df.columns[1:])
    print(joined_df.to_markdown(tablefmt="github", index=False))


if __name__ == "__main__":
    main()
