# To extract characters at specific positions from a text file, use the command line
# `dd if=input.txt bs=1 skip=187073 count=27 2>/dev/null`.

import argparse
import json
import os
import shutil
import tempfile


def replace_double_quotes_in_file(path_to_file):
    with open(path_to_file, 'r', encoding = "utf-8") as file:
        content = file.read()
    updated_content = content.replace('"', "<U+0022>")
    with open(path_to_file, 'w', encoding = "utf-8") as file:
        file.write(updated_content)


def split_text_file(path_to_file):
    with open(path_to_file, 'r', encoding="utf-8") as file:
        text = file.read()

    number_of_characters_in_chunk = 550
    number_of_chunks = len(text) // number_of_characters_in_chunk + (1 if len(text) % number_of_characters_in_chunk != 0 else 0)
    number_of_digits_in_number_of_chunks = len(str(number_of_chunks))

    temp_dir = tempfile.mkdtemp()

    for i in range(number_of_chunks):
        start = i * number_of_characters_in_chunk
        end = start + number_of_characters_in_chunk
        chunk = text[start:end]

        filename_of_chunk = os.path.join(temp_dir, f"chunk_{str(i+1).zfill(number_of_digits_in_number_of_chunks)}.txt")
        with open(filename_of_chunk, 'w', encoding="utf-8") as chunk_file:
            chunk_file.write(chunk)
    
    return temp_dir


def iterate_over_sublists(input_list, sublist_size):
    for i in range(0, len(input_list), sublist_size):
        sublist = input_list[i:i + sublist_size]
        yield sublist


def append_to_training_JSON_file(path_to_file):
    temp_dir = split_text_file(path_to_file)
    list_of_chunk_files = [os.path.join(temp_dir, file) for file in os.listdir(temp_dir) if file.startswith("chunk")]

    maximum_number_of_messages_per_line = 2048
    number_of_system_messages_per_line = 1
    number_of_messages_per_chunk = 2
    number_of_chunks_per_sublist = int(
        (maximum_number_of_messages_per_line - number_of_system_messages_per_line) / number_of_messages_per_chunk
    )
    for sublist in iterate_over_sublists(list_of_chunk_files, number_of_chunks_per_sublist):
        messages = [
            {"role": "system", "content": "You, the model, are a novelist who produces chunks of novels each with 550 characters."}
        ]
        for i, chunk_file in enumerate(sublist):
            messages.append({"role": "user", "content": "Write a chunk of a novel."})
            with open(chunk_file, 'r', encoding="utf-8") as file:
                chunk = file.read()
            messages.append({"role": "assistant", "content": chunk})
        jsonl_line = json.dumps({"messages": messages})
        path_to_training_JSONL_file = "C:/Users/Tom/Documents/Generator_Of_Excerpt_Of_Book/"
        with open(os.path.join(path_to_training_JSONL_file, "training.jsonl"), 'a', encoding="utf-8") as jsonl_file:
            jsonl_file.write(jsonl_line + '\n')

    shutil.rmtree(temp_dir)


def iterate_over_paths_to_books(path_to_directory_tree):
    for dirpath, _, filenames in os.walk(path_to_directory_tree):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            yield full_path


def add_excerpts_of_books_to_training_jsonl_file(path_to_directory_tree: str) -> None:
    for path_to_file_with_book in iterate_over_paths_to_books(path_to_directory_tree = path_to_directory_tree):
        print(f"Adding to `training.jsonl` {path_to_file_with_book}")
        replace_double_quotes_in_file(path_to_file_with_book)
        append_to_training_JSON_file(path_to_file_with_book)


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog = "Add Books To Training JSONL File",
        description = "This program adds excerpts of books to a training JSONL file for ChatGPT 4o."
    )
    parser.add_argument("path_to_directory_tree", help = "full path to a directory tree of files with books")
    args = parser.parse_args()
    path_to_directory_tree = args.path_to_directory_tree
    print(f"full path to directory tree of files with books: {path_to_directory_tree}")
    return path_to_directory_tree


if __name__ == '__main__':
    path_to_directory_tree = parse_arguments()
    add_excerpts_of_books_to_training_jsonl_file(path_to_directory_tree)