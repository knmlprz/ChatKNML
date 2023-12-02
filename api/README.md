# Copbackend

## Setup guide
1. Install docker and docker-compose. Look [here](https://docs.docker.com/desktop/) for docs
2. We're currently using `make` to build our app. It's installed by default in most of linux distros. For Windows users
it's more complicated. Look [here](https://stackoverflow.com/questions/32127524/how-to-install-and-use-make-in-windows) for more info.
In case you'll have a problem with `make` you can use commands defined in `makefile` directly.
3. Install pre-commit:
```shell
pre-commit install
```
4. Now you're ready to build our app!!! Let's hop in:
```shell
make build
```
5. Our App serves static files (css stylesheets, fonts, images and so on) we need to collect 'em.  
This command would create a `static` directory. Look there if you're interested, what's inside ;)
```shell
make collectstatic
```
6. It's time to create tables in database (docker container with database)!
```shell
make migrate
```
7. Create superuser.
```shell
make superuser
```
8. Start the app! 
```shell
make local
```
9. Open app on web browser `http://0.0.0.0:8001/admin/`. You can log in with superuser credentials.
## Start your adventure here!
Soon we'll give ya your first tasks, but now feel free to look around the project. We recommend to look on [swagger endpoint](http://0.0.0.0:8001/swagger/) as well as [admin page](http://0.0.0.0:8001/admin/).

## Tips & tricks
1. Don't be afraid to ask questions. We're here to help ya!
2. Debug app with [Postman](https://www.postman.com/) or [Insomnia](https://insomnia.rest/)
3. If you're a student, you can use Pycharm Pro for free (and other amazing staff). Just enroll for [Github Student Pack](https://education.github.com/pack). 
