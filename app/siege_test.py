import subprocess

# define the URL of the web app to test
url = 'http://127.0.0.1:5000/analysis'

# define the number of simulated users
num_users = 10

# define the duration of the test (in seconds)
test_duration = '10s'

# define the name of the output file for the test results
output_file = 'siege_results.txt'

# define the command to execute Siege
command = f'siege -c {num_users} -t {test_duration} -v {url} > {output_file}'

# execute the command using subprocess
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# wait for the command to finish and get the output
stdout, stderr = process.communicate()

# print the output
print(stdout.decode())
print(stderr.decode())