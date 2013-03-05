
// definitions
// pins 0, 1 reserved for serial comm, pins 2,3 reserved for interrupts

//pin definitions
#define grinder1Button 4            // grinder1Button on digital pin 4
#define grinder2Button 5            // grinder2Button on digital pin 5
#define grinder3Button 6            // grinder3Button on digital pin 6
#define grinder1Relay 7             // grinder1Relay on digital pin 7
#define grinder2Relay 8             // grinder2Relay on digital pin 8
#define grinder3Relay 9             // grinder3Relay on digital pin 9
#define barLatchPin 10              // shift register bar latch on digital pin 10
#define shiftDataPin 11             // shift reigister data on digital pin 11
#define shiftClockPin 12            // shift register clock on digital pin 12
#define preGrindButton 13           // Button used to activate preGrindFlag and exit pre grind phase
#define pot A1                      // Analog pot on analog pin A1
#define segmentLatchPin A2          // shift register segment latch on analog pin A2
#define grinderLed1 A3              // grinder LED 1 on analog pin A3
#define grinderLed2 A5              // grinder LED 2 on analog pin A3
#define grinderLed3 A4              // grinder LED 3 on analog pin A3

//flag definitions 
#define preGrind 0
#define idle 1
#define grinding 2
#define orderComplete 3
#define readyToBrew 4
#define blendSelected 5
#define requestAllowed 6
#define requestDenied 7
#define pulseComplete 8
#define grinderComplete 9
#define customerComplete 10
#define grindingRequest 11
#define reset 12

//--------------------------------------------------------------------------------------

// variables

//arrays

int grinderButtonPins[] = { 
  grinder1Button, grinder2Button, grinder3Button };   // an array of pin numbers to which grinder buttons are attached
int grinderButtonPinCount = 3;                        // the number of pins (i.e. the length of the array)

int grinderRelayPins[] = { 
  grinder1Relay, grinder2Relay, grinder3Relay };      // an array of pin numbers to which grinder relays are attached
int grinderRelayPinCount = 3;                         // the number of pins (i.e. the length of the array)

int grinderLedPins[] = { 
  grinderLed1, grinderLed2, grinderLed3 };
int grinderLedPinCount = 3;

int grinderButtonState[] = { 
  0,0,0};                                             // an array to store state of grinder buttons, initialized as 0's

byte dataArrayBAR[9] = {

  dataArrayBAR[0] = 0xFF, //11111111
  dataArrayBAR[1] = 0x7F, //01111111
  dataArrayBAR[2] = 0x3F, //00111111
  dataArrayBAR[3] = 0x1F, //00011111
  dataArrayBAR[4] = 0x0F, //00001111
  dataArrayBAR[5] = 0x07, //00000111
  dataArrayBAR[6] = 0x03, //00000011
  dataArrayBAR[7] = 0x01, //00000001
  dataArrayBAR[8] = 0x00};//00000000

byte dataArraySEGMENT[17] = {

  dataArraySEGMENT[0] = 0x84,    //number 0
  dataArraySEGMENT[1] = 0xF5,    //number 1
  dataArraySEGMENT[2] = 0xC8,    //number 2
  dataArraySEGMENT[3] = 0xD0,    //number 3
  dataArraySEGMENT[4] = 0xB1,    //number 4
  dataArraySEGMENT[5] = 0x92,    //number 5
  dataArraySEGMENT[6] = 0x83,    //number 6
  dataArraySEGMENT[7] = 0xF4,    //number 7
  dataArraySEGMENT[8] = 0x80,    //number 8
  dataArraySEGMENT[9] = 0xB0,    //number 9
  dataArraySEGMENT[10] = 0xFF,  //segment OFF
  dataArraySEGMENT[11] = 0xBF,    //number 0
  dataArraySEGMENT[12] = 0xEF,    //number 1
  dataArraySEGMENT[13] = 0xDF,    //number 2
  dataArraySEGMENT[14] = 0xF7,    //number 3
  dataArraySEGMENT[15] = 0xFD,    //number 4
  dataArraySEGMENT[16] = 0xFE};    //number 5

