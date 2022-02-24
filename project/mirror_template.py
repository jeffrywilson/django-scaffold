#!/usr/bin/env python3

import argparse
import datetime
import os, sys

#######################################################################################################################################################################
# MIRROR SCRIPT                                                                                                                                                       #
# This script get a database source info, create a new database with prefix mirror, restore datas and apply a initial mask for user password                          #
# Rename to mirror.py and increment the other masks acoording with your app                                                                                           #
# How script run:  /usr/bin/python3  script_dir/mirror.py -ho 127.0.0.1 -d database_name -du user_name -dp user_password -fo bkp.dump -ld your_directory -mn mirror1  #
# How edit cron tab: run crontab -e (add or update jobs in crontab)                                                                                                   #
# Cron frequency map:                                                                                                                                                 #                     
#     *      *     *      *         *                                                                                                                                 #          
#   minute  hour  day   month   day(week)                                                                                                                             #          
# Example Cron job every night at midnight:                                                                                                                           #
# 0 0 * * * /usr/bin/python3  script_dir/mirror.py -ho 127.0.0.1 -d database_name -du user_name -dp user_password -fo bkp.dump -ld your_directory -mn mirror1         #  
# #####################################################################################################################################################################


def get_arguments():
    parser = argparse.ArgumentParser()

    #Parsing arguments for pg_dump command
    parser.add_argument("-ho", "--host", action="store", type=str)
    parser.add_argument("-d", "--db_name", action="store", type=str)
    parser.add_argument("-du", "--db_username", action="store", type=str)
    parser.add_argument("-dp", "--db_password", action="store", type=str)
    parser.add_argument("-fo", "--file_output", action="store", type=str)
    parser.add_argument("-ld", "--local_dir", action="store", type=str)
    parser.add_argument("-mn", "--mirror_name", action="store", type=str)
    return parser.parse_args(sys.argv[1:])

def close_sessions(args):
    close_all_session_open = "export PGPASSWORD='%s' && psql -h %s -U %s %s -c 'UPDATE pg_database SET datallowconn = 'false' WHERE datname = '%s';' " % \
                                (args.db_password, args.host, args.db_username, args.db_name, args.db_name)
    close_all_session_open = "export PGPASSWORD='%s' && psql -h %s -U %s %s -c 'UPDATE pg_database SET datallowconn = 'false' WHERE datname = 'mirror_%s';' " % \
                                (args.db_password, args.host, args.db_username, args.db_name, args.db_name)
    os.system(close_all_session_open)
    print ("#### Connections closed ####")

def backup(args):
    file_path= download_file_path(args)
    backup_command= "export PGPASSWORD='%s' && pg_dump -h %s -U %s %s -w --clean > %s" % \
                        (args.db_password, args.host, args.db_username, args.db_name, file_path)
    
    print('Running backup process...')
    os.system(backup_command)
    return file_path

def drop_mirror(args):
    
    drop_mirror_command = "export PGPASSWORD='%s' && psql -h %s -U %s %s -c 'DROP DATABASE IF EXISTS mirror_%s;' " % \
                                (args.db_password, args.host, args.db_username, args.db_name, args.db_name )
                                
    os.system(drop_mirror_command)
    print ("#### Old mirror dropped ####")

def create_mirror_database(args):
    
    create_mirror_command = "export PGPASSWORD='%s' && psql -h %s -U %s %s -w -c 'CREATE DATABASE mirror_%s;' " % \
                            (args.db_password, args.host, args.db_username, args.db_name, args.db_name)
    os.system(create_mirror_command)
    create_owner_command = "export PGPASSWORD='%s' && psql -h %s -U %s %s -w -c 'ALTER DATABASE mirror_%s OWNER TO %s;' " % \
                            (args.db_password, args.host, args.db_username, args.db_name, args.db_name, args.db_username)

    os.system(create_owner_command)
    print ("#### Mirror Database created  ####")

def restore_base(args, bkp_file_path):
    restore_mirror_command = "export PGPASSWORD='%s' && psql -U %s -h %s -d mirror_%s -f %s" % \
                            (args.db_password, args.db_username, args.host, args.db_name, bkp_file_path)

    os.system(restore_mirror_command)
    print ("#### Database restored  ####")

def mask_values(args):
    print("Masking passwords...")
    #password secret for all
    masking_password = "export PGPASSWORD='%s' && psql -h %s -U %s %s -w -c 'UPDATE user_registration_user SET password = 'pbkdf2_sha256$216000$T0GS9mvIvKdj$b1VniujT4xjwUMd5m7sSY6YuZVmOg78QGa4HRPml9w0='' " % \
                            (args.db_password, args.host, args.db_username, args.db_name)
    os.system(masking_password)
    print ("#### Data masked  ####")

def download_file_path(args):
    if not os.path.exists (args.local_dir):
        os.mkdir (args.local_dir)
    d = datetime.datetime.now()

    #list_of_files = os.listdir(args.local_dir)
    #full_path = [args.local_dir+"/{0}".format(x) for x in list_of_files]

    # delete oldest file in directory when number of files reaches a threshold (5 for this case)
    # if len(list_of_files) >= args.days_saved:
    #     oldest_file = min(full_path, key=os.path.getctime)
    #     os.remove(oldest_file)

    #create filepath with datetime for the backup file
    download_file_path= os.path.join(args.local_dir, ('%s-%s'%(d.strftime('%Y%m%d%H%M'), args.file_output)))
    return download_file_path
    
if __name__ == "__main__":
    args= get_arguments()

    ##Init script
    print("Starting to restore mirrors...")
    close_sessions(args)
    
    # Backup
    print("Creating a backup from base...")
    backup_file_path = backup(args)

    # Dropping old mirror base if exist
    print("Searching for old mirror... dropping if exists")
    drop_mirror(args)

    # Create a new mirror 
    print("Creating a new mirror base...")
    create_mirror_database(args)

    # Restoring data
    print("Restoring data from backup files...")
    restore_base(args, backup_file_path)
    
    # Masking data
    print("Masking values...")
    mask_values(args)

    #setting default values
    if not args.file_output:
        args.file_output= args.db_name

    #backup(args)
    print('Database backup done at: ', args.local_dir)