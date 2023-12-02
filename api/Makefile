DC_FILE ?= docker-compose.yml

build:
	$(info ===> Building Docker image)
	@docker-compose -f $(DC_FILE) build

local:
	$(info ===> Starting Docker containers)
	@docker-compose -f $(DC_FILE) up

shell:
	@docker-compose -f $(DC_FILE) run --rm web python manage.py shell

tests:
	$(info ==> Running tests)
	@docker-compose -f $(DC_FILE) run --rm web python manage.py test

makemigrations:
	$(info ==> Making migrations)
	@docker-compose -f $(DC_FILE) run --rm web python manage.py makemigrations

migrate:
	$(info ==> Migrating)
	@docker-compose -f $(DC_FILE) run --rm web python manage.py migrate

collectstatic:
	$(info ==> Collecting statics)
	@docker-compose -f $(DC_FILE) run --rm web python manage.py collectstatic --noinput

superuser:
	@docker-compose -f $(DC_FILE) run --rm web python manage.py createsuperuser

bash:
	@docker-compose -f $(DC_FILE) run --rm web bash

drop_db:
	@docker-compose -f $(DC_FILE) rm -s -v db
	rm -r db

stop:
	$(info ==> Stoping all containers)
	@docker-compose -f $(DC_FILE) stop