int blendTimeArray[10][3] = {
  {
    125,125,125 }           //custom creation
  ,
  {
    25,50,25 }              //golden gate
  ,
  {
    50,40,10 }              //stanford cardinal
  ,
  {
    50,0,50 }              //fog city
  ,
  {
    100,0,0  }              //single origin, ethiopia
  ,
  {
    0,100,0  }              //single origin, colombia
  ,
  {
    0,0,100  }              //single origin, indonesia
  ,
  {
    33,33,33 }              //place holder
  ,
  {
    11,22,67 }              //place holder
  ,
  {
    5,5, 90  }              //place holder
};


int ledArray[10][3];

int blendSelectionArray[3];

int ledSelectionArray[3];

int blendCustomArray[3];

byte dataBAR;                        // byte to shift out to LED BAR display
byte dataSEGMENT;                    // byte to shift out to LED BAR display

int displayArray;                    // element of array to call
int previousDisplayArray;            // previous element of display array
int thisPin;                         // for loop iteration element 
int grinderStatus;                   // variable to determine if grinder is on or off (3 = off, 2 = on)
int stateFlag;                       // state machine flag 
int potValue;                        // variable to store value of pot
int blendRecipe;                     // variable to store what recipe is wanted, determined by pot value
int blendTimeElementSum;             // variable to store the sum of the total time/pulses left for the blendRecipe
int preGrindButtonState;             // variable to store state of pre grind button
int firstTimeHere;                       // variable to determine if first time entering loop
int n;                               // loop counter
int x;                               // loop counter
float pulse;                         // during custom control, counts number of pulses completed
float pulseMax = 40;                  // during custom control, number of pulses allowed for order ARBITRARY VALUE
int grinderRequest;                  // variable to determine which grinder is requested to turn on
int requestFlag;                     // grinder request flag 
float pulsePercentage;
char grinderPercentage0[8];
char grinderPercentage1[8];
char grinderPercentage2[8];
int dataOut;
String stringOne;
String stringTwo;
String stringThree;
String stringFour;
String stringFive;
String stringSix;
float grinderPercentage[3];
long totalTime = 9000;
long grindTime;
int blendPercentage[3];
int grinderLEDflash;
//--------------------------------------------------------------------------------------

// prototypes

void checkGrinderSwitches(void);
void grindCounter(void);
void handleGrinders(void);
void startGrinders(void);
void stopGrinders(void);
void updateDisplay(void); 
void shiftOut(int myDataPin, int myClockPin, byte myDataOut);
void resetVariables(void);
void readPot(void);
void checkPreGrindButton(void);
void displayLatchesLow(void);
void populateLedArray(void);
void setGrinderState(void);
void firstTime(void);
void blendSetup(void);
void grinderLEDS(void);
void printData(void);

//--------------------------------------------------------------------------------------

//setup function

