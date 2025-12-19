import sys

if len(sys.argv) != 3:
    print("Usage: python sort_csv.py input.csv output.csv")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

header = lines[0]         # первая строка (заголовок)
data_lines = lines[1:]    # остальные строки

# сортируем лексикографически
data_lines.sort()

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(header)
    f.writelines(data_lines)

print(f"Sorting complete. Output saved to {output_file}")
