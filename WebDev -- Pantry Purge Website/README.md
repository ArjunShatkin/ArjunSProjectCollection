# Spring 2025 CS 3200 Project - PantryPurge 2025
## Arjun Shatkin, Chance Bowman, Samuel Pollak, Meghan Powers

PantryPurge is a brand-new recipe database that allows users to search for recipes that fit their needs. This app will allow users to save money by making best use of what they already have in their kitchen to prevent waste. It will also take the hassle out of finding a recipe which you have all the ingredients for. Our search engine will be more open-ended than competitors, allowing novice cooks to work with what they have and making cooking more accessible to even the most casual users. Users can search by listing the ingredients they have in their pantry/fridge to be matched with recipes that best utilize those ingredients. They can also filter by other criteria such as prep time, cuisine, and dietary restrictions. 

## Prerequisites

- A GitHub Account
- A terminal-based git client or GUI Git client such as GitHub Desktop or the Git plugin for VSCode.
- VSCode with the Python Plugin
- A distribution of Python running on your laptop. Suggestions include: Anaconda or Miniconda.

## Current Project Components

Currently, there are three major components that will each run in their own Docker Containers:

- Streamlit App in the `./app` directory
- Flask REST api in the `./api` directory
- MySQL Database that will be initialized with SQL script files from the `./database-files` directory


## Suggestion for Learning the Project Code Base

If you are not familiar with web app development, this code base might be confusing. But don't worry, it's not that bad. Here are some suggestions for learning the code base:

1. Have two versions of the template repo - one for you to individually explore and lear and another for the team's project implementation.
1. Start by exploring the `./app` directory. This is where the Streamlit app is located. The Streamlit app is a Python-based web app that is used to interact with the user. It's a great way to build a simple web app without having to learn a lot of web development.
1. Next, explore the `./api` directory. This is where the Flask REST API is located. The REST API is used to interact with the database and perform other server-side tasks.
1. Finally, explore the `./database-files` directory. This is where the SQL scripts are located that will be used to initialize the MySQL database.

### Setting Up Your Personal Repo

1. In GitHub, click the **fork** button in the upper right corner of the repo screen.
1. When prompted, give the new repo a unique name, perhaps including your last name and the word 'personal'.
1. Once the fork has been created, clone YOUR forked version of the repo to your computer.
1. Set up the `.env` file in the `api` folder based on the `.env.template` file.
1. For running the testing containers (for your personal repo), you will tell `docker compose` to use a different configuration file named `docker-compose-testing.yaml`.
   1. `docker compose -f docker-compose-testing.yaml up -d` to start all the containers in the background
   1. `docker compose -f docker-compose-testing.yaml down` to shutdown and delete the containers
   1. `docker compose -f docker-compose-testing.yaml up db -d` only start the database container (replace db with api or app for the other two services as needed)
   1. `docker compose -f docker-compose-testing.yaml stop` to "turn off" the containers but not delete them.


## Handling User Role Access and Control

In most applications, when a user logs in, they assume a particular role. For instance, when one logs in to Pantry Purge, they can be a casual cook, a professional chef, analyst, or a system admin.
Each of those _roles_ will likely present some similar features as well as some different features when compared to the other roles. 

The code in this project demonstrates how to implement a simple RBAC system in Streamlit but without actually using user authentication (usernames and passwords). The Streamlit pages from the original template repo are split up among 3 roles - Political Strategist, USAID Worker, and a System Administrator role (this is used for any sort of system tasks such as re-training ML model, etc.). It also demonstrates how to deploy an ML model.

Wrapping your head around this will take a little time and exploration of this code base. Some highlights are below.

## Video Demonstration

Our video demonstration of the website can be found here: https://drive.google.com/file/d/1SeldBIGuCjIwn1rUSjzvUVfKF08ql5U5/view?usp=drive_link


