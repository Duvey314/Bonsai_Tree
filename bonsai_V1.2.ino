/*
Bonsai Tree
Created on 3/20/2020
By: David M. Rudow
A small monsai tree created on a 8x8 bi-color LED Matrix. 

3/25/2020
-Added cases to make a state machine
-Added side branch case
-need to add leafs

3/26/2020
-Added leafs
-Added changing leaf color

3/31/2020
-added prune function

4/15/2020
-added leaf falling
-need to test for overlap so the whole screen doesn't turn red
-check fro branch over lap and that it's not overlapping a leaf (for loop from after the current leaf)

4/16/2020
-fixed leaf overlap

4/17/2020
-need to fix deletion of main branch when pruning first side branch
-figure out something before seed to show it's on

*/

#include <Entropy.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"

//declare states for state machine
enum treeState {seedState, mainBranchGrow, sideBranchGrow, leafGrow, leafChange, leafFall};         //
treeState state;

//prune button input and variables
const int pruneButton = 2;
int buttonVal = 0;                        // value read from button
int buttonLast = 0;                       // buffered value of the button's previous state
bool buttonFlag = false;

//timer variables
const unsigned long growInterval = 1000UL;     //time between each growth
const unsigned long leafInterval = 20000UL;   //time to wait before continuing changing leaves
unsigned long growTimer = 0UL;                //current growth interval
unsigned long leafTimer = 0UL;             //current leaf growing interval

const unsigned long debounce = 20UL;
const unsigned long holdTime = 1000UL;

unsigned long buttonTime = 0UL;           // time the button was pressed down

unsigned long previousBlink = 0;
unsigned long blinkInterval = 200;

//used for blink function
int blinkState = LOW;

//needed for the matrix functions
Adafruit_BicolorMatrix matrix = Adafruit_BicolorMatrix();

//declare main branch array, max length
int mainBranchX [7];
int mainBranchY [7];
int mainBranchMaxLength = 7;
int mainBranchLength = 1;
int mainBranchHolderX = 0;
int mainBranchHolderY = 0;

//declare side branch length and array
int sideBranchX[5];
int sideBranchY[5];
int sideBranchLength = 0;
int sideBranchMaxLength = 4;
int sideBranchHolderX = 0;
int sideBranchHolderY = 0;

//leaf variables
int leafTotal = 0;
int leafMax = 10;
int leafX[15];
int leafY[15];
int leafHolderX = 0;
int leafHolderY = 0;

bool leafAdded = false;

//leaf change variables
int leafChangeTotal = 0;
int leafFallTotal = 0;
bool fallStarted = false;
int fallDirection = 0;

//variable used as holder during growth, maybe make this multiple variable later  
int randomGrowth;

//time constants
const int seedTime = 1000;
const int admireTime = 2000;
const int growTime = 3000;






void setup() {
  
  Serial.begin(9600);
  Serial.println("Bonsai Buddy is Budding");

  pinMode(pruneButton, INPUT_PULLUP);

  growTimer = millis(); 

  matrix.begin(0x70);                       // pass in the address
  matrix.setRotation(2);
  matrix.setBrightness(15);
  matrix.fillRect(0,0, 7,7, LED_OFF);
  matrix.writeDisplay();  // write the changes we just made to the display

  Entropy.initialize();                     //initialize the entropy function for random numbers

}








void loop() {
  
  buttonVal = digitalRead(pruneButton);
  
  if (buttonVal == LOW && buttonLast == HIGH){
    buttonTime = millis();
    buttonFlag = true;
  }
  
  if (buttonVal == LOW && buttonFlag == true){
    if(millis() - previousBlink >= blinkInterval){
      previousBlink = millis();
      pruneBlink();
    }
  }
  
  if (buttonVal == LOW && ((millis() - buttonTime) >= holdTime) && buttonFlag == true){
    prune();
    buttonFlag = false;
  }
  
  buttonLast = buttonVal;

if ((millis() - growTimer) >= growInterval){
  switch(state){
    case seedState:
      plantSeed();
      state = mainBranchGrow;
      break;

    case mainBranchGrow:
      if (mainBranchLength < mainBranchMaxLength){
        mainBranchAdd();
        state = mainBranchGrow;
        }
      else{
        Serial.println("Main Branch Growth Reached");
        state = sideBranchGrow;
      }
      break;

    case sideBranchGrow:      
      if (sideBranchLength < sideBranchMaxLength){
        sideBranchAdd();
        state = sideBranchGrow;
      }
      else{ 
        state = leafGrow;
      }
      break;

      case leafGrow:
        if (leafTotal < leafMax){
          leafAdd();
          state = leafGrow;
        }
        else{
          state = leafChange;
        }
        break;

      case leafChange:
        if (leafChangeTotal < leafTotal){
          leafChangeColor();
          state = leafChange;
        }
        else{
          state = leafFall;
        }
        break;

      case leafFall:
        if (leafFallTotal < leafTotal){
          leafFallAnimate();
          state = leafFall;
        }
        else{
          delay(1000*10);
          resetTree();
          state = seedState; 
        }
  }
  growTimer = millis();
  }
}




















