# IT5_Final-Project
# MHIE-ni MART (GROCERY POINT OF SALE)
This system is a data based system with the implementation of GUI via PyQt6

# CORE
under this directory is the core of this project - the database
  # db.py
  is the one responsible for creating database for items and for purchase.
  
# FEATURES
under the features directory are the necessary items to be shown in the GUI, they are as follows;
  # DASHBOARD
  the dashboard stores the current date, the total sales, and the total transactions. It also updates automatically
  # ITEMS
  this section lets the user add items into the inventory, delete items, and also update.
  # PURCHASE
  this section is where the purchasing happens. This section lets user to choose any product from the list, and enter their desired quantity, then stocks are deducted, after it will be storeed in the urchase database.
  # TRANSACTIONS
  this directory is where all the transactions are being stored. This part also lets you view the receipt by clicking any row from any of the transactions. 

# SHELL
under this directory is where or how the main window should look like.
  # main_window
  this file is where I was able to add image, tabs, the window title, or overall, this is where the structure of the window is located.

# main
the main is where all the program compiled. This file is where everything is called, and is also the reason why your program is able to run.
