#ifndef _SEEDKEY_H_
#define _SEEDKEY_H_
#ifndef DllImport
#define DllImport __declspec(dllimport)
#endif
#ifndef DllExport
#define DllExport __declspec(dllexport)
#endif
#ifdef SEEDKEYAPI_IMPL
#define SEEDKEYAPI DllExport __cdecl
#else
#define SEEDKEYAPI DllImport __cdecl
#endif
#ifdef __cplusplus
extern "C" {
#endif
    BOOL SEEDKEYAPI KWP2000_ComputeKeyFromSeed(	unsigned char Mode, BYTE *seed, unsigned short sizeSeed,
            BYTE *key, unsigned short maxSizeKey, unsigned short *sizeKey);
#ifdef __cplusplus
}
#endif
#endif