void setup (){

  Serial.begin(9600);          //starts serial with baud of 9600

    // the array elements are numbered from 0 to (pinCount - 1).
  // use a for loop to initialize each grinder button pin as an input:
  for (int thisPin = 0; thisPin < grinderButtonPinCount; thisPin++)  {
    pinMode(grinderButtonPins[thisPin], INPUT);      
  }

  // the array elements are numbered from 0 to (pinCount - 1).
  // use a for loop to initialize each grinder relay pin as an output:
  for (int thisPin = 0; thisPin < grinderButtonPinCount; thisPin++)  {
    pinMode(grinderRelayPins[thisPin], OUTPUT);      
  }

  for (int thisPin = 0; thisPin < grinderLedPinCount; thisPin++)  {
    pinMode(grinderLedPins[thisPin], OUTPUT);      
  }

  populateLedArray();

  pinMode(barLatchPin, OUTPUT);             // Set bar latch pin as output
  pinMode(segmentLatchPin, OUTPUT);         // Set segment latch pin as output
  pinMode(preGrindButton, INPUT);           // Set pre grind button pin as input
  pinMode(pot, INPUT);                      // Set pre grind button pin as input

  digitalWrite(grinder1Button, HIGH);       // turn on pullup resistors. Wire button so that press shorts pin to ground
  digitalWrite(grinder2Button, HIGH);       // turn on pullup resistors. Wire button so that press shorts pin to ground
  digitalWrite(grinder3Button, HIGH);       // turn on pullup resistors. Wire button so that press shorts pin to ground
  digitalWrite(preGrindButton, HIGH);       // turn on pullup resistors. Wire button so that press shorts pin to ground
  digitalWrite(grinder1Relay, LOW);         // Set pin LOW to have relay initialized off
  digitalWrite(grinder2Relay, LOW);         // Set pin LOW to have relay initialized off
  digitalWrite(grinder3Relay, LOW);         // Set pin LOW to have relay initialized off
  digitalWrite(grinderLed1, LOW);           // Set pin LOW to have led initialized off
  digitalWrite(grinderLed2, LOW);           // Set pin LOW to have led initialized off
  digitalWrite(grinderLed3, LOW);           // Set pin LOW to have led initialized off
  digitalWrite(barLatchPin, LOW);           // Set pin LOW to have LED bar display initialized off
  digitalWrite(segmentLatchPin, LOW);       // Set pin LOW to have LED segment display initialized off

  //attachInterrupt(0, checkGrinderSwitches, CHANGE); // interrupt on digital pin 2, calls function checkGrinderSwitches on a change in state

  resetVariables();  //function call to initilize variables
  
  stateFlag = preGrind;
}

//--------------------------------------------------------------------------------------

//main loop

void loop (){
  if (stateFlag == preGrind){
    firstTime();
    readPot();
    updateDisplay();
    checkPreGrindButton();
  }

  if (stateFlag == blendSelected){
    blendSetup();
    updateDisplay();
    grinderLEDS(); 
    stateFlag = idle;
  }

  if (stateFlag == idle){
    firstTime();
    checkGrinderSwitches();
    handleGrinders();
    updateDisplay();
  }

  if (stateFlag == grindingRequest){
    setGrinderState();
    handleGrinders();
    updateDisplay();
  }
        
   if (stateFlag == grinding){
    grindCounter();
    printData();
    handleGrinders();
    grinderLEDS(); 
    updateDisplay();
  }

  if (stateFlag == readyToBrew){
    firstTime();
    //printData();
    grinderLEDS();
    updateDisplay();    
    checkPreGrindButton();
  }

  if (stateFlag == customerComplete){
    firstTime();
    printData();
    updateDisplay();    
    checkPreGrindButton();
  }
  
  if (stateFlag == reset){
    firstTime();
    updateDisplay();
    printData();
    resetVariables();
    stateFlag = preGrind;
    }
}


//--------------------------------------------------------------------------------------

//functions

void checkGrinderSwitches(void){
  grinderStatus = 0;
  
  for (int thisPin = 0; thisPin < grinderButtonPinCount; thisPin++) {  //for loop to read in current values of grinderButtonPins
    grinderButtonState[thisPin] = digitalRead(grinderButtonPins[thisPin]); 
    grinderStatus += grinderButtonState[thisPin];
  }
  
  if (grinderStatus != 0){
    stateFlag = grindingRequest;
  }
}

void firstTime(void){
  if (firstTimeHere == true && stateFlag == preGrind){
    delay(1000);
    firstTimeHere = false;
   }

   if (firstTimeHere == true && stateFlag == idle){
    updateDisplay();
    displayArray = 10;
    firstTimeHere = false;
   }

   if (firstTimeHere == true && stateFlag == readyToBrew){
     for (int i = 0; i < 3; i++) { 
      ledSelectionArray[i]=0;
      }
    grinderLEDflash = true;
    firstTimeHere = false;
    //dataOut = true;
   }

   if (firstTimeHere == true && stateFlag == customerComplete){
    delay(1000);    
    firstTimeHere = false;
    displayArray = 0;
    dataOut = true;
   }

   if (firstTimeHere == true && stateFlag == reset){
    firstTimeHere = false;
    dataOut = true;
   }
}

