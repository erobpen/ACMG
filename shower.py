

import os
directory = 'rezultati_3.5_h-off'

# Loop through all files in the directory
for filename in os.listdir(directory):
    print(filename + " " + "=" * 20)
    print("\n\n")
    n = input("Show >> ")
    
    with open(os.path.join(directory, filename), 'r') as file:
        text = file.read()
        text = text.split("\n")
        text = "\n".join(["     " + x for x in text])
        text = "\n\n".join(text.split("attempt"))
        text = text.split("___________")
        text_1 = text[0]
        text.remove(text_1)
        text_2 = "".join(text)
        print(text_1)
        t = input("Display minizinc >> ")
        print(text_2)
        print("\n\n" * 10)
        
        # with open("zz_shower.txt", 'w') as file:
        #     file.write(text_1)