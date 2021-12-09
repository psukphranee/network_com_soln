# STL to CSV Converter

Process_A opens and transfers cad_mesh.stl to Process_B via localhost:8888. Process_B writes to file 'output'
and converts it to a csv file using 'numpy-stl'. Process_B transfers the csv file back over to Process_A. Process_A saves the file as 'cad_mesh.csv'.



## Step 1) Install Process_B dependencies and Run Server

Go in to folder Process_B. Activate the virtual environment.
```
cd Process_B

source bin/activate
```

Install dependencies
```
pip3 install numpy numpy-stl
```
Run Server
```
python3 server.py
```
## Run Process_A

Go into Process_A folder and run the client.
```
cd Process_A

python3 echo_client_3.py
```

## Video Demo Link
[Video Link](https://www.youtube.com/watch?v=NZNPP1K7AUc)