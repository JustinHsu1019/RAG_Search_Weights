from datasets import get_dataset_config_names, load_dataset

dataset_name = "MediaTek-Research/TCEval-v2"

subsets = get_dataset_config_names(dataset_name)

subset_row_count = {}

for subset in subsets:
    ds = load_dataset(dataset_name, subset)
    row_count = ds['test'].num_rows
    subset_row_count[subset] = row_count

for subset, row_count in subset_row_count.items():
    print(f"Subset: {subset}, Row Count: {row_count}")
