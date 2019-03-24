// dllmain.cpp : Implementation of DllMain.

#include "stdafx.h"
#include "resource.h"
#include "TashLib_i.h"
#include "dllmain.h"

CTashLibModule _AtlModule;

// DLL Entry Point
extern "C" BOOL WINAPI DllMain(HINSTANCE hInstance, DWORD dwReason, LPVOID lpReserved)
{
	hInstance;
	MessageBoxW(NULL, L"The TashLib COM DLL is loaded", L"TashLib loaded!", MB_OK);
	return _AtlModule.DllMain(dwReason, lpReserved); 
}
