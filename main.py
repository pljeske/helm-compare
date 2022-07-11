import argparse
import oyaml

input_file = ""
output_file = ""


def parse_args():
    global input_file, output_file

    parser = argparse.ArgumentParser()
    input_file = parser.add_argument("input", help="The (unsorted) input yaml file")
    output_file = parser.add_argument("output", help="The (sorted) output yaml file")

    args = parser.parse_args()
    input_file = args.input
    output_file = args.output


def delete_helm_lines(input_file_name: str):
    lines = []
    with open(f"./{input_file_name}", "r") as file:
        is_line_to_delete = False
        for line in file.readlines():
            if line.startswith("Release"):
                is_line_to_delete = True
            if line.startswith("---"):
                is_line_to_delete = False
            if not is_line_to_delete:
                lines.append(line)
    with open(f"./{input_file_name}", "w") as file:
        file.writelines(lines)


def sort_yaml(input_file_name: str, output_file_name: str):
    with open(f"./{input_file_name}", "r") as in_file:
        documents_gen = oyaml.unsafe_load_all(in_file)

        documents = []

        for document in documents_gen:
            documents.append(document)

        documents = sorted(documents, key=lambda k: (k['apiVersion'], k['kind'], k['metadata']['name']))

        with open(output_file_name, "w") as out_file:
            sorted_file = oyaml.dump_all(documents, out_file, sort_keys=True)
            print(sorted_file)


if __name__ == '__main__':
    parse_args()
    try:
        delete_helm_lines(input_file)
        sort_yaml(input_file, output_file)
        print("Successfully sorted yaml file. Output: " + output_file)
    except Exception as e:
        print("There was an error sorting the yaml file: " + str(e))

