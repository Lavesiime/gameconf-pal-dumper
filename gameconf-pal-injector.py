import sys
import os

# Only works with 2 arguments, you can add more but they won't really do anything
if len(sys.argv) < 3:
    print("    This tool cannot be run on its own, it needs an input file and an output file")
    print("    The first argument is the input file, the second is the output file")
    print("    For example, to inject a palette from a newGamePal.act into a file")
    print("    in the same directory called GameConfig.bin, the command would be")
    print("gameconf-pal-injector.py newGamePal.act GameConfig.bin")
    print("    This would inject the palette file called newGamePal.act to the GameConfig.bin in the same directory")
    exit()

GameConf = open(sys.argv[1], 'r+b')
PalFile = open(sys.argv[2], 'rb')

byteCount = 0

# Read how many bytes the title is and skip it
byteCount = GameConf.read(1)
byteCount = int.from_bytes(byteCount, "big") # Convert it from bytes to int because read() only works with ints
GameConf.read(byteCount)

# Read how many bytes the game description is and skip this, too
byteCount = GameConf.read(1)
byteCount = int.from_bytes(byteCount, "big")
GameConf.read(byteCount)

# RSDKv4 has 0x120 bytes of palette data
byteCount = 0x120

# Keep on going until all 0x120 bytes are read
while byteCount > 0:
    # 3 bytes at a time, I could do more or less bytes at once but because RGB is 3 bytes this feels right
    byte = PalFile.read(3)
    GameConf.write(byte)
    byteCount -= 3

GameConf.close()
PalFile.close()