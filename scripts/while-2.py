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
    for index, row in df_adjusted_genomic_labels_core.iterrows():
        if index == 0:
            continue
        delta_0 = row["delta_adjusted_rad_end"]
        if delta_0 < 0:
            while (df_adjusted_genomic_labels_core["delta_adjusted_rad_end"] < 0).any():
                delta_bs = pd.Series(
                    df_adjusted_genomic_labels_core.loc[index, "adjusted_rad_end"]
                    - df_adjusted_genomic_labels_core.loc[
                        : index - 1, "adjusted_rad_end"
                    ],
                )
                first_negative_index = delta_bs[delta_bs < 0].index[0]
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
                sort_adjusted_rad_end(df_adjusted_genomic_labels_core)
                re_cal_delta_adjusted_rad_end(df_adjusted_genomic_labels_core)
        elif 0 <= delta_0 < min_delta_rad_end:
            left = df_adjusted_genomic_labels_core.loc[index - 1, "adjusted_rad_end"]
            right = (
                df_adjusted_genomic_labels_core.loc[index, "adjusted_rad_end"]
                + min_delta_rad_end
            )
            selected_group = df_adjusted_genomic_labels_core[
                (left <= df_adjusted_genomic_labels_core["adjusted_rad_end"])
                & (df_adjusted_genomic_labels_core["adjusted_rad_end"] < right)
            ]["adjusted_rad_end"]
            print(selected_group)
            range_offset = (
                modify_times * min_delta_rad_end * (selected_group.count() // 2)
            )
            new_values = np.linspace(
                selected_group.mean() - range_offset,
                selected_group.mean() + range_offset,
                selected_group.count(),
            )
            df_adjusted_genomic_labels_core.loc[
                selected_group.index, "adjusted_rad_end"
            ] = new_values
            print(
                df_adjusted_genomic_labels_core.loc[
                    selected_group.index, "adjusted_rad_end"
                ],
                "\n",
            )
            sort_adjusted_rad_end(df_adjusted_genomic_labels_core)
            re_cal_delta_adjusted_rad_end(df_adjusted_genomic_labels_core)
        # 这一步非常关键！！！！！！
        sort_rad_start(df_adjusted_genomic_labels_core)
    iter_count += 1
