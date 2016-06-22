# ngsqc-flask web application

A basic front end for access to the NGSQC MySQL database which contains data from InterOp files, runparameters.xml and SamplesSheet.csv files output by Illumina MiSeq sequencers.

## Requirements

Requires an existing database called "ngsqc" containing data with a root user, and structured as indicated in the Models.
Requires Python 2.7.6+ 

Requires Flask, Flask-SQLAlchemy and Flask-Security 

Requires MySQL 5.6

## Overview of functionality
Provides access to a limited number of prepared methods for querying the database 

Provides access control through usernames and passwords and user classes 

