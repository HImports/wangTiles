class Map{
  Tile[][] tiles;
  int tileWidth;
  int mapWidth;

  ArrayList<Tile> wangTiles;
  PImage tilesImage;
  int timeSinceMapBuild =0;
  
  
  void update(){}

 
  void drawGrid() {
    for (int x=0; x<mapWidth; x++) {
      line(tileWidth*x, 0, tileWidth*x, height);
    }
    for (int y=0; y<mapWidth; y++) {
      line(0, tileWidth*y, width, tileWidth*y);
    }
  }
  
  boolean isWithinMap(TileLoc loc) {
    return loc.x<mapWidth && loc.x >= 0 && loc.y<mapWidth && loc.y >= 0;
  }
  
  void draw() {
    for (int x=0; x<mapWidth; x++) {
      for (int y=0; y<mapWidth; y++) {
        if (tiles[x][y] != null) {
          tiles[x][y].draw(x, y);
        } else {
          fill(0, 100, 0, 100);
          rect(x*tileWidth, y*tileWidth, tileWidth, tileWidth);
        }
      }
    }
  }
  
}