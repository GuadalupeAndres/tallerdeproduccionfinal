int LED = 13;

void setup() {
  Serial.begin(9600);
  pinMode(LED, OUTPUT);

}

void loop() {
  if(Serial.available() > 0) {
    int posX = Serial.parseInt();

    if (posX > 0){

      if (posX >= 320 ){
        Serial.print("adelante");
        digitalWrite(LED, HIGH);
      } else {
        Serial.print("atrás");
        digitalWrite(LED, LOW);
      }

      Serial.print("Valor recibido: ");
      Serial.print(posX);
    }
  }

}
