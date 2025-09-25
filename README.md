Step's:
1. please clone the repository and maksure you have scret and access key configured for the public cloud eg:aws in my case
2. run python script
   - Use --key flag and mention the specific attribute to fetch data eg:instancetypr or status etc.
   Eg:  < python3 filename.py --instance-id instancid --key InstanceType t2.micro>
   - To fetch the entire data just remove the --key flag and run the command
   Eg:  < python3 filename.py --instance-id instancid >
  
   