void plantSeed()
  {
  Serial.println("Planting Seed...");
  
  mainBranchX[0] = Entropy.random(0, 8);
  mainBranchY[0] = 0;
  
  matrix.drawPixel(mainBranchY[0], mainBranchX[0], LED_YELLOW);
  matrix.writeDisplay();
  
  Serial.print("Seed Location Selected: ");
  Serial.print(mainBranchX[0]);
  Serial.println(mainBranchY[0]);
  
  return;
  }


  
void mainBranchAdd ()
  {
    mainBranchHolderX = (mainBranchX[mainBranchLength-1] - 1 + Entropy.random(0,3));
    
    if (edgeDetected(mainBranchHolderX, 0) == false){
      
      mainBranchY[mainBranchLength] = mainBranchLength;
      mainBranchX[mainBranchLength] = mainBranchHolderX;
      
      matrix.drawPixel(mainBranchY[mainBranchLength], mainBranchX[mainBranchLength], LED_YELLOW);  
      matrix.writeDisplay();
      
      Serial.print("Growth Added At: ");
      Serial.print(mainBranchX[mainBranchLength]); 
      Serial.println(mainBranchY[mainBranchLength]);
      Serial.print("Main Branch Length: ");
      Serial.println(mainBranchLength);

      mainBranchLength++;
    }
  return;
  }  



void sideBranchAdd ()
  {
    if (sideBranchLength == 0) {                              //if no branch has been added, choose a random piece of the main branch to start from
      randomGrowth = Entropy.random(1,6);                     
      sideBranchX[0] = mainBranchX[randomGrowth];
      sideBranchY[0] = mainBranchY[randomGrowth];
      sideBranchLength++;
      }
    
        if (sideBranchX[0] < 4){                              //if the starting point is on the left side of the screen, grow right
          sideBranchX[sideBranchLength] = sideBranchX[0]+sideBranchLength;
          Serial.println("The branch is growing right");
        }
        else{
          sideBranchX[sideBranchLength] = sideBranchX[0]-sideBranchLength;
          Serial.println("The branch is growing left");
        }     
      
      randomGrowth = (sideBranchY[sideBranchLength-1] - 1 + Entropy.random(0,3));
      
      sideBranchY[sideBranchLength] = randomGrowth;  //Y branch growth
   
      matrix.drawPixel(sideBranchY[sideBranchLength], sideBranchX[sideBranchLength], LED_YELLOW);  
      matrix.writeDisplay();

      Serial.print("Branch Added at:");
      Serial.print(sideBranchX[sideBranchLength]);
      Serial.println(sideBranchY[sideBranchLength]);
      Serial.print("Side Branch Length: ");
      Serial.println(sideBranchLength);
      
      sideBranchLength++;
 
      return;
    }
    
void leafAdd(){
  randomGrowth = Entropy.random(2);
  leafAdded = false;
  if (randomGrowth == 1){                                 //decide between growing a leaf on the branch or trunk
    randomGrowth = Entropy.random(3,8);
    leafHolderX = mainBranchX[randomGrowth] - 1 + Entropy.random(3);
    leafHolderY = mainBranchY[randomGrowth] - 1 + Entropy.random(3);
  }
  else{
    randomGrowth = Entropy.random(1,4);
    leafHolderX = sideBranchX[randomGrowth] - 1 + Entropy.random(3);
    leafHolderY = sideBranchY[randomGrowth] - 1 + Entropy.random(3);
  }
  if (edgeDetected(leafHolderX, leafHolderY) == false && 
      leafHolderY > 0 &&
      overlapDetectedLeaf(leafHolderX, leafHolderY) == false &&
      overlapDetectedMainBranch(leafHolderX, leafHolderY) == false &&
      overlapDetectedSideBranch(leafHolderX, leafHolderY) == false){

    leafX[leafTotal] = leafHolderX;
    leafY[leafTotal] = leafHolderY;      
    matrix.drawPixel(leafY[leafTotal], leafX[leafTotal], LED_GREEN);  
    matrix.writeDisplay();

    Serial.print("Leaf added at: ");
    Serial.print(leafX[leafTotal]);
    Serial.println(leafY[leafTotal]);
    Serial.print("Number of leafs:");
    Serial.println(leafTotal);

    leafAdded = true;
    
    leafTotal++;
  }
  if (leafAdded == true){
    return;
  }
}


