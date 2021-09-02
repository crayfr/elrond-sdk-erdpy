class SmartContractViewModel:
    def __init__(self, project) -> None:
        self.FriendlyId = None  # this.FriendlyId = this.SourceFile.PathRelativeToWorkspace;
        self.SourceFile = MyFileViewModel()
        self.BytecodeFile = MyFileViewModel()
        self.PropertiesOnNodeDebug = PropertiesOnNetworkViewModel()
        self.PropertiesOnTestnet = PropertiesOnNetworkViewModel()
        self.IsBuilt = self.BytecodeFile is not None


class MyFileViewModel:
    def __init__(self) -> None:
        self.PathRelativeToWorkspace = None


class PropertiesOnNetworkViewModel:
    def __init__(self) -> None:
        self.Address = None
        self.AddressTimestamp = None
        self.LatestRun = SmartContractRunViewModel()
        self.WatchedVariables = []
        self.WatchedVariablesValues = dict()


class SmartContractRunViewModel:
    def __init__(self) -> None:
        self.Options = {
            "senderAddress": "",
            "functionName": "your_function",
            "functionArgs": [],
            "value": 0,
            "gasLimit": 500000000,
            "gasPrice": 200000000000000
        }

        self.VMOutput = dict()


class WatchedVariableViewModel:
    def __init__(self) -> None:
        self.Name = None
        self.FunctionName = None
        self.Arguments = None
