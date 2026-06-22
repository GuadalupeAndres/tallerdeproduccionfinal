int ENB = 5; //violeta
int IN3 = 7; //marrón
int IN4 = 6; //blanco

void setup() {
  Serial.begin(9600);
  pinMode (ENB, OUTPUT);
  pinMode (IN3, OUTPUT);
  pinMode (IN4, OUTPUT);

}

void Adelante () {
 digitalWrite (IN3, HIGH);
 digitalWrite (IN4, LOW);
 analogWrite (ENB, 255); //Velocidad 

}

void Atras () {
  digitalWrite (IN3, LOW);
 digitalWrite (IN4, HIGH);
 analogWrite (ENB, 255); //Velocidad 
}

void Frenar () {
  digitalWrite (IN3, LOW);
 digitalWrite (IN4, LOW);
 analogWrite (ENB, 0); 
}

void loop() {
  if(Serial.available() > 0) {
    int posX = Serial.parseInt();

    if (posX > 0){

      if (posX >= 320 ){
        Serial.print("adelante");
        Adelante ();
        //delay(500);
        //Frenar();
      } else {
        Serial.print("atrás");
        Atras ();
        //delay(500);
        //Frenar();

      }

      Serial.print("Valor recibido: ");
      Serial.print(posX);
    }
    
  } else {
    Frenar();
  }

}
