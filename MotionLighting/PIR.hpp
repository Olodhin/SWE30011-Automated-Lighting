#pragma once

/**
 *  Name: PIR
 * 
 *  Description:
 *      Wrapper for ElectroPeak HC-SR501 PIR sensor
 *      
 *  Methods:
 *      Constructor takes in pin number for PIR output.
 *      
 *      detect() reads from current PIR output.
 *      
 *      Requires explicit setup() for pinmode.
 *      
 *      isDetected() returns if the PIR detects anything.
 */
class PIR
{
    private:
        int detected;
        int pinNum;
        bool initDone;

        // check if PIR is detected
        void detect()
        {
            int det = LOW;

            if (initDone)
            {
                det = digitalRead(pinNum);
            }

            detected = det;
        }
    
    public:
        PIR(int pin)
        {
            detected = LOW;
            pinNum = pin;
            initDone = false;
        }

        // perform pinmode setup
        void setup()
        {
            pinMode(pinNum, INPUT);
            initDone = true;
        }

        // Check if PIR has detected motion
        int isDetected()
        {
            detect();
      
            int ret = detected;
            if (!initDone)
            {
                ret = -1;
            }

            return ret;
        }
};
