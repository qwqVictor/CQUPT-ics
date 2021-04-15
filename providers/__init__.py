from providers.basetype import ProviderBaseType
from providers.redrock import RedrockProvider
from providers.wecqupt import WeCQUPTProvider

providers: "dict[str, ProviderBaseType]"
providers = {
	"redrock": RedrockProvider,
	"wecqupt": WeCQUPTProvider
}