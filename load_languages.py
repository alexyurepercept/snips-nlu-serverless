import shutil, os
 
def copyDirectory(src, dest):
    try:
        shutil.copytree(src, dest)
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)

copyDirectory(os.path.dirname(os.path.abspath(__file__)) + '/src/snips_nlu_en-0.2.1', '/tmp/sls-py-req/snips_nlu/data/en')