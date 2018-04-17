import glob
for filename in glob.glob(r'MergeInfo/*.txt'):
    with open(filename, 'r') as f:
        lines = f.readlines()

    with open(filename, 'w') as wf:
        lines = [line.replace("~", "/home/normal") for line in lines]     
        wf.writelines(lines)
print('done.')
        
