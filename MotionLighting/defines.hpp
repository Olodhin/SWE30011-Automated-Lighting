#define PIR_PIN 2
#define R_PIN 3
#define G_PIN 5
#define B_PIN 6
#define BTN_PIN 7

#define DELAY_TIME 1000
#define MD_ON_TIME 10000
#define DEBOUNCE_DELAY 50
#define SERIAL_DELAY 1000

#define FOREACH_MDSTATE(MDSTATE) \
        MDSTATE(OFF)      \
        MDSTATE(ON_IDLE)  \
        MDSTATE(ON_DET)   //\
//        MDSTATE(CUSTOM) 

#define GENERATE_ENUM(ENUM) ENUM,
#define GENERATE_STRING(STRING) #STRING,
