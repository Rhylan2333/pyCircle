arrow_params = dict(
    alpha=0.5,
    arrowstyle="wedge,tail_width=0.2,shrink_factor=0.4",
    color="#737c7b",
    linewidth=0.0,
)

for index, row in df_adjusted_genomic_labels_core.iterrows():
    kwargs = dict(
        annotation_clip=False,
        rotation=adjust_rotation(
            np.degrees(np.pi / 2 - row["adjusted_rad_end"]),
            vertical=True,
        ),
        color=row["color"],
        fontsize=8.0,
        va="center_baseline",
        rotation_mode="anchor",  # default, anchor,
    )
    annotation_params = dict(
        text=row["annotation"],
        xy=(row["rad_start"], y_genomic_labels_core),
        xytext=(row["adjusted_rad_end"], ytext_genomic_labels_core),
        arrowprops=arrow_params,
        **kwargs,
    )
    # connectionstyle_1 = f"angle3,angleA={-(90-np.degrees(row['adjusted_rad_end']))},angleB={90-np.degrees(row['rad_start'])}"
    connectionstyle_1 = f"angle3,angleA={90-np.degrees(row['adjusted_rad_end'])},angleB={(180-np.degrees(row['rad_start']))}"
    # connectionstyle_2 = f"angle3,angleA={-(90-np.degrees(row['adjusted_rad_end']))},angleB={90-np.degrees(row['rad_start'])}"
    connectionstyle_2 = f"angle3,angleA={90-np.degrees(row['adjusted_rad_end'])},angleB={(-np.degrees(row['rad_start']))}"
    if 0 <= row["rad_start"] < np.pi:
        annotation_params["ha"] = "left"
        if 0 <= row["rad_end"] < np.pi / 2:
            annotation_params["arrowprops"]["connectionstyle"] = connectionstyle_1
        else:
            annotation_params["arrowprops"]["connectionstyle"] = connectionstyle_2
    else:
        annotation_params["ha"] = "right"
        if np.pi / 2 <= row["rad_end"] < 3 * np.pi / 2:
            annotation_params["arrowprops"]["connectionstyle"] = connectionstyle_2
        else:
            annotation_params["arrowprops"]["connectionstyle"] = connectionstyle_1

    genomic_labels_core.append(ax_genomic_labels.annotate(**annotation_params))
