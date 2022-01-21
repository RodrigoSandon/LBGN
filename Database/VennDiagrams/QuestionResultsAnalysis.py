import os, glob
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn2_circles, venn2_unweighted
from matplotlib_venn import venn3, venn3_circles
from matplotlib_venn import venn3_circles


def stacked_barplot(list_1, list_2, list_3, title, labels, dst):

    # Now have labels list (based on my input)

    width = 0.35
    fig, ax = plt.subplots()

    zipped = zip(list_1, list_2)

    sum = [x + y for (x, y) in zipped]

    ax.bar(labels, list_1, width, label="Large Responsive")
    ax.bar(labels, list_2, width, bottom=list_1, label="Both")
    ax.bar(labels, list_3, width, bottom=sum, label="Small Responsive")

    ax.set_ylabel("# Cells")
    ax.set_title(title)
    ax.legend()

    plt.savefig(dst)


def main():
    # all bars will have the same num cells (within the pool of cells that were resp to X)
    csv_path = r"/home/rory/Rodrigo/Database/StackedBars/how_shock_respcells_changein_blocks_and_rewsize/take2_rdt2_shockNonresponsive.csv"
    session = "RDT_D2"
    dst = csv_path.replace(".csv", ".png")

    df = pd.read_csv(csv_path)

    resp_L_counts = []
    resp_both_counts = []
    resp_S_counts = []

    labels = ["Block 1", "Block 2", "Block 3"]

    # Basically, have a dict for each block on the count of cells for each
    # will need to track idx of each cell so to give it an overall identity
    # d = {"resp_L": 0, "resp_S": 0, "resp_both": 0}

    for idx_col, col in enumerate(list(df.columns)):
        if "Large" in col:
            resp_L = 0
            resp_S = 0
            resp_both = 0
            print(col)
            # idx can be cell, all the same cell across columns
            # only perform this if modulus of 2 is 0 (meaning perform this after
            # every two cols starting after the first two cols)
            for idx_row, cell_id in enumerate(df[col]):
                # print(df.loc[idx][col])
                large_cell_id = cell_id
                small_cell_id = df.iloc[idx_row, idx_col + 1]

                if (
                    large_cell_id != "Neutral" and small_cell_id != "Neutral"
                ):  # cell responsive to both
                    resp_both += 1
                elif (
                    large_cell_id != "Neutral" and small_cell_id == "Neutral"
                ):  # resp to L
                    resp_L += 1
                elif large_cell_id == "Neutral" and small_cell_id != "Neutral":
                    resp_S += 1

            resp_L_counts.append(resp_L)
            resp_both_counts.append(resp_both)
            resp_S_counts.append(resp_S)

    print(resp_L_counts)
    print(resp_both_counts)
    print(resp_S_counts)

    title = f"{session}: Effect of Shock Probability on Reward Responsive Cells"
    stacked_barplot(resp_L_counts, resp_both_counts, resp_S_counts, title, labels, dst)


if __name__ == "__main__":
    main()
