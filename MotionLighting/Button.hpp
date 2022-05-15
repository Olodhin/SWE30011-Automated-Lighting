#pragma once

#include "defines.hpp"

/**
 *  class: Button
 *  
 *  Description:
 *      Abstraction of an active HIGH button.
 *      
 *      Used DEBOUNCE_DELAY from defines.hpp
 *  
 *  Methods:
 *      Constructor takes in integer corresponding to
 *          pin number of the button on the Arduino.
 *          
 *      Requires an explicit setup().
 *      
 *      getButtonState() debounces button and returns
 *          debounced result. Returns -1 if uninitialised.
 */
class Button
{
    private: 
        bool initDone;
    
        int pin;
        int state;      // debounce state
        int lastState;  // last actual read state
        unsigned long lastDebounceTime;
        
    public:
        Button(int pinNum)
        {
            initDone = false;
            
            pin = pinNum;
            state = LOW;
            lastState = LOW;
            lastDebounceTime = 0;
        }

        // explicit pint setup for button
        void setup()
        {
            pinMode(pin, INPUT);
            initDone = true;
        }

        // retrieve debounced button state
        int getButtonState()
        {
            int ret = -1;
            
            if (initDone)
            {
                ret = LOW;
                
                int currentState = digitalRead(pin);
                //Serial.println(currentState);
                if (currentState != lastState)
                {
                    lastDebounceTime = millis();
                }

                unsigned long deltaT = millis() - lastDebounceTime;
                if (deltaT > DEBOUNCE_DELAY)
                {
                    if (currentState != state)
                    {
                        state = currentState;
                        if (state == HIGH)
                        {
                            ret = HIGH;
                        }
                    }
                }

                lastState = currentState;
            }

            return ret;
        }
};
