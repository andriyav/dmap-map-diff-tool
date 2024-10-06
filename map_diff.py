import json
import sys
from deepdiff import DeepDiff
from colorama import Fore, init
from pathlib import Path
from db_access import db_access_stage, db_access_prod
from query import query_content_type, query_map

init()
mls_num = sys.argv[1]


# mls_num = 562
def filter_priority_keys(diff):
    filtered_diff = {}
    for key, value in diff.items():
        if key in ['dictionary_item_removed', 'values_changed', 'dictionary_item_added']:
            filtered_diff[key] = {}
            for sub_key, sub_value in value.items():
                if 'priority' not in sub_key:
                    filtered_diff[key][sub_key] = sub_value
        else:
            filtered_diff[key] = value

    return filtered_diff


folder_path = Path("./")
json_files = folder_path.glob("*.json")
for file_path in json_files:
    file_path.unlink()

con = db_access_stage()
cur = con.cursor()
cur.execute(query_content_type(mls_num))
content_types = cur.fetchall()
print(content_types)
cur.close()
con.close()

for content_type in content_types:
    content_type_ele = content_type[0]
    con = db_access_stage()
    cur = con.cursor()
    cur.execute(query_map(mls_num, content_type_ele))
    result_stage = cur.fetchone()
    json_stage = result_stage[0]
    cur.close()
    con.close()

    con = db_access_prod()
    cur = con.cursor()
    cur.execute(query_map(mls_num, content_type_ele))
    result_prod = cur.fetchone()

    try:
        json_prod = result_prod[0]
        diff = DeepDiff(json_prod, json_stage, verbose_level=2, ignore_type_in_groups=['type_changes'])
        if 'type_changes' in diff:
            del diff['type_changes']
        filtered_diff = filter_priority_keys(diff)
        if filtered_diff and not all(not v for v in filtered_diff.values()):
            print(
                Fore.RED + "The mismatch between stage and prod detected in the class " + Fore.LIGHTYELLOW_EX + f"{content_type_ele}. "
                + Fore.RED + f"Please check file " + Fore.LIGHTYELLOW_EX + f"{content_type_ele}.json" + Fore.RED + f" for reference")
            with open(f'{content_type_ele}.json', 'w') as json_file:
                json.dump(filtered_diff, json_file, indent=4)
            with open(f'{content_type_ele}_stage.json', 'w') as json_file:
                json.dump(json_prod, json_file, indent=4)
            with open(f'{content_type_ele}_prod.json', 'w') as json_file:
                json.dump(json_stage, json_file, indent=4)
        else:
            print(Fore.LIGHTGREEN_EX + f" {content_type_ele} - OK")


    except:
        print(
            Fore.RED + f"The source content type in stage and prod are different. {content_type_ele} is missing in prod "
                       f" Looks like the sources is going to be migrated from RETS to API")
        break

    cur.close()
    con.close()
