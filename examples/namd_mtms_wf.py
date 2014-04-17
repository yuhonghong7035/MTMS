#!/usr/bin/env python

from radical.ensemblemd import mtms

###############################################################################
#
# Main
#
if __name__ == '__main__':

    #
    # Resource configuration
    #
    resource_desc = mtms.Resource_Description()
    resource_desc.runtime = 42 # minutes
    resource_desc.cores = 1

    #resource_desc.resource = 'localhost'
    #resource_desc.dburl = 'mongodb://localhost:27017'

    #resource_desc.resource = 'stampede.tacc.utexas.edu'
    #EXECUTABLE = '/home1/01740/marksant/bin/namd_mockup_small.sh'

    resource_desc.configs = 'file:///Users/mark/proj/mtms/tmp/futuregrid.json'
    resource_desc.resource = "india.futuregrid.org"
    EXECUTABLE = '/N/u/marksant/bin/namd_mockup_small.sh'



    #
    # Application specific runtime characteristics
    #

    # Number of chromosomes
    NUM_CHRS = 2 # exp:5
    # Number of locations per chromosome
    NUM_LOCS = 1 # exp:21
    # The time of simulation per system
    SIM_TRAJ_TIME = 3 # exp:20
    # The simulation time per dynamic step
    TASK_SIM_TIME = 1
    # Executable to run for every task
    #EXECUTABLE = 'namd-mockup.sh'
    #EXECUTABLE = '/bin/echo'
    #EXECUTABLE = '/bin/true'
    #EXECUTABLE = '/bin/false'
    DATA_PREFIX = '/Users/mark/proj/mtms/data'


    #
    # !!! No user-servicable parts below !!!
    # (Not completely true, but true enough!)
    #

    # The number of dynamic steps per system
    NUM_STEPS = SIM_TRAJ_TIME / TASK_SIM_TIME

    task_desc = mtms.Task_Description()
    task_desc.tasks = ['%d/%d' % (i,j) for i in range(NUM_CHRS) for j in range(NUM_LOCS)]
    task_desc.num_stages = NUM_STEPS
    task_desc.executable = EXECUTABLE
    task_desc.arguments = '${__TASK__} ${__STAGE__} ${i_conf} ${i_pdb} ${i_crd} ${i_parm} ${i_coor} ${i_vel} ${i_xsc} ${o_coor} ${o_vel} ${o_xsc} ${o_out} ${o_err} ${o_dcd} ${o_cvd} ${o_xst}'

    io_desc = mtms.IO_Description()
    #
    # INPUTS PER SYSTEM(S), FIRST DYNAMIC STEP(D) ONLY
    # (mineq_coor, mineq_vel, mineq_xsc)
    #     - mineq_coor[S]
    #     - mineq_vel[S]
    #     - mineq_xsc[S]
    #
    #
    io_desc.input_per_task_first_stage = {
        'i_coor': '%s/${TASK}/min-eq.coor' % DATA_PREFIX,
        'i_vel': '%s/${TASK}/min-eq.vel' % DATA_PREFIX,
        'i_xsc': '%s/${TASK}/min-eq.xsc' % DATA_PREFIX
    }

    #
    # INPUTS PER DYNAMIC STEP(D) FOR ALL SYSTEMS(S) (conf)
    #     - conf_1 .. conf_D
    #
    io_desc.input_all_tasks_per_stage = {
        'i_conf': '%s/dyn-conf-files/dyn${STAGE}.conf' % (DATA_PREFIX)
    }

    #
    # INPUTS PER SYSTEM(S) FOR ALL DYNAMIC STEPS(D)
    # (sys.pdb, sys.parm, sys.crd)
    #     - pdb[S]
    #     - parm[S]
    #     - crc[S]
    #
    io_desc.input_per_task_all_stages = {
        'i_pdb': '%s/${TASK}/sys.pdb' % DATA_PREFIX,
        'i_parm': '%s/${TASK}/sys.parm' % DATA_PREFIX,
        'i_crd': '%s/${TASK}/sys.crd' % DATA_PREFIX
    }

    #
    # SINKS PER SYSTEM(S) PER DYNAMIC STEP(D)
    # (dcd, cvd, xst, out, err)
    #     - dcd_1[S] .. dcd_D[S]
    #     - cvd_1[S] .. cvd_D[S]
    #     - xst_1[S] .. xst_D[S]
    #     - out_1[S] .. out_D[S]
    #     - err_1[S] .. err_D[S]
    #
    io_desc.output_per_task_per_stage = {
        'o_dcd': '%s/${TASK}/dyn${STAGE}.dcd' % DATA_PREFIX,
        'o_cvd': '%s/${TASK}/dyn${STAGE}.cvd' % DATA_PREFIX,
        'o_xst': '%s/${TASK}/dyn${STAGE}.xst' % DATA_PREFIX,
        'o_out': '%s/${TASK}/dyn${STAGE}.out' % DATA_PREFIX,
        'o_err': '%s/${TASK}/dyn${STAGE}.err' % DATA_PREFIX
    }

    #
    # INTERMEDIATE PER SYSTEM(S) PER DYNAMIC STEP(D)
    # (coor, vel, xsc)
    #     - coor_1[S] .. coor_D[S]
    #     - vel_1[S] .. vel_D[S]
    #     - xsc_1[S] .. xsc_D[S]
    #
    # TODO: rename to intermediate without "output" ?
    io_desc.intermediate_output_per_task_per_stage = [
        {'input_label': 'i_coor', 'output_label': 'o_coor', 'pattern': '%s/${TASK}/dyn${STAGE}.coor' % DATA_PREFIX},
        {'input_label': 'i_vel', 'output_label': 'o_vel', 'pattern': '%s/${TASK}/dyn${STAGE}.vel' % DATA_PREFIX},
        {'input_label': 'i_xsc', 'output_label': 'o_xsc', 'pattern': '%s/${TASK}/dyn${STAGE}.xsc' % DATA_PREFIX}
    ]

    #
    # OUTPUTS PER SYSTEM(S) FOR FINAL DYNAMIC STEP(D) ONLY
    # (coor, vel, xsc)
    #     - coor[S]
    #     - vel[S]
    #     - xsc[S]
    #
    io_desc.output_per_task_final_stage = {
        'o_coor': '%s/${TASK}/dyn${STAGE}.coor' % DATA_PREFIX,
        'o_vel': '%s/${TASK}/dyn${STAGE}.vel' % DATA_PREFIX,
        'o_xsc': '%s/${TASK}/dyn${STAGE}.xsc' % DATA_PREFIX
    }

    engine = mtms.Engine()
    engine.execute(resource_desc, task_desc, io_desc, verbose=True)

    print 'Done!'

#
###############################################################################
