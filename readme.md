# Calyx Global - Data Engineer Assignment

### Task: 
Scrape Gold Standard registry website, for voluntary carbon market projects and their
associated metadata.

● Find a list of projects at this URL: Gold Standard Project List.

● Scrape all projects from this list and store the extracted information in a database.

● Save any associated files to a specified location.


### Summary and Approach:

As part of my analysis, I analyzed Gold Standard registry website: list of projects and individual project page.
By viewing source and inspecting elements I sought if there were any public apis available for Gold Standard registry website.
There was public api for Gold Standard registry website which returned list of projects, additionally on inspecting individual page I found there were additional information about individual project's summary, issuance list and retirement list.  

Approach: 
I am ingesting data from the public api which covers all the information about projects including description, credit summary, issuance list and retirement list.

Alternatively I could have used web scraping framework like Scrapy if the public api wasn't available. 
But in this case as the public API is available, ingesting data from the API provides faster processing and additional information about the projects.

I have applied idempotent logic, which makes sure that even if the program is executed multiple times the projects listed will match that on the website additionally if there is any update to the  project it will take the latest value for the same.

Future improvements:
If not the time constraints I would have analysed the website more, known the exact need for this activity from the stakeholders and designed the solution accordingly.
I assume this solution to be a part of a data pipeline where it can be incorporated with Airflow for orchestration and run periodically and load data incrementally based on last fetched project_id or check for all projects if there is any update or additional projects


## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)

## Requirements

- Python 3.x
- PostgreSQL
- SQLAlchemy
- Requests

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/thakurroit/Calyx_Global_Gold_Standard_Web_Scraping.git
   cd Calyx_Global_Gold_Standard_Web_Scraping
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt

   ```
3. Set up your PostgreSQL database:
   * Set Environment Variables
   ```bash
   export DATABASE_USER='your_username'
   export DATABASE_PASSWORD='your_password'
   ```

   * Create a new database named gold_standard (or update the DATABASE_URL in ingest.py to point to your existing database).

   * Ensure you have a PostgreSQL user with access to the database.

## Usage
To run the data ingestion process, execute the ingest.py script:

   ```bash
   python ingest.py
   ```
The script will connect to the Gold Standard API, fetch the data, and store it in your PostgreSQL database.

## File Structure
**ingest.py**: Main script to connect to the database and orchestrate the data ingestion process. It creates the database tables and initializes a session.

**models.py**: Defines the database schema using SQLAlchemy ORM. Includes classes for Project, SustainableDevelopmentGoal, Summary, IssuanceList, and Retirement.

**utils.py**: Contains utility functions for data ingestion from the Gold Standard API. This includes functions for fetching projects, summaries, issuance lists, and retirements.

## Database Tables
**projects**: Stores information about each carbon credit project.

**sustainable_development_goals**: Contains sustainable development goals related to each project.

**summary**: Provides a summary of credits for each project.

**issuance_list**: Records the issuance details of carbon credits for each project.

**retirements**: Records the retirement details of carbon credits for each project.