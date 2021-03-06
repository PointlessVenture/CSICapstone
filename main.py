# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
import re
import nltk
import language_tool_python
from aitextgen import aitextgen
from aitextgen_gpt_neo_implementation_local import generation, compVision, checkGrammar
useMultiset = True

if __name__ == '__main__':
    nltk.download('omw-1.4')
    # load the retrained model + metadata necessary to generate text.
    ai = aitextgen(model_folder="GOODONEATG", to_gpu=False)

    allCompliments = []
    output = compVision()
    print("Successfully generated image and output.")

    for x in range(10):
        compList = ""
        firstComp = ""
        text = ""
        text = generation(ai, output);
        if text is not None:
            text = text.replace("Generate a compliment for " + output + ": \n", "")
            text = text.replace("\r", "")
            text = text.replace("\\", "")
            text = text.replace("\n", " ")
            text = text.replace("  ", " ")

            #Start New Text Formatter. Multi-Sentence
            if(useMultiset):
                newText = text.replace("!", ".")
                newText = newText.replace("?", ".")


                compList = newText.split(".")
                subList = []
                final = ""
                for i in compList:
                    if i != compList[-1]:
                        i += "."
                        subList.append(i)

                final = "".join(subList)
                indexlist = []
                for index in range(len(text)):
                    if text[index] == "!" or text[index] == "." or text[index] == "?":
                        indexlist.append(index)
                i = 0
                for index in range(len(final)):
                    if final[index] == ".":
                        final = final[:index] + text[indexlist[i]] + final[index + 1:]
                        i = i + 1

                firstComp = final

            else:
                compList = re.split("\.|!|\?", text)

                # Grabs punctuation
                firstComp = compList[0]
                try:
                    firstComp += text[len(compList[0])]
                    firstComp = firstComp[1:]
                except IndexError:
                    pass

            allCompliments.append(firstComp)

    #print(allCompliments)
    print("Successfully generated compliments, checking grammar...")
    bestCompliment = checkGrammar(allCompliments)
    print(bestCompliment)

