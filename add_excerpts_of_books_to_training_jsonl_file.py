import argparse
import json
import os


def replace_double_quotes_in_file(path_to_file):
    with open(path_to_file, 'r', encoding="utf-8") as file:
        content = file.read()
    updated_content = content.replace('"', "<U+0022>")
    with open(path_to_file, 'w', encoding="utf-8") as file:
        file.write(updated_content)


def iterate_over_groups_of_characters(text, group_size):
    for i in range(0, len(text), group_size):
        yield text[i:i + group_size]


def length_of_contents_of_messages_in(list_of_messages: list[dict["str": "str"]]) -> int:
    length_of_contents_of_messages = 0
    for message in list_of_messages:
        content = message["content"]
        length_of_content = len(content)
        length_of_contents_of_messages += length_of_content
    return length_of_contents_of_messages

def append_to_training_JSONL_file(path_to_file):
    
    path_to_training_JSONL_file = "C:/Users/Tom/Documents/Generator_Of_Excerpt_Of_Book/training.jsonl"

    system_message = {
        "role": "system",
        "content": "You, the model, are a novelist who produces chunks of novels each with 550 characters."
    }
    list_of_messages = [system_message]

    number_of_characters_per_excerpt = 550

    with open(path_to_file, 'r', encoding = "utf-8") as file:
        text = file.read()

    list_of_excerpts = [excerpt for excerpt in iterate_over_groups_of_characters(text, number_of_characters_per_excerpt)]

    index_of_excerpt = 0
    while index_of_excerpt < len(list_of_excerpts):
        
        excerpt = list_of_excerpts[index_of_excerpt]

        number_of_characters_in_excerpt = len(excerpt)

        if (len(list_of_messages) + 2 <= 2048) and (length_of_contents_of_messages_in(list_of_messages) + number_of_characters_in_excerpt <= 128_000):
            user_message = {"role": "user", "content": "Write a chunk of a novel."}
            assistant_message = {"role": "assistant", "content": excerpt}
            list_of_messages.append(user_message)
            list_of_messages.append(assistant_message)
            index_of_excerpt += 1
        
        else:
            with open(path_to_training_JSONL_file, 'a', encoding="utf-8") as jsonl_file:
                jsonl_file.write(json.dumps({"messages": list_of_messages}) + '\n')
            list_of_messages = [system_message]

    with open(path_to_training_JSONL_file, 'a', encoding = "utf-8") as jsonl_file:
        jsonl_file.write(json.dumps({"messages": list_of_messages}) + '\n')


def iterate_over_paths_to_books(path_to_directory_tree):
    for dirpath, _, filenames in os.walk(path_to_directory_tree):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            yield full_path


def add_excerpts_of_books_to_training_jsonl_file(path_to_directory_tree: str) -> None:
    for path_to_file_with_book in iterate_over_paths_to_books(path_to_directory_tree=path_to_directory_tree):
        print(f"Adding to `training.jsonl` {path_to_file_with_book}")
        replace_double_quotes_in_file(path_to_file_with_book)
        append_to_training_JSONL_file(path_to_file_with_book)


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="Add Books To Training JSONL File",
        description="This program adds excerpts of books to a training JSONL file for ChatGPT 4o."
    )
    parser.add_argument("path_to_directory_tree", help="full path to a directory tree of files with books")
    args = parser.parse_args()
    path_to_directory_tree = args.path_to_directory_tree
    print(f"full path to directory tree of files with books: {path_to_directory_tree}")
    return path_to_directory_tree


if __name__ == '__main__':
    path_to_directory_tree = parse_arguments()
    add_excerpts_of_books_to_training_jsonl_file(path_to_directory_tree)