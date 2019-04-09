Firstly you need to set up python environment in which you run robotControl.py script.
All needed packages are described in PACKAGE_LIST.txt file, to restore it you can use anaconda manager (recommended), or standard pip (write your own script).
Packages unavailable form Anaconda Cloud are described in PACKAGE_LIST_FOR_PIP_ONLY.txt, you need to install it with pip.

Example installation for Anaconda users (5 min) :

1. Call this command to import packages and create new environment:

	# $ conda create --name <env> --file PACKAGE_LIST.txt

Hint: if it fails, try to install opencv manually after restoring rest of packages.

2. Install rest of packages from PACKAGE_LIST_FOR_PIP_ONLY.txt

	$ pip install -r PACKAGE_LIST_FOR_PIP_ONLY.txt

Example for non anaconda users :

1.	
	$ pip install -r PACKAGE_LIST.txt
2.
	$ pip install -r PACKAGE_LIST_FOR_PIP_ONLY.txt

3. To run program execute python robotControl.py

If installations fails don't worry, install packages manually,
it doesn't need to be exactly the same versions of packages.