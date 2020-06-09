#Change to your directory
os.chdir("C:/Users/Admin_2/Documents/Thesis/LUS/DeltaScenarios_TUdelft1")
notebook_dir = os.getcwd()

#Function for running GeoDMS
def geodmsrun(config, tree, geodms_dir = r"C:/Program Files/ObjectVision/GeoDms7212"): #change this to your GeoDms directory
    
    #change working directory
    notebook_dir = os.getcwd()
    os.chdir(geodms_dir)
    assert os.path.isdir(geodms_dir)
    
    print(os.getcwd())
    
    #run the geodms
    arg_exe = ['GeoDmsRun.exe', config, tree]
    call(arg_exe)
    
    #change back the working directory
    os.chdir(notebook_dir)
    print(os.getcwd())
    
    
#Functions for changing dms files
def find_line(file_path, pattern):
    #Create temp file
    lines = []
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                if pattern in line:
                    lines.append(line)
    return lines


def new_line(beginline, line, new_val, endline):
    newline = beginline + str(new_val) + line[line.find(endline):]
    return newline


def replace_line(beginline, file_path, pattern, new_val, endline):
    #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                if line==pattern:
                    subst = new_line(beginline, line, new_val, endline)
                    new_file.write(line.replace(pattern, subst))
                else:
                    new_file.write(line)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)



 
    

            
    
    
    
   
    
    
    
 



            