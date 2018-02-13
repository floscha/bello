# Bello
A productivity helper using Trello to manage tasks in a ["Bullet Journal"](http://bulletjournal.com/)-ish fashion.

## Usage

### Run Bello

The Bello service can simply be started using the provided Docker Compose configuration:
```
$ docker-compose up
```

### API Endpoints

As long as Bello does not come with a GUI, the service can only be accessed through its REST API:
- **Tasks for a week:** */weeks/<int:year>/<int:week>*
- **Tasks for a day:** */tasks/<int:year>/<int:week>/<int:day>*
