import json

#mode='2e'
mode='2b'

with open('ROAR_Sim/configurations/carla_version.txt','w') as f:

    if mode=='2b':
        f.write('0.9.10')
    elif mode=='2e':
        f.write('0.9.9')

with open('ROAR_Sim/configurations/occu_map_config.json') as f:
    occu_map_config=json.load(f)
    if mode == '2b':
        occu_map_config['absolute_maximum_map_size']=1500
    elif mode == '2e':
        occu_map_config['absolute_maximum_map_size']=550

with open('ROAR_Sim/configurations/occu_map_config.json','w') as f:
    json.dump(occu_map_config, f,indent=4)

with open('ROAR_gym/configurations/agent_configuration.json') as f:
    agent_config = json.load(f)
    if mode == '2b':
        agent_config["waypoint_file_path"] = "../ROAR_Sim/data/berkeley_minor_sdzl_waypoints.txt"
    elif mode == '2e':
        agent_config["waypoint_file_path"] = '../ROAR_Sim/data/easy_map_waypoints.txt'

with open('ROAR_gym/configurations/agent_configuration.json', 'w') as f:
    json.dump(agent_config, f,indent=4)

with open('ROAR/configurations/configuration.py') as f:
    lines=f.readlines()
    for i in range(len(lines)):
        line=lines[i]
        if 'waypoint_file_path:' in line and '=' in line and 'txt' in line:
            if mode == '2b':
                lines[i] = line[:line.find('waypoint_file_path:')]+'waypoint_file_path: str = Field(default=(Path(os.getcwd()) / "data" / "berkeley_minor_sdzl_waypoints.txt").as_posix())\n'
            elif mode == '2e':
                lines[i] = line[:line.find('waypoint_file_path:')]+'waypoint_file_path: str = Field(default=(Path(os.getcwd()) / "data" / "easy_map_waypoints.txt").as_posix())\n'

with open('ROAR/configurations/configuration.py', 'w') as f:
    f.writelines(lines)



with open('ROAR/agent_module/rl_e2e_ppo_agent.py') as f:
    lines=f.readlines()
    for i in range(len(lines)):
        line=lines[i]
        if 'occ_file_path' in line and '=' in line and 'Path' in line:
            if mode == '2b':
                lines[i] = line[:line.find('occ_file_path')]+'occ_file_path = Path("../ROAR_Sim/data/berkeley_minor_cleaned_global_occu_map.npy")\n'
            elif mode == '2e':
                lines[i] = line[:line.find('occ_file_path')]+'occ_file_path = Path("../ROAR_Sim/data/easy_map_global_occu_map.npy")\n'

with open('ROAR/agent_module/rl_e2e_ppo_agent.py','w') as f:
    f.writelines(lines)