# asset-recommendation-system
An asset recommendation system with tunable hybrid approach. 


## Milestone 1

Tech Stack: Minukube, Kafka, Python, FastAPI, MLFlow server

### Foundational Model Training Flow

![Diagram](media/foundation_training_flow.png?raw=true "diagram")


### Retraining Model Flow

![diagram](media/retraining_flow.png?raw=true "diagram")

### Setup Dev Environment

- Initialize all services: Postgres, MLFlow, Server. **Reminder:** We are using docker image to containerize all services, thus if you make any changes in any files, you have to rerun this command to see changes.

`docker compose up --build -d`

- Load foundational FAR-trans data into Postgres

`python FAR-Trans/script.py`
