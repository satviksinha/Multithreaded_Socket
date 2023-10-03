# Multi-threaded Socket Programming

The following implementation contains five files:
- `server.py`: server side implementation
- `client.py`: client side implementation
- `file.txt`: the file to be transfered
- `input.txt`: the file containing the name of the file to be transferred and the IP address,port number of proxies and server
- `client_file.txt`: the output file saved at the client side


## How to run the code?

* Run the servers on your local machines with port numbers corresponding to the ones mentioned in the `input.txt` file which lists the IP addresses and port numberd of the proxies and server in order.
* Port number will be asked as input from the user when running the server.
* After runnning the servers on different terminals, run the client on a seperate terminal.

You'll be able to transfer file from the server to the client through the proxoes following these steps.

A new `client_file.txt` gets created on the client side with the data. If you want to transfer a binary file, change the name of the file in the following piece of code at the client side:

```python
with open("client_file.txt", 'wb') as f:
            f.write(response)
```

Replace the `client_file.txt` to the name of the file with the appropriate extension.

## About the code

* The file size is assumed to be less than 1024 bytes. If not we can always change the upper cap in the send and rcv methods.
* Classes have been created to follow OOP principles