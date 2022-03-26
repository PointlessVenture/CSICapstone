writefile = open("FullDataset.txt", "w")
baseFilePath = "Compliments/compliment"
baseFileSuffix = ".txt"
totalFiles = 541209

for i in range(1,totalFiles):
    if(i % 1000 == 0):
        print(i)
    file = baseFilePath + str(i) + baseFileSuffix
    readfile = open(file, "r")
    text = readfile.read()
    readfile.close()
    text = text.replace("\\n", "\n")
    text += "\n"
    writefile.write(text)
