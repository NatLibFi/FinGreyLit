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

    model_dfs = []
    overall_avgs = []

    for fpath in sys.argv[1:]:
        model_name = fpath.split("-", maxsplit=1)[1].rsplit(".")[0].split(":")[0]
        df = pd.read_csv(
            fpath,
            sep="|",
            skiprows=[1],
        ).dropna(axis=1, how="all")
        df.columns = df.columns.str.strip()

        # Compute weighted average for this model
        weighted_avg = (df["mean"] * df["size"]).sum() / df["size"].sum()
        overall_avgs.append((model_name, weighted_avg))

        # Prepare model-specific dataframe
        df_model = df[["language", "field", "mean"]].copy()
        df_model.rename(columns={"mean": model_name}, inplace=True)
        model_dfs.append(df_model)

    # Merge all model dataframes
    joined_df = model_dfs[0]
    for df in model_dfs[1:]:
        joined_df = joined_df.merge(df, on=["language", "field"], how="outer")

    num_cols = joined_df.columns[2:]

    # Per-language averages
    lang_avgs = []
    for lang, grp in joined_df.groupby("language"):
        avg_row = grp[num_cols].mean().to_frame().T
        avg_row["language"] = lang.upper()
        avg_row["field"] = "AVERAGE"
        lang_avgs.append(avg_row)

    # Overall weighted average row
    df_avg = pd.DataFrame({name: [avg] for name, avg in overall_avgs})
    df_avg["language"] = "ALL"
    df_avg["field"] = "AVERAGE"

    # Final table
    full_df = pd.concat([joined_df, *lang_avgs, df_avg], ignore_index=True)
    full_df[num_cols] = highlight_max(full_df[num_cols])
    print(full_df.to_markdown(tablefmt="github", index=False))


if __name__ == "__main__":
    main()
