import os


nextLineIsATimestamp = False
newBlock = False
block = []
formattedLine = None
ts = None
index = 0

if os.path.exists("new_destination.csv"):
  os.remove("new_destination.csv")
else:
  print("The file does not exist")

writer = open("new_destination.csv", "a")

with open('source.log', 'r') as reader:

  for line in reader:
    index +=1

    formattedLine = line.replace(" ", ',').split(",")
    formattedLine = filter(None, formattedLine)

    if '----' in line:
      newBlock = True
      nextLineIsATimestamp = True
            
    if newBlock is True:
      newBlock = False
    elif nextLineIsATimestamp:
      # this is a new block, this is a timestamp
      ts = formattedLine[0]
      # reset the state
      nextLineIsATimestamp = False
    else:
      formattedLine[-1] = formattedLine[-1].replace('\n', '')
      block.extend(formattedLine)
      block.append(ts)
      writer.write(",".join(block));
    
    formattedLine = None
    block = []


writer.close()
