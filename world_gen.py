#!/usr/bin/python

from collections import deque
import random
import string
import pdb

class WorldPoint:
  def __init__(self, newRow, newCol):
    self.row = newRow
    self.col = newCol

class BernoulliEvent:
  def __init__(self, probEventOccurs):
    self._eventProb = probEventOccurs
    self._eventArray = []
    
    arraySize = 100
    if self._eventProb >= 0.0 and self._eventProb <= 1.0:
      successCount = int(self._eventProb * arraySize)
      self._eventArray.extend([True]*successCount)
      self._eventArray.extend([False]*(arraySize-successCount))

  def isSuccess(self):
    return self._eventArray[random.randrange(0,len(self._eventArray))]

class WorldMap:
  def __init__(self, numberOfSeedPts, worldWidth, worldHeight):
    self.world_map = []
    self.numberOfSeedPts = numberOfSeedPts
    self.worldWidth = worldWidth
    self.worldHeight = worldHeight
    self.spawnLandEvent = BernoulliEvent(0.30)
    self.LandTile = 1
    self.SeaTile = 0
    self.totalWorldPoints = worldWidth * worldHeight;
   
    # Initialize all world map tiles to sea    
    for iLatitude in range(0,self.worldHeight):
      self.world_map.append([self.SeaTile]*self.worldWidth)
    
    # Initialize with seed points
    self.seedPts = deque()
    for seedPt in range(1,self.numberOfSeedPts+1):
      newSeedPt = self.getRandomWorldPoint()
      self.seedPts.append(newSeedPt)
      self.world_map[newSeedPt.row][newSeedPt.col] = self.LandTile
      
  def generateMap(self):
    numOfLandTiles = len(self.seedPts);
    targetNumOfLandTiles = self.totalWorldPoints * 0.40
    while numOfLandTiles<targetNumOfLandTiles:
      if not self.seedPts:
	currPt = self.getRandomWorldPoint()
        self.world_map[currPt.row][currPt.col] = self.LandTile
      else:
      	currPt = self.seedPts.popleft()
      newLandTiles = self.growMap(currPt)
      numOfLandTiles += len(newLandTiles)
      print numOfLandTiles
      self.seedPts.extend(newLandTiles)
  
  # Returns an array of new land points     
  def growMap(self, currPt):
    newLandPts = []
    vectorPts = [WorldPoint(-1, -1), WorldPoint(-1, 0), WorldPoint(-1, 1), 
                      WorldPoint(0, -1), WorldPoint(0, 1),
                      WorldPoint(1, -1), WorldPoint(1, 0), WorldPoint(1, 1)]
      
    for vectorPt in vectorPts:
      #vectorPt = vectorPts[vectorIndex]
      newRow = currPt.row + vectorPt.row
      newCol = currPt.col + vectorPt.col
      
      if newRow < 0: 
        newRow = self.worldHeight + newRow
      elif newRow >= self.worldWidth:
        newRow = newRow % self.worldHeight
        
      if newCol < 0: 
        newCol = self.worldHeight + newCol
      elif newCol >= self.worldWidth:
        newCol = newCol % self.worldHeight        
     
      # Only look at surrounding point if it is a sea tile
      if self.world_map[newRow][newCol] == self.SeaTile and self.spawnLandEvent.isSuccess():
        self.world_map[newRow][newCol] = self.LandTile
        newLandPts.append(WorldPoint(newRow, newCol))
        
    return newLandPts    
      
  def getRandomWorldPoint(self):
    randPt = WorldPoint(0,0)
    randPt.row = random.randrange(0, self.worldHeight)
    randPt.col = random.randrange(0, self.worldWidth)
    print randPt.row, " ", randPt.col
    return randPt

  def getCompressedMap(self):
    # Iterate over each map row and convert it from binary to hex string
    hexDigits = {"0000":"0", "0001":"1", "0010":"2", "0011":"3", "0100":"4",
                 "0101":"5", "0110":"6", "0111":"7", "1000":"8", "1001":"9",
                 "1010":"A", "1011":"B", "1100":"C", "1101":"D", "1110":"E",
                 "1111":"F"}
    
    hexMap = []
    for iRow in range(0,self.worldHeight):
      binaryStr = map(str,self.world_map[iRow])
      
      hexStr = ""
      for start in range(0, self.worldWidth, 4):
        bitGroup = string.join(binaryStr[start:start+4], "")

        hexStr += hexDigits[bitGroup]
        
      hexMap.append(hexStr)
      
    return hexMap

WORLD_WIDTH_TILES = 1000
WORLD_HEIGHT_TILES = 1000
worldMap = WorldMap(2, WORLD_WIDTH_TILES, WORLD_HEIGHT_TILES)
worldMap.generateMap()
world_map = worldMap.world_map

# Now that the landmass has been generated lets output it to 
# a file so it can be analyzed

# Open worldmap.txt for writing as buffered
#fileHandle = open('worldmap.txt', 'w', 1)

#for iRow in range(0,WORLD_HEIGHT_TILES):
#  latitudeStr = ",".join(map(str,world_map[iRow]))
#  fileHandle.write(latitudeStr)
#  fileHandle.write("\n")
  
#fileHandle.close()

compressed = worldMap.getCompressedMap()
fileHandle = open('worldmap_compress.txt', 'w', 1)
for iRow in range(0,WORLD_HEIGHT_TILES):
  fileHandle.write(compressed[iRow])
  fileHandle.write("\n")
fileHandle.close()

print "map generated!";