void blendSetup(void){
   if(blendRecipe !=0){ 
    for (int i = 0; i < grinderButtonPinCount; i++) {  
        grindTime = (blendTimeArray[blendRecipe][i])*totalTime;
        blendSelectionArray[i] = (grindTime)/100; 
        ledSelectionArray[i] = ledArray[blendRecipe][i];
      }
    }
    else if(blendRecipe == 0){
       for (int i = 0; i < grinderButtonPinCount; i++) { 
      blendSelectionArray[i] = (blendTimeArray[blendRecipe][i]);
      ledSelectionArray[i] = ledArray[blendRecipe][i];
       }
    }
    firstTimeHere = true;
}

void startGrinders(void){
      digitalWrite(grinderRelayPins[grinderRequest], HIGH);   //turns on requested grinder
}

void stopGrinders(void){
  for (int thisPin = 0; thisPin < grinderButtonPinCount; thisPin++)  {
    digitalWrite(grinderRelayPins[thisPin], LOW);     //turns off all grinders
  }
}

void grinderLEDS(void){
  if(stateFlag == readyToBrew && grinderLEDflash == true){
    x=0;
    while (x<8){
      for (int i = 0; i < 3; i++) { 
        digitalWrite(grinderLedPins[i], 1);
      }
      delay(75);
      for (int i = 0; i < 3; i++) { 
        digitalWrite(grinderLedPins[i], 0);
      }
      delay(75);
      x++;
    }
    grinderLEDflash = false;
  }

  else {
    for (int i = 0; i < 3; i++) { 
      digitalWrite(grinderLedPins[i], ledSelectionArray[i]);
    }
  }
}

void handleGrinders(void){
  if(requestFlag == requestAllowed){
    startGrinders();
    stateFlag = grinding;
  }
  else if (requestFlag == requestDenied){
      if (stateFlag == orderComplete){
          stopGrinders();
          firstTimeHere = true;
          stateFlag = readyToBrew;
      }
      else if (stateFlag == grinderComplete || stateFlag == pulseComplete){
        stopGrinders();
        stateFlag = idle;
     } 
  }  
}

void grindCounter(void){
  if(blendRecipe == 0){
    delay(blendSelectionArray[grinderRequest]);
    pulse++;
    blendCustomArray[grinderRequest] += 1;
    pulsePercentage = (pulse*100)/pulseMax;
   // Serial.println(pulsePercentage);
   // dtostrf(pulsePercentage, 2, 2, pulsePercentageChar);
   // stringOne = "pulsePercentageOverall ";
   // stringTwo= stringOne + pulsePercentageChar;
   // Serial.println(stringTwo);
      for (int x = 0; x < grinderButtonPinCount; x++)  {
         grinderPercentage[x] = (blendCustomArray[x]*100)/pulseMax;
      }
         dtostrf(grinderPercentage[0], 2, 2, grinderPercentage0);
         dtostrf(grinderPercentage[1], 2, 2, grinderPercentage1);
         dtostrf(grinderPercentage[2], 2, 2, grinderPercentage2);
         stringOne = "grinderPercentage ";
         stringTwo= stringOne + grinderPercentage0;
         stringThree= stringTwo + " ";
         stringFour= stringThree + grinderPercentage1;
         stringFive= stringFour + " ";
         stringSix= stringFive + grinderPercentage2;
         dataOut = true; 
  
    requestFlag = requestDenied;
    stateFlag = pulseComplete;
    
    if (pulse >= pulseMax){
      requestFlag = requestDenied;
      stateFlag = orderComplete;
    }
  }
  else if (blendRecipe != 0){
    delay(blendSelectionArray[grinderRequest]);
    blendPercentage[grinderRequest] = blendTimeArray[blendRecipe][grinderRequest];
         stringOne = "grinderPercentage ";
         stringTwo= stringOne + blendPercentage[0];
         stringThree= stringTwo + " ";
         stringFour= stringThree + blendPercentage[1];
         stringFive= stringFour + " ";
         stringSix= stringFive + blendPercentage[2];
         dataOut = true; 
    
    blendSelectionArray[grinderRequest] = 0;
    ledSelectionArray[grinderRequest] = 0;
    blendTimeElementSum = 0;
    for(int i=0; i<3;i++){
      blendTimeElementSum += blendSelectionArray[i];
    }
    if(blendTimeElementSum == 0){
      requestFlag = requestDenied;
      stateFlag = orderComplete;
    }
    else if (blendTimeElementSum != 0){
      requestFlag = requestDenied;
      stateFlag = grinderComplete;
    }  
  }
}

