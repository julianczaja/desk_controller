#include <Arduino.h>
#include "AiEsp32RotaryEncoder.h"

#define ROTARY_ENCODER_A_PIN D6
#define ROTARY_ENCODER_B_PIN D5
#define ROTARY_ENCODER_BUTTON_PIN D7
#define ROTARY_ENCODER_VCC_PIN -1
#define ROTARY_ENCODER_STEPS 4

#define MODE_1_PIN D1
#define MODE_2_PIN D2

void on_button_clicked();
void IRAM_ATTR readEncoderISR();

uint8_t mode = 1;
int mode1value = 0;
int mode2value = 0;

AiEsp32RotaryEncoder rotaryEncoder = AiEsp32RotaryEncoder(
    ROTARY_ENCODER_A_PIN,
    ROTARY_ENCODER_B_PIN,
    ROTARY_ENCODER_BUTTON_PIN,
    ROTARY_ENCODER_VCC_PIN,
    ROTARY_ENCODER_STEPS);

void write_frame(int d1, int d2)
{
  Serial.printf("[%d,%d]", d1, d2);
}

void setup()
{
  Serial.begin(115200);
  Serial.flush();
  // Serial.println("Hello world");

  pinMode(MODE_1_PIN, OUTPUT);
  pinMode(MODE_2_PIN, OUTPUT);

  rotaryEncoder.begin();
  rotaryEncoder.setup(readEncoderISR);
  rotaryEncoder.setBoundaries(-99999, 99999, false);
  rotaryEncoder.setAcceleration(50);
  rotaryEncoder.setEncoderValue(0);
}

void loop()
{
  if (rotaryEncoder.encoderChanged())
  {
    int currentEncoderReading = rotaryEncoder.readEncoder();
    if (mode == 1)
    {
      write_frame(currentEncoderReading - mode1value, 0);
      mode1value = currentEncoderReading;
    }
    else
    {
      write_frame(0, currentEncoderReading - mode2value);
      mode2value = currentEncoderReading;
    }
  }

  if (rotaryEncoder.isEncoderButtonClicked())
  {
    on_button_clicked();
  }
}

void on_button_clicked()
{
  static unsigned long lastTimePressed = 0;

  if (millis() - lastTimePressed < 200)
    return;

  lastTimePressed = millis();

  if (mode == 1)
  {
    mode = 2;
    mode1value = rotaryEncoder.readEncoder();
    rotaryEncoder.setEncoderValue(mode2value);
    digitalWrite(MODE_1_PIN, HIGH);
    digitalWrite(MODE_2_PIN, LOW);
  }
  else
  {
    mode = 1;
    mode2value = rotaryEncoder.readEncoder();
    rotaryEncoder.setEncoderValue(mode1value);
    digitalWrite(MODE_1_PIN, LOW);
    digitalWrite(MODE_2_PIN, HIGH);
  }
}

void IRAM_ATTR readEncoderISR()
{
  rotaryEncoder.readEncoder_ISR();
}
