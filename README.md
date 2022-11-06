# Deep Learning Playground

Web Application where people new to Machine Learning can input a dataset and experiment around with basic Pytorch modules through a drag and drop interface

> **Deployed website:** https://datasciencegt-dlp.com/ </br>
 **GitHub repo:** https://github.com/karkir0003/Deep-Learning-Playground/ </br> **Owners:** See [CODEOWNERS](./CODEOWNERS)

# How to Run

## Prerequisites
Have the following installed first:

1. [NodeJS v16](https://nodejs.org/en/download/) (should come with NPM v8)
1. [Anaconda](https://www.anaconda.com/)
1. [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html). After installing, type `aws configure` in your terminal and type in the credentials given in [Secrets](https://docs.google.com/spreadsheets/d/1fRndo-7u0MXghiZoMp3uBepDBW9EghcJ9IL4yS0TdD8/edit?usp=sharing)

## Recommended
1. [GitKraken Pro](https://help.gitkraken.com/gitkraken-client/how-to-install/)

## Shortcuts:
| Terminal   | Procedure   | Command |
|-----------|-----------|-----|
| Command Prompt | Run All | `start /B npm run startf & start npm run startb` |
| Powershell | Run All | `cmd /C 'start /B npm run startf & start npm run startb'` |
| Linux Terminal | Run All | `tmux new-session -d -s frontend_session 'npm run startf'; tmux new-session -d -s backend_session 'npm run startb'` |


## Installing/updating the frontend (one-time)
In the root directory of this project (`~/Deep-Learning-Playground`), run: 
```
npm run installf
```
## Installing/updating the backend (one-time)
```
npm run installb
```
## Running the frontend
```
npm run startf
```
## Running the backend
```
npm run startb
```

# Furter Details: Backend

## Conda Env Setup

- `conda env create -f environment.yml` in the `/conda` directory

- Updating an environment: `conda env update -f environment.yml` in the `/conda` directory

## Backend Infrastructure

`python -m backend.driver` from the `~/Deep-Learning-Playground` directory

The backend supports training of a deep learning model and/or a classical ML model

## Backend Architecture

See [Architecture.md](./.github/Architecture.md)

## Examples

To see how `driver.py` is used, see [`Backend_Examples.md`](./.github/Backend_Examples.md)

# Furter Details: Frontend

## Startup Instructions

> **Note:** You will need the `.env` file to get the `Feedback` page working, but other pages work fine without it. Run the [build_env.py](./backend/aws_helpers/aws_secrets_utils/build_env.py) using `python build.py` in the `backend/aws_helpers/aws_secrets_utils` directory.

1. For complete functionality with the backend, first, start the backend using the instructions above. The backend will be live at http://localhost:8000/

2. Then in a separate terminal, start the frontend development server. After installing the prerequisites above, run the following commands:

    ```
    cd frontend\playground-frontend
    npm install
    npm start
    ```

3. Then, go to http://localhost:3000/

## Frontend Architecture

See [Architecture.md](./.github/Architecture.md)

# License

Deep Learning Playground is MIT licensed, as found in the [LICENSE](./LICENSE) file.

Deep Learning Playground documentation is Creative Commons licensed, as found in the [LICENSE-docs](./.github/LICENSE-docs) file.
