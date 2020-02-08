import re
import linecache
import pandas as pd
from pandas import DataFrame
import numpy as np
import csv
import os
import statistics

#'O:/HLS_Projects/matrix_mult_2019/solution1/.autopilot/db/a.o.3.ll'

path_name_begin='O:/HLS_Projects/BenchMarks_Hls/dfDiv_BM/division'
path_name_begin2='O:/HLS_Projects/apdcm'
path_name_begin3='O:/HLS_Projects/ultimate_new_matrix_mult'
path_name_begin4='O:/HLS_Projects/GSM/solution1'
path_name_end='/.autopilot/db/float64_div.verbose.bind.rpt'


file_list=[]
for root, dirs, files in os.walk(path_name_begin3):
    for file in files:
        if file.endswith("o.3.ll"):               # for timing and latency
            name1=os.path.join(root, file)
            name2=name1.replace('\\','/')
            file_list.append(name2)




main_df = pd.DataFrame(
    columns=['solution_name',' total_no_crit_edge','total number of instaces in CE','max(inst_per_ce)','np.mean(inst_per_ce)','sum(math_inst_all_ce)','max(math_inst_all_ce)',' np.mean(math_inst_all_ce)','sum(logic_op_ce_list)',
             ' max(logic_op_ce_list)',' np.mean(logic_op_ce_list)',' sum(mem_op_ce_list)','max(mem_op_ce_list)',' np.mean(mem_op_ce_list)',
             'sum(vec_op_ce_list)',' max(vec_op_ce_list)',' np.mean(vec_op_ce_list)','  sum(ext_op_ce_list)',' max(ext_op_ce_list)',' np.mean(ext_op_ce_list)',
             'sum(other_op_ce_list)',' max(other_op_ce_list)',' np.mean(other_op_ce_list)',
             ' total_no_BB', 'total number of instctss in bb', 'max(inst_per_bb)', 'np.mean(inst_per_bb)',
             'sum(math_inst_all_bb)', 'max(math_inst_all_bb)', ' np.mean(math_inst_all_bb)', 'sum(logic_op_bb_list)',
             ' max(logic_op_bb_list)', ' np.mean(logic_op_bb_list)', ' sum(mem_op_bb_list)', 'max(mem_op_bb_list)',
             ' np.mean(mem_op_bb_list)',
             'sum(vec_op_bb_list)', ' max(vec_op_bb_list)', ' np.mean(vec_op_bb_list)', '  sum(ext_op_bb_list)',
             ' max(ext_op_bb_list)', ' np.mean(ext_op_bb_list)',
             'sum(other_op_bb_list)', ' max(other_op_bb_list)', ' np.mean(other_op_bb_list)'
             ])



math_list = ['add ', 'mul ', 'sdiv ', 'udiv ', 'urem ', 'srem ']
ext_list = ['sext ', 'zex t']
logic_list = ['shl ', 'lshr ', 'ashr ', 'and ', 'or ', 'xor ']
flp_list = ['fadd ', 'fsub ', 'fmul ', 'fdiv ', 'frem ']
vec_op_list = ['extractelement ', 'insertelement ']
memory_op_list = ['alloca ', 'load ', 'store ', 'getelementptr ']
other_op_list = ['icmp ', 'fcmp ', 'phi ', 'select ', 'call ', 'va_arg ']

max_no_inst_bb=0
avg_no_inst_bb=0
total_no_load=0
total_no_store=0
total_no_math=0
total_no_logic=0
total_no_compare=0
max_no_math_bb=0
max_no_logic_bb=0
max_no_compare_bb=0
avg_no_math_bb=0
avg_no_logic_bb=0
avg_no_compare_bb=0





for file_name in file_list:

   # print(file_name)
    funct_array = file_name.split('/')
    solution_name = funct_array[3]





    #file_name='O:/HLS_Projects/matrix_mult_2019/solution1/.autopilot/db/a.o.3.ll'
    print(solution_name)
    data1 = open(file_name).read()
    num_bb = data1.count('<label>:')
    math_inst_all_bb=[]
    inst_per_bb=[]
    logic_op_bb_list=[]
    vec_op_bb_list=[]
    mem_op_bb_list=[]
    ext_op_bb_list=[]
    other_op_bb_list=[]
    inst_count=1

