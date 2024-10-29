# To extract characters at specific positions from a text file, use the command line
# `dd if=input.txt bs=1 skip=187073 count=27 2>/dev/null`.

import argparse
import json
import os


def replace_double_quotes_in_file(path_to_file):
    with open(path_to_file, 'r', encoding = "utf-8") as file:
        content = file.read()
    updated_content = content.replace('"', "<U+0022>")
    with open(path_to_file, 'w', encoding = "utf-8") as file:
        file.write(updated_content)


def split_text_file(path_to_file):
    with open(path_to_file, 'r', encoding = "utf-8") as file:
        text = file.read()

    number_of_characters_in_chunk = 550
    number_of_chunks = len(text) // number_of_characters_in_chunk + (1 if len(text) % number_of_characters_in_chunk != 0 else 0)
    number_of_digits_in_number_of_chunks = len(str(number_of_chunks))

    path_to_directory = os.path.dirname(path_to_file)

    for i in range(number_of_chunks):
        start = i * number_of_characters_in_chunk
        end = start + number_of_characters_in_chunk
        chunk = text[start:end]

        filename_of_chunk = os.path.join(path_to_directory, f"chunk_{str(i+1).zfill(number_of_digits_in_number_of_chunks)}.txt")
        with open(filename_of_chunk, 'w', encoding = "utf-8") as chunk_file:
            chunk_file.write(chunk)


def append_to_training_JSON_file(path_to_file):
    path_to_directory = os.path.dirname(path_to_file)
    list_of_chunk_files = [os.path.join(path_to_directory, file) for file in os.listdir(path_to_directory) if file.startswith("chunk")]

    messages = [
        {"role": "system", "content": "You, the model, are a novelist who produces chunks of novels each with 550 characters."}
    ]
    for i, chunk_file in enumerate(list_of_chunk_files):
        messages.append({"role": "user", "content": "Write a chunk of a novel."})
        with open(chunk_file, 'r', encoding="utf-8") as file:
            chunk = file.read()
        messages.append({"role": "assistant", "content": chunk})

    jsonl_line = json.dumps({"messages": messages})

    path_to_training_JSONL_file = "C:/Users/Tom/Documents/Books/"
    with open(os.path.join(path_to_training_JSONL_file, "training.jsonl"), 'a', encoding="utf-8") as jsonl_file:
        jsonl_file.write(jsonl_line + '\n')

    for chunk_file in list_of_chunk_files:
        os.remove(chunk_file)


def add_book_to_training_jsonl_file(path_to_file: str) -> None:
    replace_double_quotes_in_file(path_to_file)
    split_text_file(path_to_file)
    append_to_training_JSON_file(path_to_file)


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog = "Add Book To Training JSONL File",
        description = "This program adds a book to a training JSONL file for ChatGPT 4o."
    )
    parser.add_argument("path_to_file", help = "full path to the file with the book")
    args = parser.parse_args()
    path_to_file = args.path_to_file
    print(f"Full path to the file with the book: {path_to_file}")
    return path_to_file


if __name__ == '__main__':
    path_to_file = parse_arguments()
    add_book_to_training_jsonl_file(path_to_file)