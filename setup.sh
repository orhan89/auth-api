#!/bin/bash

read -p "Type the name of application :" APP_NAME
read -p "Type the name for database: " DB_NAME

roots=(conf runserver.py README.md requirements.txt db scripts manage.py test APP_NAME)

function find_all_files {
    FILE=$1

    if [ -d ${FILE} ]
    then
	echo "${FILE} is directory"

	echo "Entering ${FILE} directory"
	PARENT_FILE=$FILE
	cd $FILE

	for FILE in $(ls)
	do
	    find_all_files $FILE
	done

	echo "Exiting directory $(basename $PWD)"
	FILE=$(basename $PWD)
	cd ..
    else
	echo "${FILE} is a file"
	sed -i "s/APP_NAME/${APP_NAME}/g" ${FILE}
	sed -i "s/DB_NAME/${DB_NAME}/g" ${FILE}
    fi

    if [[ $FILE == *APP_NAME* ]]
    then
        newFILE=${FILE/APP_NAME/${APP_NAME}}
        echo "Changing file name $FILE to $newFILE"
        mv $FILE $newFILE
    fi
}

for item in ${roots[*]}
do
    find_all_files $item
done

echo "================="
echo "=  GIT RELATED  ="
echo "================="

# commit all the change
echo "Commit all the change"
git add --all
git commit -m "Initial commit for application ${APP_NAME}"

read -p "Is the repository is already provided in GitHub? " -r
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    # create new repository
    echo "Create new repository"
    read -p "Github username: " GITHUB_USERNAME
    read -p "Type the repository name to create: " GITHUB_REPOS
    curl -u ${GITHUB_USERNAME} https://api.github.com/user/repos -d '{"name":"'${GITHUB_REPOS}'"}'
else
    echo "Using existing repository"
    read -p "Github username: " GITHUB_USERNAME
    read -p "Type the repository name: " GITHUB_REPOS
fi

git remote set-url origin https://github.com/${GITHUB_USERNAME}/${GITHUB_REPOS}.git

read -p "Push to repository? " -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
    # push to repository
    git push -u origin 
fi

echo "==========================="
echo "=  CONFIGURATION  FILES  ="
echo "==========================="

# add configuration file
if [ ! -d /etc/${APP_NAME} ]; then
    echo "Create directory /etc/${APP_NAME}"
    sudo mkdir /etc/${APP_NAME}
else
    echo "Directory /etc/${APP_NAME} is already exists!"
fi

if [ ! -f /etc/${APP_NAME}/development.cfg ]; then
    echo "Copy configuration file to /etc/${APP_NAME}"
    sudo cp conf/configuration.cfg /etc/${APP_NAME}/development.cfg
    sudo cp conf/configuration.cfg /etc/${APP_NAME}/testing.cfg
else
    echo "Configuration files are already exists! Please copy manually"
fi

if [[ -f /etc/${APP_NAME}/development.cfg && -f /etc/${APP_NAME}/testing.cfg ]]; then
    read -p "Type Application ID :" APP_KEY
    read -p "Type Database Host :" DB_HOST
    read -p "Type Database Username: " DB_USERNAME
    read -p "Type Database Password :" DB_PASSWORD

    for file in development testing
    do
	sudo sed -i "s/APP_KEY =/APP_KEY = \"${APP_KEY}\"/" /etc/${APP_NAME}/${file}.cfg
	sudo sed -i "s/DB_HOST =/DB_HOST = \"${DB_HOST}\"/" /etc/${APP_NAME}/${file}.cfg
	sudo sed -i "s/DB_USERNAME =/DB_USERNAME = \"${DB_USERNAME}\"/" /etc/${APP_NAME}/${file}.cfg
	sudo sed -i "s/DB_PASSWORD =/DB_PASSWORD = \"${DB_PASSWORD}\"/" /etc/${APP_NAME}/${file}.cfg
    done

    sudo sed -i "s/DB_DATABASE =/DB_DATABASE = \"${DB_NAME}\"/" /etc/${APP_NAME}/development.cfg
    sudo sed -i "s/DB_DATABASE =/DB_DATABASE = \"${DB_NAME}-test\"/" /etc/${APP_NAME}/testing.cfg

else
    echo "Configurations files doesn't exists!"
fi

echo "========================="
echo "=  PREPARING DATABASES  ="
echo "========================="

if [ -f db/${APP_NAME}.sql ]; then
    mysql -u${DB_USERNAME} -p${DB_PASSWORD} < db/${APP_NAME}.sql
    echo "OK"
fi