### ------------features from basic block-------------------------------------
    with open(file_name, 'rt') as file:
        copy = False

        math_inst_bb=0
        logic_inst_bb=0
        ext_inst_bb=0
        mem_op_bb=0
        vec_op_bb=0
        other_op_bb=0
        inst_count = 0
        i=1
        crit_edge_count=0
        for num, line in enumerate(file, 1):




            if '; <label>' in line:
               # print('label',i)
                i=i+1
                copy = True
                continue


            elif 'ret void' in line :
              # math_inst_all_bb.append(math_inst_bb)

               copy = False
               continue
            elif 'br label' in line:
                math_inst_all_bb.append(math_inst_bb)
                inst_per_bb.append(inst_count)
                logic_op_bb_list.append(logic_inst_bb)
                mem_op_bb_list.append(mem_op_bb)
                vec_op_bb_list.append(vec_op_bb)
                ext_op_bb_list.append(ext_inst_bb)
                other_op_bb_list.append(other_op_bb)
                inst_count=0
                math_inst_bb = 0
                logic_inst_bb=0
                mem_op_bb=0
                vec_op_bb=0
                ext_inst_bb=0
                other_op_bb=0
                copy = False
                continue
            if copy:
               # print(line)
                line_str=line.lstrip()

                if line_str[:2] != "br":
                    inst_count=inst_count+1
                if any(s in line for s in math_list):
                    math_inst_bb= math_inst_bb+1
                elif any(s in line for s in logic_list):
                    logic_inst_bb= logic_inst_bb+1
                elif any(s in line for s in ext_list):
                    ext_inst_bb = ext_inst_bb + 1
                elif any(s in line for s in memory_op_list):
                    mem_op_bb = mem_op_bb + 1
                elif any(s in line for s in vec_op_list):
                    vec_op_bb = vec_op_bb + 1
                elif any(s in line for s in other_op_list):
                    other_op_bb = other_op_bb + 1

               # print(math_inst_bb)




### ------------features from critical edge-------------------------------------

    math_inst_all_ce=[]
    inst_per_ce=[]
    logic_op_ce_list=[]
    vec_op_ce_list=[]
    mem_op_ce_list=[]
    ext_op_ce_list=[]
    other_op_ce_list=[]


    with open(file_name, 'rt') as file:
        copy = False

        total_no_crit_edge = 0
        max_no_inst_crit_edge = 0
        avg_no_inst_crit_edge = 0
        math_inst_ce = 0
        logic_inst_ce = 0
        ext_inst_ce = 0
        mem_op_ce = 0
        vec_op_ce = 0
        inst_count_ce = 0
        other_op_ce=0


        for num, line in enumerate(file, 1):

            if line[:11]=="._crit_edge":
                total_no_crit_edge=total_no_crit_edge+1
                copy = True
                continue



            elif 'br' in line:
                math_inst_all_ce.append(math_inst_ce)
                inst_per_ce.append(inst_count_ce)
                logic_op_ce_list.append(logic_inst_ce)
                mem_op_ce_list.append(mem_op_ce)
                vec_op_ce_list.append(vec_op_ce)
                ext_op_ce_list.append(ext_inst_ce)
                other_op_ce_list.append(other_op_ce)
                inst_count_ce=0
                math_inst_ce = 0
                logic_inst_ce=0
                mem_op_ce=0
                vec_op_ce=0
                ext_inst_ce=0
                other_op_ce=0
                copy = False
                continue
            if copy:
               # print(line)
                line_str=line.lstrip()

                if line_str[:2] != "br" or  line_str[:3] != "ret":
                    inst_count_ce=inst_count_ce+1
                if any(s in line for s in math_list):
                    math_inst_ce= math_inst_ce+1
                elif any(s in line for s in logic_list):
                    logic_inst_ce= logic_inst_ce+1
                elif any(s in line for s in ext_list):
                    ext_inst_ce = ext_inst_ce + 1
                elif any(s in line for s in memory_op_list):
                    mem_op_ce = mem_op_ce + 1
                elif any(s in line for s in vec_op_list):
                    vec_op_ce = vec_op_ce + 1
                elif any(s in line for s in other_op_list):
                    other_op_ce = other_op_ce + 1



    main_df = main_df.append(pd.Series(
            [solution_name,total_no_crit_edge,
             sum(inst_per_ce),max(inst_per_ce),np.mean(inst_per_ce),sum(math_inst_all_ce),max(math_inst_all_ce), np.mean(math_inst_all_ce),
             sum(logic_op_ce_list), max(logic_op_ce_list), np.mean(logic_op_ce_list), sum(mem_op_ce_list),max(mem_op_ce_list), np.mean(mem_op_ce_list),
             sum(vec_op_ce_list), max(vec_op_ce_list), np.mean(vec_op_ce_list),  sum(ext_op_ce_list), max(ext_op_ce_list), np.mean(ext_op_ce_list),
             sum(other_op_ce_list), max(other_op_ce_list), np.mean(other_op_ce_list),
             num_bb,
             sum(inst_per_bb), max(inst_per_bb), np.mean(inst_per_bb), sum(math_inst_all_bb), max(math_inst_all_bb),
             np.mean(math_inst_all_bb),
             sum(logic_op_bb_list), max(logic_op_bb_list), np.mean(logic_op_bb_list), sum(mem_op_bb_list),
             max(mem_op_bb_list), np.mean(mem_op_bb_list),
             sum(vec_op_bb_list), max(vec_op_bb_list), np.mean(vec_op_bb_list), sum(ext_op_bb_list),
             max(ext_op_bb_list), np.mean(ext_op_bb_list),
             sum(other_op_bb_list), max(other_op_bb_list), np.mean(other_op_bb_list)],index=main_df.columns), ignore_index=True)

    export_csv = main_df.to_csv('O:/HLS_Projects/ll_file_data_matrix_mult.csv', index=None, header=True)




