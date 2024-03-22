#include <Windows.h>
#include <stdlib.h>
#include <stdio.h>

#define SEEDKEYAPI_IMPL
#include "token_dll.h"
#include "token_dll_types.h"
#include "string.h"
#include "aes_cmac_rfc/TI_aes_128.h"
#include "aes_cmac_rfc/aes-cbc-cmac.h"

#ifdef __cplusplus
extern "C" {
#endif

BOOL SEEDKEYAPI KWP2000_ComputeKeyFromSeed
(
	unsigned char Mode,
    BYTE *seed, 
    unsigned short sizeSeed,
    BYTE *key, 
    unsigned short maxSizeKey, 
    unsigned short *sizeKey
)
{
    BOOL rc = TRUE;
    
    PHSM_ESL_TOKEN_T *token_ptr = (PHSM_ESL_TOKEN_T *)key;
    
    int i;

#ifdef DEBUG
    FILE* debug_file =  fopen("c:\\temp\\dll_debug.txt","w");
    
    fprintf(debug_file, "Processing seed/key request\n");
    fprintf(debug_file, "Mode: %d\n", Mode);
    fprintf(debug_file, "Seed length: %d\n", sizeSeed);
    for (i = 0; i < sizeSeed; i++)
    {
       fprintf(debug_file, "%x ", seed[i]);
    }
    fprintf(debug_file, "\n");
    fprintf(debug_file, "Max Key: %d\n", maxSizeKey);
#endif


    /* Check input parameters */
    if (   (NULL == seed)
        || (NULL == token_ptr))
    {
       rc = FALSE;
#ifdef DEBUG
       fprintf(debug_file, "Null pointer error in seed/key response generation!\n");
#endif
    }
    /* Correct security level for token */
    else if (Mode != PSEC_UDS_ESL_SECLVL)
    {
       rc = FALSE;
#ifdef DEBUG
       fprintf(debug_file, "Security level doesn't match, expected %d, got %d\n", PSEC_UDS_ESL_SECLVL, Mode);
#endif
    }
    /* Correct number of seed bytes */
    else if (sizeSeed > PSEC_ESL_TOKEN_CHALLENGE_SIZE)
    {
       rc = FALSE;
#ifdef DEBUG
       fprintf(debug_file, "Cannot generate seed/key response. Expected %d bytes of seed data, received %d\n", PSEC_ESL_TOKEN_CHALLENGE_SIZE, sizeSeed); 
#endif
    }
    /* Enough space for the response */
    else if (maxSizeKey < PSEC_ESL_TOKEN_SIZE)
    {
       rc = FALSE;
#ifdef DEBUG
       fprintf(debug_file, "Cannot generate seed/key response. %d bytes of data buffer are required and the tool only provided %d\n", PSEC_ESL_TOKEN_SIZE, maxSizeKey); 
#endif
    }
    else
    {
        const U8 entitlement[2]   = {0x00, 0x65};

        const U8 token_signing_key[BLOCK_SIZE] = {0x00, 0x11, 0x22, 0x33,
                                                  0x44, 0x55, 0x66, 0x77,
                                                  0x88, 0x99, 0xAA, 0xBB,
                                                  0xCC, 0xDD, 0xEE, 0xFF};

        const U8 ecu_serial[20]   = {0x00, 0x00, 0x00, 0x00, 0x00,
                                     0x00, 0x00, 0x00, 0x00, 0x00,
                                     0x00, 0x00, 0x00, 0x00, 0xFF,
                                     0xFF, 0xFF, 0xFF, 0xFF, 0xFF};

        const U8 token_ver = 0;
        const U8 key_ver   = 0;
        const U8 requester_id[8] = "PiSnoop";

        /* First populate the seed regions of the token */
        //memcpy(token_ptr->manufacturer_challenge, seed, PSEC_ESL_TOKEN_CHALLENGE_SIZE);
        memset(token_ptr->manufacturer_challenge, 0x00u, PSEC_ESL_TOKEN_CHALLENGE_SIZE);
        
        /* Populate the freshness value. It's just the UTC date in:
        ** { year, month, day, hour, minute } */
        {
            SYSTEMTIME system_time;
            GetSystemTime(&system_time);
            
            system_time.wYear = 2022u; 
            system_time.wMonth = 10u;
            system_time.wDay = 04;
            system_time.wHour = 10;
            system_time.wMinute = 10;
            
            /* 2 digit year starting in y2k. If anyone in 2256 is still using this, 
            ** sorry but you really should have upgraded by now */
            token_ptr->freshness_value[0] = system_time.wYear - 2000U; 
            token_ptr->freshness_value[1] = system_time.wMonth;
            token_ptr->freshness_value[2] = system_time.wDay;
            token_ptr->freshness_value[3] = system_time.wHour;
            token_ptr->freshness_value[4] = system_time.wMinute;
        }
        
        /* Populate other fields - todo, figure out how to get these from the client */
        token_ptr->token_ver = token_ver;
        token_ptr->key_ver   = key_ver;
        memcpy(token_ptr->ecu_serial,   ecu_serial,   sizeof(ecu_serial));
        memcpy(token_ptr->entitlement,  entitlement,  sizeof(entitlement));
        memcpy(token_ptr->requester_id, requester_id, sizeof(requester_id));

        /* Generate the CMAC signature of the newly minted token. This step MUST occur last */
        AES_CMAC(token_signing_key, (U8*)token_ptr, PSEC_ESL_TOKEN_SIGNED_SIZE, token_ptr->authentication_data);
        
        *sizeKey = sizeof(PHSM_ESL_TOKEN_T);
    }
#ifdef DEBUG
    fclose(debug_file);
#endif

    return rc;
}
    
#ifdef __cplusplus
}
#endif
