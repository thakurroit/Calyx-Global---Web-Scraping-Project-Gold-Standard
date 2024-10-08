# Calyx Global - Data Engineer Assignment

### Task: 
Scrape Gold Standard registry website, for voluntary carbon market projects and their
associated metadata.

● Find a list of projects at this URL: Gold Standard Project List.

● Scrape all projects from this list and store the extracted information in a database.

● Save any associated files to a specified location.


### Summary and Approach:

As part of my analysis, I examined the Gold Standard registry website, focusing on the list of projects and the individual project pages. By viewing the source and inspecting elements, I sought to determine if there were any public APIs available for the Gold Standard registry. I found that the website elements had a public API that returns a list of projects. Additionally, upon inspecting individual project pages, I discovered that there was extra information available regarding each project's summary, issuance list, and retirement list.

#### Approach
I am ingesting data from the public API, which encompasses all information about the projects, including descriptions, credit summaries, issuance lists, and retirement lists.

Alternatively, I could have utilized a web scraping framework like Scrapy if the public API had not been available. However, since the public API is accessible, ingesting data from it allows for faster processing and provides comprehensive information about the projects.

I have implemented idempotent logic to ensure that even if the program is executed multiple times, the projects listed will match those on the website. Additionally, if there are any updates to a project, the latest values will be retrieved.

#### Future Improvements
Given more time, I would have further analyzed the website, understood the exact needs for this activity from the stakeholders, and designed the solution accordingly. I envision this solution as part of a data pipeline that could be integrated with Airflow for orchestration, allowing it to run periodically. This setup would enable incremental loading of data based on the last fetched project ID, or it could check all projects for any updates or new additions.


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