'''

             func_name,target_clk, estimated_clk, uncertainity, max_latency, min_latency, pipe_line_type, num_of_states,
             total_fcu_delay,
             max_fcu_delay, num_of_fcu, max_state_delay, min_state_delay], index=main_df.columns), ignore_index=True)

                   # print(math_inst_bb)
    
    '''



'''
    p=0

    print("-----------critical edge features--------------------")

    p=p+1
    print('total # of critical edges= ',total_no_crit_edge)
    p=p+1

    print('total # of instructions in all critical edge of  design= ',sum(inst_per_ce))
    p=p+1
    print('max # of instructions in all critical edge design= ',max(inst_per_ce))
    p=p+1
    print('average # of instructions in all critical edge design= ',np.mean(inst_per_ce))
    p=p+1

    print('total # of math ops in all CRITICAL EDGE design= ',sum(math_inst_all_ce))
    p=p+1
    print('max # of math ops in CRITICAL EDGE= ',max(math_inst_all_ce))
    p=p+1
    print('avg # of math ops in CRITICAL EDGE== ',np.mean(math_inst_all_ce))
    p=p+1

    print('total # of logic ops in critical edge design= ',sum(logic_op_ce_list))
    p=p+1
    print('max # of logic ops in critical edge= ',max(logic_op_ce_list))
    p=p+1
    print('avg # of logic ops in critical edge== ',np.mean(logic_op_ce_list))
    p=p+1


    print('total # of mem ops in critical edge design= ',sum(mem_op_ce_list))
    p=p+1
    print('max # of mem ops in critical edge design= ',max(mem_op_ce_list))
    p=p+1
    print('avg # of mem ops in critical edge design= ',np.mean(mem_op_ce_list))
    p=p+1

    print('total # of ext ops in critical edge design= ',sum(ext_op_ce_list))
    p=p+1
    print('max # of ext ops in critical edge design= ',max(ext_op_ce_list))
    p=p+1
    print('avg # of ext ops in critical edge  design= ',np.mean(ext_op_ce_list))
    p=p+1

    print('total # of vector ops in critical edge design= ',sum(vec_op_ce_list))
    p=p+1
    print('max # of vector ops in critical edge design= ',max(vec_op_ce_list))
    p=p+1
    print('avg # of vector ops in critical edge  design= ',np.mean(vec_op_ce_list))
    p=p+1
    
    print('total # of other ops in critical edge design= ',sum(other_op_ce_list))
    p=p+1
    print('max # of other ops in critical edge design= ',max(other_op_ce_list))
    p=p+1
    print('avg # of other ops in critical edge  design= ',np.mean(other_op_ce_list))
    p=p+1
    
    
    


    print("-----------basic block features--------------------")


    print('total # of basic block= ',num_bb)

    print('total # of instruction in design= ',sum(inst_per_bb))
    p=p+1
    print('max # of instruction in design= ',max(inst_per_bb))
    p=p+1
    print('average # of instruction in design= ',np.mean(inst_per_bb))
    p=p+1

    print('total # of math ops in design= ',sum(math_inst_all_bb))
    p=p+1
    print('max # of math ops in bb= ',max(math_inst_all_bb))
    p=p+1
    print('avg # of math ops in bb== ',np.mean(math_inst_all_bb))
    p=p+1

    print('total # of logic ops in design= ',sum(logic_op_bb_list))
    p=p+1
    print('max # of logic ops in bb= ',max(logic_op_bb_list))
    p=p+1

    print('avg # of logic ops in bb== ',np.mean(logic_op_bb_list))
    p=p+1



    print('total # of mem ops in design bb= ',sum(mem_op_bb_list))
    p=p+1

    print('max # of mem ops in design bb= ',max(mem_op_bb_list))
    p=p+1

    print('avg # of mem ops in design bb= ',np.mean(mem_op_bb_list))
    p=p+1


    print('total # of ext ops in design bb= ',sum(ext_op_bb_list))
    p=p+1

    print('max # of ext ops in design bb= ',max(ext_op_bb_list))
    p=p+1

    print('avg # of ext ops in design bb= ',np.mean(ext_op_bb_list))


    p=p+1
    print('total # of vector ops in design bb= ',sum(vec_op_bb_list))
    p=p+1

    print('max # of vector ops in design bb= ',max(vec_op_bb_list))
    p=p+1

    print('avg # of vector ops in design bb= ',np.mean(vec_op_bb_list))
    
    
        p=p+1
    print('total # of other ops in design bb= ',sum(other_op_bb_list))
    p=p+1

    print('max # of other ops in design bb= ',max(other_op_bb_list))
    p=p+1

    print('avg # of other ops in design bb= ',np.mean(other_op_bb_list))
    
    
    

    print("number of featutes=== ", p)
    #print('max no of math inst in bb= ', math_inst_bb,  'average no of math inst= ', math_inst_bb, 'total inst= ', inst_count, 'number of bb= ', num_bb)

'''













































