# Installing and Running the App

You need Poetry to install and run the application.

**Poetry** can be set up using the following commands:

**Linux, macOS, Windows (WSL):**

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Details on installing and using the official documentation are available [here](https://python-poetry.org/docs/).

---

## 1. Installation

### Cloning the repository and installing dependencies

```bash
git clone https://github.com/ram-alb/rantools-v2.git
cd rantools-v2
```

Install dependencies using Poetry:

```bash
make install
```

### To work with the project, you will need to set the values of the environment variables in the `.env.dev` file

- `SECRET_KEY`: Django secret key.
- `DEBUG`: Using debug provides you with debug toolbar.
- `DJANGO_ALLOWED_HOSTS`: Include localhost to run the application locally.
- `LDAP_URL`: LDAP server URL.
- `ATOLL_HOST`: IP address of Atoll DB.
- `ATOLL_PORT`: Port for connection to Atoll DB.
- `SERVICE_NAME`: Atoll DB service name.
- `ATOLL_LOGIN`: Username for Atoll DB.
- `ATOLL_PASSWORD`: Atoll Username's password.
- `ENM_SERVER_2`: URL for connecting to ENM2.
- `ENM_SERVER_4`: URL for connecting to ENM4.
- `ENM_LOGIN`: Username for connecting to ENM2 and ENM4.
- `ENM_PASSWORD`: ENM username's password.

### Start Local Server

Run make `dev-start` to start the local server.

```bash
make dev-start
```