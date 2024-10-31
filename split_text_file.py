import argparse
import os


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
    split_text_file(path_to_file = path_to_file)