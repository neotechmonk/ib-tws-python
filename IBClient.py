from datetime import datetime, timedelta

from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper


class IBClient(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.historicalDataReceived = False
    
    def historicalTicksLast(self, reqId, ticks, done):
        for tick in ticks:
            print(f"Tick data: {tick.time} - {tick.price}")
        
        if done:
            self.historicalDataReceived = True
            print("Historical data request completed.")
            self.disconnect()


def main():
    client = IBClient()
    
    # Connect to the IB TWS (Trader Workstation) or Gateway
    client.connect("127.0.0.1", 7496, 0)  # Modify host and port as per your setup
    
    # Wait until the connection is established
    while not client.isConnected():
        pass
    
    print("Connection established.")
    
    # Define the contract details for the stock
    contract = Contract()
    contract.symbol = "MSFT"  # Replace with the desired stock symbol
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    
    # Calculate the start date for the historical data request
    end_date = datetime.now().strftime("%Y%m%d %H:%M:%S")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y%m%d %H:%M:%S")
    
    # Request historical tick data for the stock
    client.reqHistoricalTicks(
        reqId=1,
        contract=contract,
        startDateTime=start_date,
        endDateTime=end_date,
        numberOfTicks=0,
        whatToShow="TRADES",
        useRth=0,
        ignoreSize=True,
        miscOptions=[]
    )
    
    print("Historical data request sent.")
    
    # Wait for the historical data to be received
    while not client.historicalDataReceived:
        pass
    
    print("Historical data received.")
    
    # Disconnect from IB
    client.disconnect()


if __name__ == "__main__":
    main()
