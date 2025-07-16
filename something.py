from sortium import Sorter
import sys

folder_path = sys.argv[1]
# dest_path = sys.argv[2]

print(folder_path)
# print(dest_path)

# file_utils = FileUtils()
# file_utils.flatten_dir(folder_path, dest_path)

sorter = Sorter()
sorter.sort_by_type(folder_path)
