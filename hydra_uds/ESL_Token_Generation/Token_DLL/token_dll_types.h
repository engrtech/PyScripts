#ifndef TOKEN_DEF_H
#define TOKEN_DEF_H

//#include <stdint.h>

#ifndef U8
#define U8 unsigned char
#endif

typedef struct
{
    U8 token_ver;
    U8 key_ver;
    U8 ecu_serial[20];
    U8 freshness_value[5];
    U8 entitlement[2];
    U8 requester_id[8];
    U8 manufacturer_reserved[187];
    U8 manufacturer_challenge[16];
    U8 authentication_data[16];
}
PHSM_ESL_TOKEN_T;

#define PSEC_ESL_TOKEN_CHALLENGE_SIZE    (16U)
#define PSEC_ESL_TOKEN_SIZE              sizeof(PHSM_ESL_TOKEN_T)
#define PSEC_ESL_TOKEN_SIGNED_SIZE       (240U)
#define PSEC_UDS_ESL_SECLVL              (0x61U)

#endif