# TODO

- Experiment with storage of mqtt messages.

    - Which DB? Relational (SQL) or not (Mongo).
    - Create table(s) for mqtt message storage.

- Create application base.
    - Decide on structure between front end and back end applications.

        - ~~Ability to debug back end in virtual environment.~~
        - ~~Ability to stage front end for debug.~~
        - Determine how to manage python dependancies.

    - ~~Create base front end application.~~
        - ~~Simple 'Hello World' React application.~~

    - Create base back end application.
        - ~~Serve front end application.~~
        - ~~Connect to mqtt broker.~~
        - Store all mqtt message in DB.

    - ~~Create virtual test environment.~~

    - ~~Create build environment.~~

- Logging
    - Explore possibility of per class logging level.
        - Can each logging output have specific per module/class specifics?
    - Define config parameters for logging.
        - Classes/Modules to log.
        - Log level per module or class?
        - What loggers to output to.
    - Define configurable loggers.
        - Console.
        - Rolling file.
        - Syslog?
    - Errors and Warnings should always be logged by the console no matter the configuration.
    - Console by default should only log Errors ans Warning from all modules.