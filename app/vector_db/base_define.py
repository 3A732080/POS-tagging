import weaviate

# 單例模式：確保整個應用中僅存在一個實例（weaviate.Client），並且提供一個全域訪問點來訪問該實例
class WeaviateClientSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs): # 檢查類別層級的 _instance 屬性是否已經被賦值
        if not cls._instance:
            cls._instance = super(WeaviateClientSingleton, cls).__new__(cls)
            # 初始化 weaviate.Client
            cls._instance.client = weaviate.Client(*args, **kwargs)

            # 檢查連接是否成功
            if cls._instance.client.is_ready():
                print("成功連接到 Weaviate!")
            else:
                print("連接到 Weaviate 失敗。")

        return cls._instance

    def __getattr__(self, name):
        # 代理調用被封裝的 weaviate.Client 實例中相應的屬性或方法
        return getattr(self._instance.client, name)

    def __setattr__(self, name, value):
        if name == "client":
            # 允許對 _client 屬性進行初始化賦值
            return super(WeaviateClientSingleton, self).__setattr__(name, value)

        # 代理所有屬性設置到 weaviate.Client 實例
        return setattr(self._instance.client, name, value)