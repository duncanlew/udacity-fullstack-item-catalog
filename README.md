# Udacity Item Catalog Project
This is a project for the Udacity Full Stack Web Developer Nanodegree program.
ADD A PICTURE OF THE SITE OVER HERE

## Overview
The goal of the project is to create a stateful web application which displays a list of items within categories. User registration and authenticaiton by means of OAuth is also a part of the application. Registered users are allowed to perform CRUD actions on their own items.

For the purpose of this application, a computer shop aggregation site has been created in which users can add their shops and their products.

The used technolgies for this project are:
* something
* git
* vagrant 

## Executing the project
In order to execute the project, we need to go through a couple of steps

### 1. Install Virtualbox and Vagrant
Make sure to first install [Virtualbox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) and [Vagrant](https://www.vagrantup.com/downloads.html). 

### 2. Set up VM with configuration of Udacity and git repository
The configuration of Udacity called [FSND-Virtual-Machine.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip), needs to be downloaded. 
Change into this directory after you've unzipped the directory. Find a folder called Vagrant and `cd` into this directory. 
Afterwards, do a git clone of my repository into this folder so that my project folder is inside this Vagrant folder. 

### 3. Start up virtual machine
Start up the virtual machine by running the command `vagrant up`. After running `vagrant up`, run `vagrant ssh` to login
to the virtual machine. LOAD TO /vagrant/udacity-item-catalog



## 5. Requirements
pip3 install -r requirements.txt

### 4. Load the data into the database
Load the data into the database by running the following command
```
python3 database_initializer.py
```

### 6. Run the python command to generate the reports
python3 project.py

Go to a browser and load localhost:5000


## Sources