void printData(){
  if (dataOut == true && (stateFlag == orderComplete || stateFlag == grinderComplete || stateFlag == pulseComplete)){
    Serial.println(stringSix);
    dataOut = false;
   }

   if (dataOut == true && stateFlag == readyToBrew){
    Serial.println("readyToBrew");
    dataOut = false;
   }
   if (dataOut == true && stateFlag == customerComplete){
    Serial.println("complete");
    dataOut = false;
   }
   if (dataOut == true && stateFlag == reset){
    Serial.println("reset");
    dataOut = false;
   }
}

void readPot(void){
  potValue = analogRead(pot);
  blendRecipe = (potValue*9)/1020;
  stringOne = "blendRecipe ";
  stringTwo = stringOne + blendRecipe;
}

void checkPreGrindButton(void){
  preGrindButtonState = digitalRead(preGrindButton);
  if (stateFlag == preGrind && preGrindButtonState == HIGH){
    stateFlag = blendSelected;
  }
  else if (stateFlag == readyToBrew && preGrindButtonState == HIGH){
    stateFlag = customerComplete;
    firstTimeHere = true;
  } 
  else if (stateFlag == customerComplete && preGrindButtonState == HIGH){
    stateFlag = reset;
    firstTimeHere = true;
  } 
}

void displayLatchesLow(void){
  digitalWrite(segmentLatchPin, LOW);
  digitalWrite(barLatchPin, LOW);
}

void populateLedArray(void){
  for (int i = 0; i < 10; i++) {  //for loop to read BlendTimeArray and convert to 0 or 1
    for (int j=0; j < 3; j++){
      if (blendTimeArray[i][j]!=0){
        ledArray[i][j]=1;
      }
    }
  }
}

void setGrinderState(void){
    for (int i = 0; i < 3; i++){
      if (grinderButtonState[i] != 0){
        grinderRequest = i;
      }
    }
    if (pulse >= pulseMax){
      requestFlag = requestDenied;
      stateFlag = orderComplete;
    }
    else if (blendSelectionArray[grinderRequest] == 0){
      requestFlag = requestDenied;
      stateFlag = grinderComplete;
    }
    else {
      requestFlag = requestAllowed;
    }
}


