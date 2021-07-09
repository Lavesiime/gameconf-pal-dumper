import sys
import os

# Only works with 2 arguments, you can add more but they won't really do anything
if len(sys.argv) < 3:
    print("    This tool cannot be run on its own, it needs an input file and an output file")
    print("    The first argument is the input file, the second is the output file")
    print("    For example, to extract a palette from a GameConfig.bin and send it to")
    print("    a file in the same directory called GameConfPal.act, the command would be")
    print("gameconf-pal-dumper.py GameConfig.bin GameConfPal.act")
    print("    This would generate a palette file called GameConfPal.act in the same directory as gameconf-pal-dumper.py")
    exit()

inFile = open(sys.argv[1], 'rb')
outFile = open(sys.argv[2], 'wb')

byteCount = 0

# Read how many bytes the title is and skip it
byteCount = inFile.read(1)
byteCount = int.from_bytes(byteCount, "big") # Convert it from bytes to int because read() only works with ints
inFile.read(byteCount)

# Read how many bytes the game description is and skip this, too
byteCount = inFile.read(1)
byteCount = int.from_bytes(byteCount, "big")
inFile.read(byteCount)

# RSDKv4 palette count is 0x120 bytes, so read that many
byteCount = 0x120

# Keep on going until all 0x120 bytes are read
while byteCount > 0:
    # 3 bytes at a time, I could do more or less bytes at once but because RGB is 3 bytes this feels right
    byte = inFile.read(3)
    outFile.write(byte)
    byteCount -= 3

inFile.close()
outFile.close()