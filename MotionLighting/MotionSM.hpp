#pragma once

#include "defines.hpp"
#include "PIR.hpp"
#include "RGBLED.hpp"

/** 
 *  Name: MDState
 *  
 *  Description:
 *      States for Motion Detector State Machine
 *      
 *      Uses FOREACH_MDSTATE and GENERATE_ENUM
 *          from defines.hpp
 */
enum MDState
{
    FOREACH_MDSTATE(GENERATE_ENUM)
};

/** 
 *  Name: MDStateString
 *  
 *  Description:
 *  Uses pre-processor magic to get state
 *          strings for each state in MDState.
 *      
 *      Uses FOREACH_MDSTATE and GENERATE_STRING
 *          from defines.hpp
 */
static const char* MDStateString[] = 
{
    FOREACH_MDSTATE(GENERATE_STRING)
};

/**
 *  Name: MotionSM
 *  
 *  Description:
 *      The state machine for the motion detector.
 *      
 *      States:
 *          OFF
 *              LEDs are off. No response to PIR input.
 *          ON_IDLE
 *              LEDs are off. Waits for PIR to go HIGH.
 *          ON_DET
 *              LEDs are on. Waits for PIR to go LOW.
 *          CUSTOM
 *              LEDs are on. Uses cmd parameter to 
 *                  select color.
 *                  
 *  Methods:
 *      Constructor requires an LED (for output)
 *      
 *      Requires explicit setup()
 *      
 *      nextStateLogic() takes in inputs (btn, detection, cmd)
 *          and decides the next state.
 *          
 *      stateActions() processes LED output for current state.
 *      
 *      printState() prints the current state to serial.
 */
class MotionSM
{
    private:
        MDState currentState;
        
        RGBLED& led;

        double timer;       // perhaps unneeded

    public:
        MotionSM(RGBLED& led) : led(led)
        {
            currentState = MDState::OFF;
        }

        // determine the next state based on inputs
        void nextStateLogic(int btn, int detection)
        {
            MDState nextState = currentState;

            switch(currentState)
            {
                case MDState::OFF:
                {
                    if (btn == HIGH)
                    {
                        nextState = MDState::ON_IDLE;
                    }

                    break;
                }
                case MDState::ON_IDLE:
                {
                    if (btn == HIGH)
                    {
                      nextState = MDState::OFF;
                    }
                    else if (detection == HIGH)
                    {
                      nextState = MDState::ON_DET;
                      timer = millis();
                    }
                
                    break;
                }
                case MDState::ON_DET:
                {
                    double deltaT = millis() - timer;
                    if (btn == HIGH)
                    {
                        nextState = MDState::OFF;
                    }
//                    else if (cmd != 0)
//                    {
//                        nextState = MDState::CUSTOM;
//                    }
                    else if (deltaT > MD_ON_TIME)
                    {
                        nextState = MDState::ON_IDLE;
                    }

                    // reset timer whenever movement detected.
                    if (detection == HIGH)
                    {
                        timer = millis();
                    }
                
                    break;
                }
//                case MDState::CUSTOM:
//                {
//                    if (btn == HIGH)
//                    {
//                        nextState = MDState::OFF;
//                    }
//                
//                    break;
//                }
                default:
                {
                    break;
                }
            }

            currentState = nextState;
        }

        // process state actions
        void stateActions()
        {
            switch(currentState)
            {
                case MDState::OFF:
                case MDState::ON_IDLE:
                {
                    led.off();
                    break;
                }
                case MDState::ON_DET:
//                case MDState::CUSTOM:
                {
                    led.on();
                    break;
                }
            }
        }

        // print current state to serial
        void printState()
        {
            Serial.println("State:");
            Serial.println(getState());
        }

        String getState()
        {
            return MDStateString[currentState];
        }
};
