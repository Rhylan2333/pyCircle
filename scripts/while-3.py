while iter_count < max_iter:
    if 2 * np.pi <= df_genomic_labels_core.shape[0] * min_delta_rad_end:
        print("min_delta_rad_end is too large.")
        break
    if (
        min_delta_rad_end
        <= df_adjusted_genomic_labels_core["delta_adjusted_rad_end"].iloc[1:]
    ).all():
        print(f"Stop, iter_count = {iter_count}")
        break
    # 0 <= "delta_adjusted_rad_end" < min_delta_rad_end
    selected_rows = df_adjusted_genomic_labels_core[
        (0 <= df_adjusted_genomic_labels_core["delta_adjusted_rad_end"])
        & (
            df_adjusted_genomic_labels_core["delta_adjusted_rad_end"]
            < min_delta_rad_end
        )
    ]["delta_adjusted_rad_end"]
    if not selected_rows.empty:
        consecutive_groups = find_consecutive_groups(selected_rows)
        print(consecutive_groups, "\n")
        for indexes in consecutive_groups:
            selected_group = df_adjusted_genomic_labels_core.loc[
                indexes, "adjusted_rad_end"
            ]
            if selected_group.count() % 2 == 0:
                # 为什么引入了这个后就不行了呢？
                range_offset = min_delta_rad_end * (selected_group.count() // 2 - 0.5)
            else:
                range_offset = min_delta_rad_end * (selected_group.count() // 2)
            df_adjusted_genomic_labels_core.loc[indexes, "adjusted_rad_end"] = (
                np.linspace(
                    selected_group.mean() - range_offset,
                    selected_group.mean() + range_offset,
                    selected_group.count(),
                )
            )
            # sort_adjusted_rad_end(df_adjusted_genomic_labels_core)
            re_cal_delta_adjusted_rad_end(df_adjusted_genomic_labels_core)
    for i, row in df_adjusted_genomic_labels_core.iterrows():
        if i == 0:
            continue
        delta_0 = row["delta_adjusted_rad_end"]
        if delta_0 < 0:
            while (df_adjusted_genomic_labels_core["delta_adjusted_rad_end"] < 0).any():
                delta_bs = pd.Series(
                    df_adjusted_genomic_labels_core.loc[i, "adjusted_rad_end"]
                    - df_adjusted_genomic_labels_core.loc[
                        : i - 1, "adjusted_rad_end"
                    ],
                )
                print(delta_bs)
                first_negative_index = delta_bs[delta_bs < 0].index[0]
                selected_group = df_adjusted_genomic_labels_core.loc[
                    first_negative_index:i, "adjusted_rad_end"
                ]
                new_values = [
                    df_adjusted_genomic_labels_core.loc[i, "adjusted_rad_end"],
                    *df_adjusted_genomic_labels_core.loc[
                        first_negative_index : i - 1, "adjusted_rad_end"
                    ].tolist(),
                ]
                df_adjusted_genomic_labels_core.loc[
                    selected_group.index, "adjusted_rad_end"
                ] = new_values
                sort_adjusted_rad_end(df_adjusted_genomic_labels_core)
                re_cal_delta_adjusted_rad_end(df_adjusted_genomic_labels_core)
        # 这一步非常关键！！！！！！
        sort_rad_start(df_adjusted_genomic_labels_core)