# Evaluation Step

All scripts should run in sloth/scripts

## Create user
1. execute "python create_delete_user.py create" to create user, create can be replaced by delete, show, clear

## Latency Evaluation
1. execute "python main.py".
2. 'sloth-test.log' and 'latency_data.xls' will be generated.
3. You can export 'latency_data.xls' and save somewhere else.
4. Delete 'sloth-test.log'.
5. Repeat step 1-4 about 5-10 times (you can write scripts to achieve that).

## Throughput Evaluation
1. execute 'python throughput.py mix'.
2. 'sloth-test.log' and 'throughput_data.xls' will be generated.
3. You can export 'throughput_data.xls' and save somewhere else.
4. Delete 'sloth-test.log'.
5. Repeat step 1-4 about 5-10 times (you can write scripts to achieve that).

## Neutron Comparision
1. download a neutron project, and copy the scripts folder to /neutron/scripts/
2. repeat Latency evaluation and Throughput evaluation, just modify 'sloth-test.log' to 'neutron-test.log' in 'cfg.ini',
'latency.py', 'throughput.py'.

## Note
1. throughput evaluation is multi-thread, you can modify parameters in 'throughput.py' and 'throughput_test.py'.