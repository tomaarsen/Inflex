import glob

with open("compare\\words\\nouns.txt") as words_file:
    words = words_file.read().split("\n")
    for perl_file_path in glob.glob("compare\\perl_output\\*\\*\\*.txt"):
        python_file_path = perl_file_path.replace("perl_output", "python_output")
        with open(perl_file_path, "r") as perl_file:
            with open(python_file_path, "r") as python_file:
                perl_data = perl_file.read().split("\n")
                python_data = python_file.read().split("\n")
                if perl_data != python_data:
                    c = 0
                    print(f"[ ]: {perl_file_path!r}")
                    for i, (pe, py) in enumerate(zip(perl_data, python_data)):
                        if pe != py:
                            # print(i, pe, py)
                            # print(words[i], pe, py)
                            c += 1
                            # breakpoint()
                            # print(pe, py)
                    print(c)
                else:
                    print(f"[+]: {perl_file_path!r}")
