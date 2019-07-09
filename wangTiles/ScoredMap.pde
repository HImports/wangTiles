class ScoredMap extends Map {

  ScoredMap(ScoredMap toCopy) {
    tiles = toCopy.getTilesCopy();
    mapWidth = toCopy.mapWidth;
    tileWidth = toCopy.tileWidth;
    timeSinceMapBuild = 0; //reset so that this map's processing time counts from 0
    wangTiles = wangTiles;
  }

  ScoredMap(int imapWidth, int itileWidth) {
    tilesImage = loadImage(FILENAME);
    mapWidth = imapWidth;
    tileWidth = itileWidth;
    timeSinceMapBuild = 0; //reset so that this map's processing time counts from 0
    wangTiles = parseTilesIntoSet();
    normalizeTileLikelyhoods(wangTiles);
    tiles = new Tile[mapWidth][mapWidth];
    ArrayList<PVector> tileLocs = new ArrayList<PVector>();
    for (int x=0; x<mapWidth; x++) {
      for (int y=0; y<mapWidth; y++) {
        tileLocs.add(new PVector(x, y));
      }
    }
    Collections.shuffle(tileLocs);
    for (PVector test : tileLocs) {
      placeBestTile((int)test.x,(int)test.y);//placeRandomTileAt((int)test.x, (int)test.y);
    }
    print (wangTiles);
    tiles = new ConstrainedMap(mapWidth,tileWidth).tiles;
  }

  void update() {
    textSize(24);
    text(mapScore(), 20, 20);
    improveMethod3();
    //for (int i=0; i<50; i++) {
     // tryRandomizingRegion();
   // }
  }
  
  void improveMethod3(){
    for (int x=0; x<mapWidth; x++) {
      for (int y=0; y<mapWidth; y++) {
        placeBestTile(x, y);
      }
    }
  }

  ArrayList<TileLoc> getTilesInRandomOrder(){
   ArrayList<TileLoc> tileLocs = new ArrayList<TileLoc>();
    for (int x=0; x<mapWidth; x++) {
      for (int y=0; y<mapWidth; y++) {
        tileLocs.add(new TileLoc(x, y));
      }
    }
    Collections.shuffle(tileLocs);
    return tileLocs; 
  }

  void placeBestTile(int x, int y){
    float bestScore = -9999999;
    ArrayList<Tile>bestTiles = new ArrayList<Tile>();
    for (Tile tile : wangTiles){
      float score = placementScore(tile,x,y);
      if (placementScore(tile,x,y)>bestScore){
        bestScore = placementScore(tile,x,y);
        bestTiles = new ArrayList<Tile>();
        bestTiles.add(tile);
      }
    }
    tiles[x][y] = bestTiles.get((int)random(bestTiles.size()));
  }
  
  void placeWeightedGuess(int x, int y){
    int weightSum =0;
    for (Tile test : wangTiles){
      weightSum += test.likelyhood+1000*placementScore(test, x, y);
     
    }
    int choice = (int)random(weightSum);
    Collections.shuffle(wangTiles);
    for (Tile test2 : wangTiles){
      choice -= test2.likelyhood+1000*placementScore(test2,x,y);
      if(choice<=0){
        tiles[x][y] = test2;
      }
    }
   
  }



  void randomizeRegion (int x1, int y1, int x2, int y2) {
    assert (x1<x2 && y1<y2);
    for (int x = x1; x<x2; x++) {
      for (int y = y1; y<y2; y++) {
        placeRandomTileAt(x, y);
      }
    }
  }

  void tryRandomizingRegion() {
    //print("hello");
    ScoredMap otherOption = new ScoredMap(this);
    int windowWidth = (int) random(2, 14);
    int x1 = int(random(mapWidth-windowWidth+1));
    int y1 = int(random(mapWidth-windowWidth+1));
    int x2 = x1+windowWidth;
    int y2 = y1+windowWidth;
    int numTriesPerRegion = 4;
    for ( int i=0; i<numTriesPerRegion; i++) {
      otherOption.randomizeRegion(x1, y1, x2, y2);

      if (otherOption.regionScore(x1, y1, x2, y2)>regionScore(x1, y1, x2, y2)) {
      //if (otherOption.mapScore()>mapScore()) {
        tiles = otherOption.getTilesCopy();
        //print("found a better map");
      }
    }
  }


 ArrayList<Tile> getViableTiles(int x, int y){
   //returns non zero score tiles.  If none exists, returns all tiles.
   ArrayList<Tile> result = new ArrayList<Tile>();
   for (Tile tile : wangTiles){
     if (placementScore(tile,x,y)>0){
       result.add(tile);
     }
   }
   if (result.size()>0){
   return result;
   }
   else{
     return wangTiles;
   }
 }


  void placeRandomTileAt(int x, int y) {
    int ex = x;//(int)random(mapWidth);
    int why = y;//(int)random(mapWidth);
    Tile tile=null;

    //tile =  wangTiles.get((int)random(wangTiles.size()));
    //tile =  getRandomChoice(wangTiles);
    ArrayList<Tile> choices = getViableTiles(x, y);
    tile = getRandomChoice(choices);
    //tile =  choices.get((int)random(choices.size()));
    tiles[ex][why] = tile;
  }

  float regionScore(int x1, int y1, int x2, int y2) {
    float result = 0;
    for (int x = x1; x<x2; x++) {
      for (int y = y1; y<y2; y++) {
        result += placementScore(tiles[x][y], x, y);
      }
    }
    return result;
  }


  float mapScore() {
    float result = 0;
    for (int x=0; x<mapWidth; x++) {
      for (int y=0; y<mapWidth; y++) {
        result += placementScore(tiles[x][y], x, y);
      }
    }
    return result/(mapWidth*mapWidth)/4.0;
  }

  float placementScore (Tile tile, int tileX, int tileY) {
    float result =  
      scoreOfNeighbor(tile, tileX, tileY, tileX+1, tileY) +
      scoreOfNeighbor(tile, tileX, tileY, tileX-1, tileY) +
      scoreOfNeighbor(tile, tileX, tileY, tileX, tileY+1) +
      scoreOfNeighbor(tile, tileX, tileY, tileX, tileY-1);

    return result;
  }

  float scoreOfNeighbor(Tile tile, int tileX, int tileY, int neighborX, int neighborY) {
    if (neighborX>=mapWidth || neighborY>=mapWidth || neighborX<0 || neighborY<0 || tile == null) {
      return 1;
    } else {

      Directions direction = getDirectionFromDelta(neighborX-tileX, neighborY-tileY);             
      return tile.edgeFractionInCommonWithNeighbor(tiles[neighborX][neighborY], direction);
    }
  }
}