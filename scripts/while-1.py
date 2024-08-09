while iter_count < max_iter:
    if 2 * np.pi <= df_genomic_labels_core.shape[0] * min_delta_rad_end:
        print("min_delta_rad_end is too large.")
        break
    for index, row in df_adjusted_genomic_labels_core[
        df_adjusted_genomic_labels_core["chr"] == "Hass_Chr_5"
    ].iterrows():
        # 记得把限定条件删掉
        if index == 0:
            continue
        delta_0 = row["delta_adjusted_rad_end"]
        if delta_0 < 0:
            # 检查往前多个是否有交叉的情况
            # 取最靠近起点的label交换rad
            while (df_adjusted_genomic_labels_core["delta_adjusted_rad_end"] < 0).any():
                delta_bs = pd.Series(
                    df_adjusted_genomic_labels_core.loc[index, "adjusted_rad_end"]
                    - df_adjusted_genomic_labels_core.loc[
                        : index - 1, "adjusted_rad_end"
                    ],
                )
                first_negative_index = delta_bs[delta_bs < 0].index[0]
                print(delta_bs, index, first_negative_index)
                selected_group = df_adjusted_genomic_labels_core.loc[
                    first_negative_index:index, "adjusted_rad_end"
                ]
                new_values = [
                    df_adjusted_genomic_labels_core.loc[index, "adjusted_rad_end"],
                    *df_adjusted_genomic_labels_core.loc[
                        first_negative_index : index - 1, "adjusted_rad_end"
                    ].tolist(),
                ]
                df_adjusted_genomic_labels_core.loc[
                    selected_group.index, "adjusted_rad_end"
                ] = new_values
                df_adjusted_genomic_labels_core.sort_values(
                    by=["adjusted_rad_end", "annotation"],
                    ignore_index=True,
                    inplace=True,
                )
                re_cal_delta_adjusted_rad_end(df_adjusted_genomic_labels_core)

                print(
                    df_adjusted_genomic_labels_core[
                        df_adjusted_genomic_labels_core["chr"] == "Hass_Chr_5"
                    ].loc[:, ["adjusted_rad_end", "delta_adjusted_rad_end"]],
                    "\n\n",
                )

            # re_cal_delta_adjusted_rad_end(df_adjusted_genomic_labels_core)
        elif 0 <= delta_0 < min_delta_rad_end:
            if index == 1:
                assign_new_group_type_1(df_adjusted_genomic_labels_core, index)
            else:
                delta_b1 = df_adjusted_genomic_labels_core.loc[
                    index - 1, "delta_adjusted_rad_end"
                ]
                if 0 <= delta_b1 < min_delta_rad_end:
                    df_adjusted_genomic_labels_core.loc[index, "group_type"] = (
                        df_adjusted_genomic_labels_core.loc[index - 1, "group_type"]
                    )
                elif min_delta_rad_end <= delta_b1:
                    assign_new_group_type_1(df_adjusted_genomic_labels_core, index)
        elif min_delta_rad_end <= delta_0:
            df_adjusted_genomic_labels_core.loc[index, "group_type"] = 0

    if (df_adjusted_genomic_labels_core["group_type"] == 0).all():
        print(f"Stop, iter_count = {iter_count}")
        break

    for group_type in df_adjusted_genomic_labels_core["group_type"].unique()[1:]:
        selected_group = df_adjusted_genomic_labels_core.loc[
            df_adjusted_genomic_labels_core["group_type"] == group_type,
            "adjusted_rad_end",
        ]
        range_offset = min_delta_rad_end * (selected_group.count() // 2)
        new_values = np.linspace(
            selected_group.mean() - range_offset,
            selected_group.mean() + range_offset,
            selected_group.count(),
        )
        df_adjusted_genomic_labels_core.loc[
            selected_group.index, "adjusted_rad_end"
        ] = new_values
    # df_adjusted_genomic_labels_core.sort_values(
    #     by=["adjusted_rad_end", "annotation"],
    #     # by=["rad_start", "adjusted_rad_end"],
    #     # by=["rad_start", "adjusted_rad_end"],
    #     ignore_index=True,
    #     inplace=True,
    # )
    re_cal_delta_adjusted_rad_end(df_adjusted_genomic_labels_core)
    df_adjusted_genomic_labels_core["group_type"] = 0
    iter_count += 1
