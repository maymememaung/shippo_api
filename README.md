# shippo_api
This is a simple command line interface for handling shipping related tasks using shippo api (test mode).
Reference Docs: https://goshippo.com/docs/reference.

Set Up

1. Install Python on your machine depending on your operating system at https://www.python.org/downloads/. The development environment uses Python 3.10.7.

2. Clone this repository in your desired directory.

3. Open the terminal/command and type cd shippo_api.

4. Install requirements using pip3 install -r requirements.txt, if you're using Python 3.xx.xx.

5. In this directory, create config.py.

6. Write API_KEY = "YOUR_KEY" in config.py, with YOUR_KEY your own Shippo API Key. If you don't have one, you can sign up at https://goshippo.com/products/api/. Use a test token.

5. Save config.py and run program on terminal/command using python3 main.py.

Assumptions

1. This program currently assumes that there is only one parcel/ package per shipment, for simplicity.
2. Shippo API returns all shipments in descending order of shipment creation time.