void updateDisplay(void) {

  if (stateFlag == preGrind){
    displayArray = blendRecipe;
    if (displayArray != previousDisplayArray){
      previousDisplayArray = displayArray;
      dataSEGMENT = dataArraySEGMENT[displayArray];
      displayLatchesLow();
      shiftOut(shiftDataPin, shiftClockPin, dataSEGMENT);   
      digitalWrite(segmentLatchPin, 1);
    }
  }

  if (stateFlag == blendSelected){
    displayLatchesLow();
    displayArray=0;
    n = 0;
    x = 0;
    while(x<3){
      while (n<9){
        if (displayArray < 8){
          displayArray += 1;
        }
        else {
          displayArray = 0;
        }

        delay(50);

        if (displayArray != previousDisplayArray){
          previousDisplayArray = displayArray;
          dataBAR = dataArrayBAR[displayArray];
          displayLatchesLow();
          shiftOut(shiftDataPin, shiftClockPin, dataBAR);   
          digitalWrite(barLatchPin, 1);
          n++;
        }
      }
      x++;
      n=0;
    }
  }

  if (stateFlag == idle){
        if (displayArray < 16){
          displayArray += 1;
        }
        else {
          displayArray = 11;
        }
    if (displayArray != previousDisplayArray){
      previousDisplayArray = displayArray;
      dataSEGMENT = dataArraySEGMENT[displayArray];
      displayLatchesLow();
      shiftOut(shiftDataPin, shiftClockPin, dataSEGMENT);   
      digitalWrite(segmentLatchPin, 1);
    }
  }
  
  if (stateFlag == customerComplete){
        if (displayArray < 9){
          displayArray += 1;
        }
        else {
          displayArray = 0;
        }
    if (displayArray != previousDisplayArray){
      previousDisplayArray = displayArray;
      dataSEGMENT = dataArraySEGMENT[displayArray];
      displayLatchesLow();
      shiftOut(shiftDataPin, shiftClockPin, dataSEGMENT);   
      digitalWrite(segmentLatchPin, 1);
    }
  }
  
  if (stateFlag == reset){
    displayLatchesLow();
    displayArray=0;
    n = 0;
    
    while (n<15){

      if (displayArray == 8){
        displayArray = 0;
      }

      else if (displayArray == 0){
        displayArray = 8;
      }

      delay(50);
      dataBAR = dataArrayBAR[displayArray];
      displayLatchesLow();
      shiftOut(shiftDataPin, shiftClockPin, dataBAR);   
      digitalWrite(barLatchPin, 1);
      n++;
    }
  } 

  if (stateFlag == readyToBrew){
    if (displayArray < 8){
      displayArray += 1;
    }

    else {
      displayArray = 0;
    }

    delay(150);

    if (displayArray != previousDisplayArray){
      previousDisplayArray = displayArray;
      dataBAR = dataArrayBAR[displayArray];
      displayLatchesLow();
      shiftOut(shiftDataPin, shiftClockPin, dataBAR);   
      digitalWrite(barLatchPin, 1);
    } 
  }

  delay(100);
  
  if (displayArray != previousDisplayArray){
    previousDisplayArray = displayArray;
    dataBAR = dataArrayBAR[displayArray];
    displayLatchesLow();
    shiftOut(shiftDataPin, shiftClockPin, dataBAR);   
    digitalWrite(barLatchPin, 1);
  } 
}

void shiftOut(int myDataPin, int myClockPin, byte myDataOut) {
  // This shifts 8 bits out MSB first, 
  //on the rising edge of the clock,
  //clock idles low

  //internal function setup
  int i=0;
  int pinState;
  pinMode(myClockPin, OUTPUT);
  pinMode(myDataPin, OUTPUT);

  //clear everything out just in case to
  //prepare shift register for bit shifting
  digitalWrite(myDataPin, 0);
  digitalWrite(myClockPin, 0);

  //for each bit in the byte myDataOut�
  //NOTICE THAT WE ARE COUNTING DOWN in our for loop
  //This means that %00000001 or "1" will go through such
  //that it will be pin Q0 that lights. 
  for (i=7; i>=0; i--)  {
    digitalWrite(myClockPin, 0);

    //if the value passed to myDataOut and a bitmask result 
    // true then... so if we are at i=6 and our value is
    // %11010100 it would the code compares it to %01000000 
    // and proceeds to set pinState to 1.
    if ( myDataOut & (1<<i) ) {
      pinState= 1;
    }
    else {    
      pinState= 0;
    }

    //Sets the pin to HIGH or LOW depending on pinState
    digitalWrite(myDataPin, pinState);
    //register shifts bits on upstroke of clock pin  
    digitalWrite(myClockPin, 1);
    //zero the data pin after shift to prevent bleed through
    digitalWrite(myDataPin, 0);
  }

  //stop shifting
  digitalWrite(myClockPin, 0);
}

void resetVariables(void){
  displayArray = 0;
  previousDisplayArray = -1;
  n=0;
  x=0;
  pulse=0;
  firstTimeHere = true;
    
  for (int x = 0; x < grinderButtonPinCount; x++)  {
    blendCustomArray[x]=0;   
    blendPercentage[x]=0;   
  }
}
