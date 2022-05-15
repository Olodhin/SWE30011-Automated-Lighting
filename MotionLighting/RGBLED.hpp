#pragma once

/**
 *  Name: RGBLED
 * 
 *  Description: 
 *      An RGB LED class.
 *      
 *  Methods:
 *      Constructor takes in pin numbers.
 *      
 *      Requires explicit setup() for pinmode.
 *   
 *      trimVal(val) ensures val is between 
 *          RGB_MIN and RGB_MAX
 *          
 *      setColor(r, g, b) allows for RGB  values
 *          to be customised.
 *          
 *      on() and off() turn the LEDs on or off.
 */
class RGBLED
{
    private:
        const int RGB_MIN = 0;
        const int RGB_MAX = 255;
  
        int rPin;
        int gPin;
        int bPin; 
        bool initDone;

        // RGB values, 255 max
        int r;
        int g;
        int b;

        // ensure RGB min and max bounds
        int trimVal(int val)
        {
            if (val > RGB_MAX)
            {
                val = RGB_MAX;
            }
    
            if (val < RGB_MIN)
            {
                val = RGB_MIN;
            }

            return val;
        }

    public:
        RGBLED(int rPin, int gPin, int bPin) : 
            rPin(rPin), gPin(gPin), bPin(bPin)
        {
            // default color = WHITE
            r = 255;
            g = 255;
            b = 255;

            initDone = false;
        }

        void setup()
        {
            pinMode(rPin, OUTPUT);
            pinMode(gPin, OUTPUT);
            pinMode(bPin, OUTPUT);
        }

        void setColor(int rVal, int gVal, int bVal)
        {
            r = trimVal(rVal);
            g = trimVal(gVal);
            b = trimVal(bVal);
        }

        void on()
        {
            analogWrite(rPin, r);
            analogWrite(gPin, g);
            analogWrite(bPin, b);
        }

        void off()
        {
            analogWrite(rPin, 0);
            analogWrite(gPin, 0);
            analogWrite(bPin, 0);
        }

        String getColor()
        {
            return String(r) + ":" + String(g) + ":" + String(b);
        }
};
