#include "RGBLED.hpp"
#include "PIR.hpp"
#include "MotionSM.hpp"
#include "MotionCommand.hpp"
#include "defines.hpp"
#include "Button.hpp"

PIR pir(PIR_PIN);
RGBLED led(R_PIN, G_PIN, B_PIN);
Button btn(BTN_PIN);
MotionSM sm(led);
MotionCommand mc(led);

unsigned long lastSerialTime = 0;

int lastPirState;
int lastBtnState;

void setup()
{
    lastPirState = LOW;
    lastBtnState = LOW;
    
    pir.setup();
    btn.setup();

    Serial.begin(9600);
    Serial.println();
}
void loop()
{
    int pirState = pir.isDetected();
    int btnState = btn.getButtonState();
  
    sm.nextStateLogic(btnState, pirState);
    sm.stateActions();

    bool btnChanged = (btnState != lastBtnState);
    bool pirChanged = (pirState != lastPirState);
    bool cmdFound = false;
    
    if (Serial.available() > 0)
    {
        String cmd = Serial.readString();
        cmdFound = mc.processCmd(cmd);
        Serial.flush();
    }

    if (allowSerialWrite(lastSerialTime, btnChanged, pirChanged, cmdFound))
    {
        lastSerialTime = millis();
        String state = sm.getState();
        String pirOutput = IOString(pirState);
        String color = led.getColor();
        Serial.println("state:" + state + ";pirOutput:" + pirOutput + ";color:" + color);
    }

    lastPirState = pirState;
    lastBtnState = btnState;
}

bool allowSerialWrite(unsigned long lastTime, bool btnChanged, bool pirChanged, bool cmdFound)
{
    unsigned long currentTime = millis();
    bool serialDelayElapsed = (currentTime - lastTime > SERIAL_DELAY);

    return serialDelayElapsed || btnChanged || pirChanged || cmdFound;
}

String IOString(int ioElement)
{
    return (ioElement == HIGH) ? "HIGH" : "LOW";
}
