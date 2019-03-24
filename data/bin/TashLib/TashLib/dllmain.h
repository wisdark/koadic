// dllmain.h : Declaration of module class.

class CTashLibModule : public CAtlDllModuleT< CTashLibModule >
{
public :
	DECLARE_LIBID(LIBID_TashLibLib)
	DECLARE_REGISTRY_APPID_RESOURCEID(IDR_TASHLIB, "{C02068B5-64F3-4BE7-8D5A-B3A270605C76}")
};

extern class CTashLibModule _AtlModule;
