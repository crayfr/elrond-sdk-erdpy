from erdpy.accounts import Account, Address
import logging
import traceback
from typing import Any, Callable, List, Tuple

from erdpy import errors
from erdpy.contracts import SmartContract
from erdpy.proxy import ElrondProxy

logger = logging.getLogger("environments")


class Environment:
    def __init__(self) -> None:
        pass

    def run_flow(self):
        raise NotImplementedError()

    def deploy_contract(self, contract: SmartContract, owner: Account, arguments: List[Any], gas_price: int, gas_limit: int, value: int, chain: str, version: int) -> Tuple[str, Address]:
        raise NotImplementedError()

    def execute_contract(self, contract: SmartContract, caller: Account, function: str, arguments: List[str], gas_price: int, gas_limit: int, value: int, chain: str, version: int) -> str:
        raise NotImplementedError()

    def query_contract(self, contract, function, arguments=None):
        raise NotImplementedError()


class TestnetEnvironment(Environment):
    def __init__(self, url) -> None:
        super().__init__()
        self.url = url

    def run_flow(self, flow: Callable) -> Any:
        return self._wrap_flow(flow)

    def _wrap_flow(self, flow: Callable) -> Any:
        try:
            logger.debug("Starting flow...")
            result = flow()
            logger.debug("Flow ran.")
            return result
        except errors.KnownError as err:
            logger.critical(err)
        except Exception:
            print(traceback.format_exc())

    def deploy_contract(self, contract: SmartContract, owner: Account, arguments: List[Any], gas_price: int, gas_limit: int, value: int, chain: str, version: int) -> Tuple[str, Address]:
        logger.debug("deploy_contract")
        tx = contract.deploy(owner, arguments, gas_price, gas_limit, value, chain, version)
        proxy = self._get_proxy()
        tx_hash = tx.send(proxy)
        return tx_hash, contract.address

    def execute_contract(self, contract: SmartContract, caller: Account, function: str, arguments: List[str], gas_price: int, gas_limit: int, value: int, chain: str, version: int) -> str:
        logger.debug("execute_contract: %s", contract.address.bech32())
        tx = contract.execute(caller, function, arguments, gas_price, gas_limit, value, chain, version)
        proxy = self._get_proxy()
        tx_hash = tx.send(proxy)
        return tx_hash

    def upgrade_contract(self, contract: SmartContract, caller, arguments, gas_price, gas_limit, value, chain, version) -> str:
        logger.debug("upgrade_contract: %s", contract.address.bech32())
        tx = contract.upgrade(caller, arguments, gas_price, gas_limit, value, chain, version)
        proxy = self._get_proxy()
        tx_hash = tx.send(proxy)
        return tx_hash

    def query_contract(self, contract: SmartContract, function, arguments=None) -> List[Any]:
        logger.debug("query_contract: %s", contract.address.bech32())
        proxy = self._get_proxy()
        return_data = contract.query(proxy, function, arguments)
        return return_data

    def _get_proxy(self) -> ElrondProxy:
        return ElrondProxy(self.url)
