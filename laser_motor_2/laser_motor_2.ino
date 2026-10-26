#include "Adafruit_VL53L0X.h"

Adafruit_VL53L0X lox = Adafruit_VL53L0X();

int ENB = 5;  //violeta
int IN3 = 7;  //marrón
int IN4 = 6;  //blanco

int analog = A0;  //violeta - verde - naranja
int valX = 0;
int posX = 0;  //variable de la posición
int medicion = 0; //valor de lo que se detecta

void setup() {
  Serial.begin(9600);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  //analogWrite(ENB, 255);
  
  // wait until serial port opens for native USB devices
  while (!Serial) {
    delay(1);
  }

  Serial.println("Adafruit VL53L0X test.");
  Serial.println("Ejemplo modificado by BEEGGLE");
  if (!lox.begin()) {
    Serial.println(F("Failed to boot VL53L0X"));
    while (1);
  }
  // power
  Serial.println(F("VL53L0X API Continuous Ranging example\n\n"));


  // start continuous ranging
  lox.startRangeContinuous();
}

void Adelante() {
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENB, 240);  //Velocidad
  //delay(20);
  //analogWrite(ENB, 220);

}

void Atras() {
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENB, 240);  //Velocidad
  //delay(20);
  //analogWrite(ENB, 220);
}

void Frenar() {
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENB, 0);
}

void Detectar() {
  if (lox.isRangeComplete()) {

    //Serial.println(lox.readRange());
    medicion = lox.readRange() - 25;

    Serial.print("Distancia en mm: ");
    Serial.println(medicion);
    //delay(200);
  }
}

void Validar(){

  Detectar();
  delay(200);

  if(medicion > 30 && medicion < 350) {
      //posX = medicion;
      int mem1 = medicion;


      Detectar();
      delay(200);

      if((mem1 <= medicion + 5)&(mem1 >= medicion - 5)){

         Detectar();
         delay(200);

        int mem2 = medicion;

        if((mem2 <= medicion + 5)&(mem2 >= medicion - 5)){

          posX = medicion;

          posX = map(posX, 50, 350, 2, 10);

        } else {
          posX = 0;
        }

      }

      
  } else {
    posX = 0; // fuera de rango
  }

}

void loop() {

  valX = analogRead(analog);  //potenciómetro

  valX = map(valX, 0, 1023, 1, 10);
  //delay(100);

  //Serial.println("Valor leido");
  //Serial.println(valX);

  Validar();

  Serial.print("Valor recibido: ");
    Serial.print(posX);



  if (posX > 0) {

    if (posX > valX + 1) {
      Serial.print("adelante");
      Adelante();
      //delay(500);
      //Frenar();
    } else if (posX < valX - 1) {
      Serial.print("atrás");
      Atras();
      //delay(500);
      //Frenar();
    } else if (posX == valX) {
      Frenar();
    }

    Serial.print("Valor recibido: ");
    Serial.print(posX);


  } else {
    Frenar();
  }
}
