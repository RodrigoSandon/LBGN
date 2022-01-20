import os, glob
import pandas as pd
import matplotlib.pyplot as plt


def stacked_barplot(list_1, list_2, title, labels, dst):

    # Now have labels list (based on my input)

    width = 0.35
    fig, ax = plt.subplots()
    ax.bar(labels, list_1, width, label="Responsive")
    ax.bar(labels, list_2, width, bottom=list_1, label="Non-Responsive")

    ax.set_ylabel("# Cells")
    ax.set_title(title)
    ax.legend()

    plt.savefig(dst)


def main():
    csv_path = r"/home/rory/Rodrigo/Database/StackedBars/how_shock_respcells_changein_blocks_and_rewsize/RDT_D2/Shock_True/rdt2_shock_true_rew_block.csv"
    session = csv_path.split("/")[7]
    dst = csv_path.replace(".csv", ".png")

    df = pd.read_csv(csv_path)

    resp_count = []
    nonresp_count = []
    labels = ["Shock Responsiveness", "Large Reward, Block 2", "Large Reward, Block 3"]

    total_cell_count = 106
    shock_resp_cells_count = len(df)

    for count, col in enumerate(list(df.columns)):
        if count == 1:
            df_sub = df.loc[df[col] != "Neutral"]
            resp_count.append(len(df_sub))
            nonresp_count.append(total_cell_count - len(df_sub))
            prev_resp_count = len(df_sub)
        elif count > 1:
            df_sub = df.loc[df[col] != "Neutral"]
            resp_count.append(len(df_sub))
            nonresp_count.append(shock_resp_cells_count - len(df_sub))

    print(resp_count)
    print(nonresp_count)

    title = (
        f"{session}: Effect of Shock Probability on Shock-Large Reward Responsive Cells"
    )
    stacked_barplot(resp_count, nonresp_count, title, labels, dst)


if __name__ == "__main__":
    main()
