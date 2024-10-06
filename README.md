# dmap-map-diff-tool

The tool is used to check for differences between stage and prod environments before promoting to prod, to ensure that changes made in prod are not overwritten.

# Required tools
1. Python3: https://www.python.org/downloads/
2. Access to prod in stage mls admin via tunels. 

# Installation
1. Install the Python3 using the links provided above.
2. Clone the repository using `git clone`.
3. Create a virtual environment: `python3 -m venv venv`.
4. Activate the virtual environment: `venv\Scripts\activate`.
5. Install the requirements: `pip install -r requirements.txt`.
6. Create `.env` with credentials to get access to MLS Admin in prod and stage. 

`HOST_STAGE=Host of MLSAdmin db on stage`

`PORT=5432`

`DATABASE=DB name`

`USER_STAGE=user`

`PASSWORD_STAGE=password on stage`

`HOST_PROD=Host of MLSAdmin db on stage`

`USER_PROD=user`

`PASSWORD_PROD=password on prod`


# Running

1. Activate tunel to prod and stage in two separate terminal windows.
2. Run the app: `python map_diff.py 422`.  - kw id of the target source.


