import json
from pathlib import Path

OldDir = "JSONs/OldCode/"
ParsedDir = "JSONs/ParsedCode/"
RefinedDir = "JSONs/RefinedCode/"
CodeJSON = "codigos_aguaEnNavarra.json"


def openFile(fileDir):
    try:
        with open(fileDir + CodeJSON, "r", encoding="utf-8") as f:
            file = json.loads(f.read())
    except FileNotFoundError:
        file = None
    return file


def saveCode(jsonDir, DataFile):
    Path(jsonDir).mkdir(parents=True, exist_ok=True)
    with open(jsonDir + CodeJSON, 'w', encoding='utf-8') as outfile:
        json.dump(DataFile, outfile)


def refineCode(newFile, oldFile):
    refinedFile = []

    for item in newFile:
        newCode = []
        if item["codigo"] not in [x["codigo"] for x in oldFile]:
            newCode.append(item)

    saveCode(RefinedDir, refinedFile)


def main():
    newFile = openFile(ParsedDir)
    oldFile = openFile(OldDir)

    if oldFile is None:
        saveCode(RefinedDir, newFile)
        saveCode(OldDir, newFile)
        return

    refineCode(newFile, oldFile)
    saveCode(OldDir, newFile)


if __name__ == "__main__":
    main()
