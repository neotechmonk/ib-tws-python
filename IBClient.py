import time
from datetime import datetime, timedelta

from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper


class IBClient(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.historicalDataReceived = False
    
    def historicalData(self, reqId, bar):
        print(f"Received historical data: {bar.date} - {bar.open} - {bar.high} - {bar.low} - {bar.close}")
    
    def historicalDataEnd(self, reqId, start, end):
        super().historicalDataEnd(reqId, start, end)
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
    contract.symbol = "AAPL"  # Replace with the desired stock symbol
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    
    # Calculate the start date for the historical data request
    end_date = datetime.now().strftime("%Y%m%d %H:%M:%S")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y%m%d %H:%M:%S")
    
    # Request historical data for the stock
    client.reqHistoricalData(
        reqId=1,
        contract=contract,
        endDateTime=end_date,
        durationStr="30 D",  # Request data for the last 30 days
        barSizeSetting="1 day",  # Request daily data
        whatToShow="TRADES",
        useRTH=0,
        formatDate=1,
        keepUpToDate=False,
        chartOptions=[]
    )
    
    print("Historical data request sent.")
    
    # Wait for the historical data to be received with a timeout mechanism
    timeout = 10  # Timeout duration in seconds
    start_time = time.time()
    while not client.historicalDataReceived:
        if time.time() - start_time > timeout:
            print("Timeout reached. Historical data not received.")
            break
        time.sleep(0.1)
    
    print("Historical data received.")
    
    # Disconnect from IB
    client.disconnect()


if __name__ == "__main__":
    main()