void leafChangeColor(){
  matrix.drawPixel(leafY[leafChangeTotal], leafX[leafChangeTotal], LED_RED);
  matrix.writeDisplay();
  
  Serial.print("Leaf color changed at: ");
  Serial.print(leafX[leafChangeTotal]);
  Serial.println(leafY[leafChangeTotal]);

  leafChangeTotal++;

  return;
}

void leafFallAnimate(){
  if (leafY[leafFallTotal] > 0){                                                 //If the leaf hasn't reached the ground, fall more
    if (fallStarted == false){                                      //start the leaf falling and making fure it doesn't fall off the screen
      matrix.drawPixel(leafY[leafFallTotal], leafX[leafFallTotal], LED_OFF);     //clear the pixel the leaf starts in
      matrix.writeDisplay();

      fallDirection = Entropy.random(2);
      fallStarted = true;
      if (leafX[leafFallTotal] == 0){                               //the leaf starts falling to the right(like it just fell left)
        leafX[leafFallTotal]++;             //move the x value one to the right
        fallDirection = 1;
      }                                                             //next time the leaf will know which way it just fell      
      else if (leafX[leafFallTotal] == 7){
        leafX[leafFallTotal]--;
        fallDirection = 0;
      }
      else if (fallDirection == 0){
        leafX[leafFallTotal]++;
        fallDirection = 1;
      }
      else if (fallDirection == 1){
        leafX[leafFallTotal]--;
        fallDirection = 0;
      }
    leafY[leafFallTotal]--;

    Serial.println("Leaf Started Falling");
    
    matrix.drawPixel(leafY[leafFallTotal], leafX[leafFallTotal], LED_RED);
    matrix.writeDisplay();
    
    delay(500);
    }
    for (int h = leafY[leafFallTotal]-1; h  >= 0 ; h--){
      if(overlapDetectedMainBranch(leafX[leafFallTotal],leafY[leafFallTotal]) == true || overlapDetectedSideBranch(leafX[leafFallTotal],leafY[leafFallTotal]) == true){
        matrix.drawPixel(leafY[leafFallTotal], leafX[leafFallTotal], LED_YELLOW);
        matrix.writeDisplay();
      }
      else if(overlapDetectedLeafFall(leafX[leafFallTotal],leafY[leafFallTotal], leafFallTotal) == false){
        matrix.drawPixel(leafY[leafFallTotal], leafX[leafFallTotal], LED_OFF);
        matrix.writeDisplay();
      }
      if (fallDirection == 0){
        leafX[leafFallTotal]++;
        fallDirection = 1;
      }
      else if (fallDirection == 1){
        leafX[leafFallTotal]--;
        fallDirection = 0;
      }
      leafY[leafFallTotal] = h;
      
      matrix.drawPixel(leafY[leafFallTotal], leafX[leafFallTotal], LED_RED);
      matrix.writeDisplay();

      Serial.println("Leaf Fell a Bit");
      Serial.println(h);
      
      delay(500);
    }
  }
  else{
    leafFallTotal++;
    fallStarted = false;
    return;
  }
}


void resetTree(){
  mainBranchLength = 1;
  sideBranchLength = 0;
  leafTotal = 0;
  leafChangeTotal = 0;
  leafFallTotal = 0; 
  
  matrix.clear();
  
  Serial.println("The royal tree is clean your highness");

  return;
}

bool edgeDetected(int growthCheckX, int growthCheckY)
  {
  if (growthCheckX > 7 || growthCheckX < 0 ||
      growthCheckY > 7 || growthCheckY < 0){
    Serial.println("Edge Detected");
    return true;
    
  }
  else{
    Serial.println("No Edge Detected");
    return false;
  }
}

bool overlapDetectedMainBranch(int positionMainBranchX, int positionMainBranchY){
  for (int i = 0; i < mainBranchMaxLength; i++){
    if (positionMainBranchX == mainBranchX[i] && positionMainBranchY == mainBranchY[i]){
      Serial.println("Overlap Detected on Main Branch");
      return true;
    }
  }
  Serial.println("No Overlap Detected on Main Branch");
  return false;
}

