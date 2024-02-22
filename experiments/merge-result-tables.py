import sys
import pandas as pd

# "Test" this by running python3 merge-result-tables.py tests/results-*.md


def read_md_table(file_path):
    df = pd.read_csv(
        file_path,
        sep="|",
        skiprows=[1],
    ).dropna(axis=1, how="all")
    df.columns = df.columns.str.strip()
    df.drop(columns=["size"], inplace=True)
    return df


def highlight_max(df):
    styled_rows = []
    for _, row in df.iterrows():
        is_max = list(row == row.max())
        styled_rows.append(
            [f"**{v:.4f}**" if is_max[i] else f"{v:.4f}" for i, v in enumerate(row)]
        )
    return pd.DataFrame(styled_rows)


def main():
    if len(sys.argv) <= 1:
        print("Usage: python merge-result-tables.py results-*.md > combined-results.md")
        sys.exit(1)

    dfs = []
    for fpath in sys.argv[1:]:
        column_name = fpath.split("-", maxsplit=1)[1].rsplit(".")[0].split(":")[0]
        dfs.append(read_md_table(fpath).rename(columns={"mean": column_name}))

    joined_df = dfs[0]
    for tmp_df in dfs[1:]:
        joined_df = joined_df.merge(tmp_df, on=["language", "field"], how="outer")

    num_cols = joined_df.columns[2:]

    df_grp_langs = joined_df.groupby(by="language")
    lang_avgs = []
    for lang, grp in df_grp_langs:
        df_tmp = grp[num_cols].mean().to_frame().T
        df_tmp["language"] = lang.upper()
        df_tmp["field"] = "AVERAGE"
        lang_avgs.append(df_tmp)

    df_avg = joined_df[num_cols].mean().to_frame().T

    full_df = pd.concat([joined_df, *lang_avgs, df_avg]).reset_index(drop=True)
    full_df["language"].iloc[-1] = "ALL"
    full_df["field"].iloc[-1] = "AVERAGE"

    full_df[num_cols] = highlight_max(full_df[num_cols])
    print(full_df.to_markdown(tablefmt="github", index=False))


if __name__ == "__main__":
    main()
