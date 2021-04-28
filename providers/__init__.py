from providers.basetype import ProviderBaseType
from providers.redrock import RedrockProvider
from providers.wecqupt import WeCQUPTProvider
from providers.jwzxdirect import JWZXDirectProvider

providers: "dict[str, ProviderBaseType]"
providers = {
	"redrock": RedrockProvider,
	"wecqupt": WeCQUPTProvider,
	"jwzxdirect": JWZXDirectProvider
}