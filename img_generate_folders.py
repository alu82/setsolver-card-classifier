import os

folders = ["train", "test"]
numbers = [1, 2, 3]
colors = ["red", "green", "purple"]
forms = ["square", "oval", "wave"]
fillings = ["solid", "empty", "dashed"] 

base_folder = f"{os.path.dirname(__file__)}/images"
for folder in folders:
    counter = 0
    for number in numbers:
        for color in colors:
            for form in forms:
                for filling in fillings:
                    dir_name = f"{base_folder}/{folder}/{counter:02d}-{number}-{color}-{form}-{filling}"
                    try:
                        os.makedirs(dir_name)
                        print(f"{dir_name} created.")
                    except FileExistsError:
                        print(f"{dir_name} alrady exists.")
                    counter += 1
                