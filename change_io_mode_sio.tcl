
open_hw
connect_hw_server -url localhost:3121
open_hw_target 
current_hw_device [get_hw_devices xcvu13p_0]
refresh_hw_device -update_hw_probes false [lindex [get_hw_devices xcvu13p_0] 0]
set_property PROBES.FILE {./dremi_v3.1/dremi_sys_top.ltx} [get_hw_devices xcvu13p_0]
set_property FULL_PROBES.FILE {./dremi_v3.1/dremi_sys_top.ltx} [get_hw_devices xcvu13p_0]
refresh_hw_device [lindex [get_hw_devices xcvu13p_0] 0]
set_property OUTPUT_VALUE 3 [get_hw_probes ext_cfg_word -of_objects [get_hw_vios -of_objects [get_hw_devices xcvu13p_0] -filter {CELL_NAME=~"reset_block_inst1"}]]
commit_hw_vio [get_hw_probes {ext_cfg_word} -of_objects [get_hw_vios -of_objects [get_hw_devices xcvu13p_0] -filter {CELL_NAME=~"reset_block_inst1"}]]