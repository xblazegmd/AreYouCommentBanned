result = ""
titleCount = 0
with open("changelog.md", "r") as f:
    for line in f:
        if line.startswith("#"):
            titleCount += 1
            if titleCount > 1:
                break

        result += line

print(result.strip())