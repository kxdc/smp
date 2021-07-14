import os

def exists_file(filename):

    if not os.path.exists(filename):
        print(filename, " is empty")
        return False
    else:
        print("processing ", filename)
        return True


def process_file(filename):

    if exists_file(filename):
        # do somting
    else:
        return

if __name__ == '__main__':

    file_path = "/path/to/xxxx"
    
    process_file(xls_name)

