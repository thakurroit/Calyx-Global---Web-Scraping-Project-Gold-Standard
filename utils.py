import requests
import time
import traceback
from sqlalchemy import exc
from models import Project, SustainableDevelopmentGoal, Summary, IssuanceList, Retirement


# Ingesting projects
def ingest_data(page_number, session):
    url = f"https://public-api.goldstandard.org/projects?query=&page={page_number}&size=25&sortColumn=&sortDirection="
    
#Adding this header as a direct connection to API wasn't possible, the header here will emulate as API is requested from a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        projects = response.json()

        for project in projects:
            try:
                project_data = {
                    "id": project.get("id"),
                    "created_at": project.get("created_at"),
                    "updated_at": project.get("updated_at"),
                    "name": project.get("name"),
                    "description": project.get("description"),
                    "status": project.get("status"),
                    "gsf_standards_version": project.get("gsf_standards_version"),
                    "estimated_annual_credits": project.get("estimated_annual_credits"),
                    "crediting_period_start_date": project.get("crediting_period_start_date"),
                    "crediting_period_end_date": project.get("crediting_period_end_date"),
                    "methodology": project.get("methodology"),
                    "type": project.get("type"),
                    "size": project.get("size"),
                    "sustaincert_id": project.get("sustaincert_id"),
                    "sustaincert_url": project.get("sustaincert_url"),
                    "project_developer": project.get("project_developer"),
                    "carbon_stream": project.get("carbon_stream"),
                    "country": project.get("country"),
                    "country_code": project.get("country_code"),
                    "latitude": project.get("latitude"),
                    "longitude": project.get("longitude"),
                    "labels": project.get("labels")

                }

                existing_project = session.query(Project).filter_by(id=project_data['id']).first()
                if existing_project:
                    for key, value in project_data.items():
                        setattr(existing_project, key, value)
                    print(f"Updating existing project {project_data['id']}")
                else:
                    new_project = Project(**project_data)
                    session.add(new_project)
                    print(f"Inserting new project {project_data['id']}")

                sustainable_goals = project.get("sustainable_development_goals", [])
                for goal in sustainable_goals:
                    goal_data = {
                        "project_id": project_data['id'],
                        "name": goal.get("name"),
                        "issuable_products": goal.get("issuable_products")
                    }

                    existing_goal = session.query(SustainableDevelopmentGoal).filter_by(
                        project_id=goal_data['project_id'],
                        name=goal_data['name']
                    ).first()

                    if existing_goal:
                        existing_goal.issuable_products = goal_data['issuable_products']
                    else:
                        new_goal = SustainableDevelopmentGoal(**goal_data)
                        session.add(new_goal)

                session.commit()
                print(f"Successfully ingested project {project_data['id']}")

            except exc.SQLAlchemyError as e:
                print(f"Error occurred: {e}")
                traceback.print_exc()
                session.rollback()

            project_id = project['id']
            ingest_summary(project_id, session)
            ingest_issuance_list(project_id, session)
            ingest_retirements(project_id, session)


    else:
        print(f"Error: API request failed. Status code: {response.status_code}")


# Ingesting summary for projects
def ingest_summary(project_id, session):
    url = f"https://public-api.goldstandard.org/projects/{project_id}/credits/summary"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for item in data:
            product = item['product']
            for summary in item['summary']:
                summary_data = {
                    'project_id': project_id,
                    'product': product,
                    'status': summary['status'],
                    'total': summary['total']
                }
                existing_summary = session.query(Summary).filter_by(
                    project_id=project_id,
                    product=product,
                    status=summary['status']
                ).first()
                if existing_summary:
                    for key, value in summary_data.items():
                        setattr(existing_summary, key, value)
                else:
                    new_summary = Summary(**summary_data)
                    session.add(new_summary)

        time.sleep(1)
        session.commit()


# Ingesting issuance list for projects
def ingest_issuance_list(project_id, session):
    page = 1
    while True:
        url = f"https://public-api.goldstandard.org/projects/{project_id}/credits?page={page}&size=25&issuances=true"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if not data:  # Break if no more data
                break
            for item in data:
                issuance_data = {
                    'id': item['id'],
                    'project_id': project_id,
                    'created_at': item['created_at'],
                    'updated_at': item['updated_at'],
                    'number_of_credits': item['number_of_credits'],
                    'starting_credit_number': item['starting_credit_number'],
                    'ending_credit_number': item['ending_credit_number'],
                    'batch_number': item['batch_number'],
                    'serial_number': item['serial_number'],
                    'certified_date': item['certified_date'],
                    'monitoring_period_start_date': item['monitoring_period_start_date'],
                    'monitoring_period_end_date': item['monitoring_period_end_date'],
                    'status': item['status'],
                    'vintage': item['vintage'],
                    'is_active': item['is_active'],
                    'product_name': item['product']['name'],
                    'product_abbreviation': item['product']['abbreviation'],
                    'labels': item['labels']
                }
                existing_issuance = session.query(IssuanceList).filter_by(id=item['id']).first()
                if existing_issuance:
                    for key, value in issuance_data.items():
                        setattr(existing_issuance, key, value)
                else:
                    new_issuance = IssuanceList(**issuance_data)
                    session.add(new_issuance)
            session.commit()
            time.sleep(1)
            page += 1
        else:
            break


# Ingesting issuance list for projects
def ingest_retirements(project_id, session):
    page = 1
    while True:
        url = f"https://public-api.goldstandard.org/projects/{project_id}/credits?page={page}&size=25&issuances=false"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if not data:  # Break if no more data
                break
            for item in data:
                retirement_data = {
                    'id': item['id'],
                    'project_id': project_id,
                    'created_at': item['created_at'],
                    'updated_at': item['updated_at'],
                    'number_of_credits': item['number_of_credits'],
                    'starting_credit_number': item['starting_credit_number'],
                    'ending_credit_number': item['ending_credit_number'],
                    'batch_number': item['batch_number'],
                    'serial_number': item['serial_number'],
                    'certified_date': item['certified_date'],
                    'monitoring_period_start_date': item['monitoring_period_start_date'],
                    'monitoring_period_end_date': item['monitoring_period_end_date'],
                    'status': item['status'],
                    'vintage': item['vintage'],
                    'is_active': item['is_active'],
                    'note': item.get('note'),
                    'product_name': item['product']['name'],
                    'product_abbreviation': item['product']['abbreviation'],
                    'labels': item['labels']
                }
                existing_retirement = session.query(Retirement).filter_by(id=item['id']).first()
                if existing_retirement:
                    for key, value in retirement_data.items():
                        setattr(existing_retirement, key, value)
                else:
                    new_retirement = Retirement(**retirement_data)
                    session.add(new_retirement)
            session.commit()
            time.sleep(1)
            page += 1
        else:
            break
