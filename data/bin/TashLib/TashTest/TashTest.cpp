// TashTest.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"

#import "TashLib.tlb" no_namespace named_guids


int _tmain(int argc, _TCHAR* argv[])
{
	CoInitialize(NULL);

	{
		BSTR sHello = SysAllocString(L"\xcc\x90\x90\xc3");

		ITashLoaderPtr pTashLoader(__uuidof(TashLoader));

		pTashLoader->Load(sHello, (BSTR)NULL, 0);

		SysFreeString(sHello);
	}

	CoUninitialize();

	return 0;
}

