import sys
import os

# Only works with 2 arguments, you can add more but they won't really do anything
if len(sys.argv) < 4:
    print("    This tool cannot be run on its own, it needs some parameters to run")
    print("    The first argument is the mode to run it in. -d is to dump, -i is to inject")
    print("    The second argument is the GameConfig file, and the third is the palette file to dump to/inject from.")
    print("    For example, if I wanted to dump a palette from a GameConfig to GamePal.act, I would do")
    print("gameconf-pal-tools.py -d GameConfig.bin GamePal.act")
    print("    This would dump the GameConfig palette to a file named GamePal.act in the same directory")
    print("")
    print("    If I wanted to inject a palette from GamePal.act to GameConfig.bin, I would do")
    print("gameconf-pal-tools.py -i GameConfig.bin GamePal.act")
    print("    This would inject the GamePal.act palette to the GameConfig.bin")
    exit()

# Mode 1 is dump, mode 2 is inject, anything else is invalid
mode = 0
if sys.argv[1] == '-d': mode = 1
if sys.argv[1] == '-i': mode = 2

if mode == 0:
    print("Invalid mode")
    print("Run this program without any arguments to see proper use")
    exit()


GameConf = open(sys.argv[2], 'r+b')

if mode == 1: PalFile = open(sys.argv[3], 'wb')
else: PalFile = open(sys.argv[3], 'rb')

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
    if mode == 2:
        byte = PalFile.read(3)
        GameConf.write(byte)
    else:
        byte = GameConf.read(3)
        PalFile.write(byte)
    
    byteCount -= 3

GameConf.close()
PalFile.close()