bool overlapDetectedSideBranch(int positionSideBranchX, int positionSideBranchY){
  for (int j = 0; j < sideBranchMaxLength; j++){
    if (positionSideBranchX == sideBranchX[j] && positionSideBranchY == sideBranchY[j]){
      Serial.println("Overlap Detected on side Branch");
      return true;
    }
  }
  Serial.println("No Overlap Detected on side Branch");
  return false;
}  

bool overlapDetectedLeaf(int positionLeafX, int positionLeafY){
  for (int k = 0; k < leafMax; k++){
    if (positionLeafX == leafX[k] && positionLeafY == leafY[k]){
      Serial.println("Overlap Detected on Leaf");
       return true;
    }  
  }
  Serial.println("No Overlap Detected on Leaf");
  return false;
}

bool overlapDetectedLeafFall(int positionLeafFallX, int positionLeafFallY, int leafNumber){
  for (int l = leafNumber+1; l < leafMax; l++){
    if (positionLeafFallX == leafX[l] && positionLeafFallY == leafY[l]){
      Serial.println("Overlap Detected on Leaf");
       return true;
    }  
  }
  Serial.println("No Overlap Detected on Leaf");
  return false;
}

void prune(){
  if (state == mainBranchGrow){
    if (mainBranchLength > 1){
      mainBranchLength--;
      
      matrix.drawPixel(mainBranchY[mainBranchLength], mainBranchX[mainBranchLength], LED_OFF);  
      matrix.writeDisplay();
      
      Serial.print("Branch Pruned at: ");
      Serial.print(mainBranchX[mainBranchLength]); 
      Serial.println(mainBranchY[mainBranchLength]);
      //Serial.print("Main Branch Length: ");
      //Serial.println(mainBranchLength);
    }
  }
  if (state == sideBranchGrow){
    if (sideBranchLength > 0){
      sideBranchLength--;

      matrix.drawPixel(sideBranchY[sideBranchLength], sideBranchX[sideBranchLength], LED_OFF);  
      matrix.writeDisplay();
      
      Serial.print("Branch Pruned at: ");
      Serial.print(sideBranchX[sideBranchLength]); 
      Serial.println(sideBranchY[sideBranchLength]);
    }
  }
  if (state == leafGrow){
    if (leafTotal > 0){
      leafTotal--;

      matrix.drawPixel(leafY[leafTotal], leafX[leafTotal], LED_OFF);
      matrix.writeDisplay();

      Serial.print("Leaf Pruned at: ");
      Serial.print(leafX[leafTotal]);
      Serial.println(leafY[leafTotal]);
    }
  }
  return;
}

void pruneBlink(){
if (buttonFlag == true){
  if (state == mainBranchGrow){
      if (mainBranchLength > 1){
        mainBranchLength--;
        if(blinkState == LOW){
          blinkState = HIGH;
          matrix.drawPixel(mainBranchY[mainBranchLength], mainBranchX[mainBranchLength], LED_OFF);  
          matrix.writeDisplay();
        }
        else if(blinkState == HIGH){
          blinkState = LOW;
          matrix.drawPixel(mainBranchY[mainBranchLength], mainBranchX[mainBranchLength], LED_YELLOW);  
          matrix.writeDisplay();
        }
      }
      mainBranchLength++;
    }
    if (state == sideBranchGrow){
      if (sideBranchLength > 0){
        sideBranchLength--;
        if(blinkState == LOW){
          blinkState = HIGH;
          matrix.drawPixel(mainBranchY[mainBranchLength], mainBranchX[mainBranchLength], LED_OFF);  
          matrix.writeDisplay();
        }
        else if(blinkState == HIGH){
          blinkState = LOW;
          matrix.drawPixel(mainBranchY[mainBranchLength], mainBranchX[mainBranchLength], LED_YELLOW);  
          matrix.writeDisplay();
      }
    }
    sideBranchLength++;
    }
    if (state == leafGrow){
      if (leafTotal > 0){
        leafTotal--;
        if(blinkState == LOW){
          blinkState = HIGH;
          matrix.drawPixel(mainBranchY[mainBranchLength], mainBranchX[mainBranchLength], LED_OFF);  
          matrix.writeDisplay();
        }
        else if(blinkState == HIGH){
          blinkState = LOW;
          matrix.drawPixel(mainBranchY[mainBranchLength], mainBranchX[mainBranchLength], LED_GREEN);  
          matrix.writeDisplay();
      }
    }
    leafTotal++;
    }
}
  return;
}  
   
