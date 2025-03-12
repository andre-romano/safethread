import os

from safethread.utils import INIFileHandler

# Define the path to the INI file
ini_file_path = os.path.join(os.path.dirname(__file__), 'TEST.ini')

# Create an instance of INIFileHandler
ini_handler = INIFileHandler(ini_file_path)

# Write some data to the INI file
ini_handler.set('Section1.Key1', 'Value1')
ini_handler.set('Section1.Key2', 'Value2')
ini_handler.set('Section2.Key1', 'Value3')

# Save the changes to the file
ini_handler.start_write()
ini_handler.join_write()
print(f'Written to file: {ini_file_path}')

# Create an instance of INIFileHandler
ini_handler = INIFileHandler(ini_file_path)

# Read file
ini_handler.start_read()
ini_handler.join_read()

# Read data from the INI file
value1 = ini_handler.get('Section1.Key1', 'default_value1')
value2 = ini_handler.get('Section1.Key2', 'default_value2')
value3 = ini_handler.get('Section2.Key1', 'default_value3')

print(f'Section1 -> Key1: {value1}')
print(f'Section1 -> Key2: {value2}')
print(f'Section2 -> Key1: {value3}')

if os.path.exists(ini_file_path):
    os.remove(ini_file_path)
    print(f'Removed file: {ini_file_path}')
