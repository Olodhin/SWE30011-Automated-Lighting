#pragma once

#include "RGBLED.hpp"

/**
 *  Name: MotionCommand
 * 
 *  Description:
 *      Parses commands in the form:
 *          'r:111,g:111,b:111' (in no particular order)
 */
class MotionCommand
{
    private:
        RGBLED& led;
    
        int getRGBVal(char rgb, String cmd)
        {
            
        }

        void constructPairs(String cmd, char delim, int& pairCount, String* pairs)
        {           
            // construct pairs e.g. 'r:111', 'g:111'
            String tmp = "";
            int len = cmd.length() - 1; // remove newline
            for(int i = 0; i < len; i++)
            {
                char tmpChar = cmd[i];
                Serial.println("L: " + String(tmpChar) + ", " + String(int(tmpChar)));
                
                if (tmpChar == delim || i == len - 1)
                {
                    if (i == len - 1)
                    {
                        tmp += String(tmpChar);
                    }
                    pairs[pairCount++] = tmp;
                    Serial.println("BREAK - " + String(pairs[pairCount-1]));
                    tmp = "";
                }
                else
                {
                    tmp += String(tmpChar);
                }
//                if (tmpChar != delim || tmpChar == '\n')
//                {
//                    pairs[pairCount++] = tmp;
//                    Serial.println("new: " + tmp);
//                    tmp = "";
//                }
//                else
//                {
//                    tmp += String(tmpChar);
//                    Serial.println("tmpt: " + tmp);
//                }
            }

            //Serial.flush();

            return;
        }
    
    public:
        MotionCommand(RGBLED& led) : led(led)
        {}

        // example cmd: r:1,g:2,b:3
        bool processCmd(String cmd)
        {
            char delim = ',';
            int r = 0, g = 0, b = 0;
            int pairCount = 0;
            int len = cmd.length() - 1; // remove newline char
            String pairs[3];

            int delimCount = 0;
            int rIdx = -1, gIdx = -1, bIdx = -1;
            for(int i = 0; i < len; i++)
            {
                char tmp = cmd[i];
                if (tmp ==  delim)
                    delimCount++;
                else
                {
                    switch(tmp)
                    {
                        case 'r':
                            rIdx = i;
                            break;
                        case 'b':
                            bIdx = i;
                            break;
                        case 'g':
                            gIdx = i;
                            break;
                    }
                }
            }

            if (delimCount == 2 && rIdx != -1 && gIdx != -1 && bIdx != -1)
            {
//                Serial.println(rIdx);
//                Serial.println(gIdx);
//                Serial.println(bIdx);
                String rStr = "", gStr = "", bStr = "";
                for(int i = rIdx + 2; i < gIdx - 1; i++)
                {
//                    Serial.println(String(cmd[i]));
                    rStr += String(cmd[i]);
                }

                for(int i = gIdx + 2; i < bIdx - 1; i++)
                {
                    gStr += String(cmd[i]);
                }

                for(int i = bIdx + 2; i < cmd.length(); i++)
                {
                    bStr += String(cmd[i]);
                }

//                Serial.println(rStr);
//                Serial.println(gStr);
//                Serial.println(bStr);

                int r, g, b;
                r = rStr.toInt();
                g = gStr.toInt();
                b = bStr.toInt();

                led.setColor(r, g, b);
            }
            
            return true;
        }
};
