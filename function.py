#!/usr/bin/python3
import os
import re
import sys
import time
def reset_fpga():
    f = os.popen("vivado -mode batch  -source reset_fpga.tcl")
    data = f.read()
    print(data)
    remove_file(os.getcwd(),"vivado")
    return data

def change_io_mode(mode=3):
    if mode == 2:
        f = os.popen("vivado -mode batch  -source change_io_mode_dio.tcl")
    elif mode == 3:
        f = os.popen("vivado -mode batch  -source change_io_mode_sio.tcl") 
    elif mode == 4:
        f = os.popen("vivado -mode batch  -source change_io_mode_debug.tcl") 
    else:
        pass
        #return "Mode Error, undefined mode"
    data = f.read()
    print(data)
    remove_file(os.getcwd(),"vivado")
    return data

def remove_file(path,filename):
    files = os.listdir(path)
    for i,f in enumerate(files):
        if f.find(filename)>=0 :
            os.remove(path+"/"+f)
    


def setup_pcie_driver():
    f = os.popen("bash ./dma_v3/load_driver.sh")
    data = f.read()
    return data

def init_pcie_device():
    data = setup_pcie_driver()
    write_reg(0x12c, 0x0)  # recover value
    write_reg(0x10c, 0x0)  # recover value
    write_reg(0x120, 0x0)  # recover value
    write_reg(0x0100, 0x0)
    return data

def Download_and_Process(DATA_FILE,DATA_SIZE,DATA_AddrOffset):
    
    pass

def read_reg(addr):
    f = os.popen('./dma_v3/dmatest/reg_rw /dev/xdma0_user ' + str(addr) + ' w')
    data1 = f.read()
    # print data1
    result = re.findall('Read 32-bit value at address 0x.{8}.*: 0x(.{8})\n', data1)
    value = int(result[0], 16)
    f.close()
    return value

def write_reg(addr, value):
    #os.system('./reg_rw /dev/xdma0_user ' + str(addr) + ' w ' + str(value))
    f = os.popen('./dma_v3/dmatest/reg_rw /dev/xdma0_user ' + str(addr) + ' w ' + str(value))
    f.close()
    return 0
    
def import_data(MSG_ID,PKT_ID,PKT_HEA_LEN,SIZE,AddrOffset,name):
    PKT_LEN = SIZE
    MMEM_ADDR = AddrOffset >> 6
    IMP_WORD1 = (MSG_ID << 28) + (PKT_ID << 20) + (PKT_HEA_LEN << 24) + (PKT_LEN >> 6)
    IMP_WORD2 = MMEM_ADDR
    write_reg(0x0104, IMP_WORD1)
    write_reg(0x0108, IMP_WORD2)
    write_reg(0x0100, 0x1)
    print("Info: Wait for FPGA to restore %s info."%name)
    while (read_reg(0x10c) == 0):
        pass
    write_reg(0x10c, 0x0)  # recover value

def data_download(FILE,SIZE,AddrOffset):
    ret = os.fork()
    if ret == 0:
        os.system('./dma_v3/dmatest/dma_to_device -d /dev/xdma0_h2c_0 -f ' + FILE + ' -s ' + str(SIZE) + ' -a ' + str(AddrOffset) + ' -c 1')  # MPU Insts
        sys.exit()
    else:
        print("Info: Wait for current write transactions to complete.")
        os.wait()
    print("Info: Current write transactions completed.")

# MPU TRANS
def MPU_TRANS(curChannel,MPU_AddrOffset,MPU_FILE,MPU_SIZE):
    print("Info: Writing to h2c channel %d at address offset %d." % (curChannel, MPU_AddrOffset))
    data_download(FILE=MPU_FILE, SIZE=MPU_SIZE, AddrOffset=MPU_AddrOffset)
    import_data(MSG_ID=1, PKT_ID=1, PKT_HEA_LEN=0, SIZE=MPU_SIZE, AddrOffset=MPU_AddrOffset, name='MPU')

# VP Convert
def VP_Convert(VP_HEXFILE,VP_TEMPFILE,VP_FILE,VP_SIZE):
    print("Info: Converting VP program into binary file")
    ret = os.fork()
    if ret == 0:
        os.system('vpprog/hextf2bin.py -i ' + VP_HEXFILE + ' -o ' + VP_TEMPFILE)  # hex2bin
        os.system(' dd if=' + VP_TEMPFILE + ' of=' + VP_FILE + ' ibs=' + str(VP_SIZE) + ' conv=sync')
        sys.exit()
    else:
        print("Info: Wait for current conversion to complete.")
        os.wait()
    print("Info: Current conversion completed.")

# VP TRANS
def VP_TRANS(VP_FILE,VP_SIZE,VP_AddrOffset):

    data_download(FILE=VP_FILE,SIZE=VP_SIZE,AddrOffset=VP_AddrOffset)
    import_data(MSG_ID=2,PKT_ID=2,PKT_HEA_LEN=0,SIZE=VP_SIZE,AddrOffset=VP_AddrOffset,name='VP')

# DATA TRANS
def DATA_TRANS(DATA_FILE,DATA_SIZE,DATA_AddrOffset):

    data_download(FILE=DATA_FILE, SIZE=DATA_SIZE, AddrOffset=DATA_AddrOffset)
    import_data(MSG_ID=4, PKT_ID=10, PKT_HEA_LEN=0, SIZE=DATA_SIZE, AddrOffset=DATA_AddrOffset, name='taskdata')

# Export info
def Export_Info():
    write_reg(0x120, 0x1)
    print("Info: Wait for FPGA to export value.")
    while (read_reg(0x12c) == 0):
        pass
    EXP_WORD1 = read_reg(0x124)
    EXP_WORD2 = read_reg(0x128)
    write_reg(0x12c, 0x0)  # recover value
    write_reg(0x120, 0x0)  # recover value
    # print "Export value is %x %x" %(EXP_WORD1,EXP_WORD2 )
    PKT_ID = EXP_WORD1 >> 26
    PKT_LEN = EXP_WORD1 & 0b11111111111111111111
    MMEM_ADDR = EXP_WORD2 << 6
    print("Export PKT_ID is %d" % (PKT_ID))
    print("Export PKT_LEN is %d" % (PKT_LEN))
    print("Export MMEM_ADDR is %d" % (MMEM_ADDR))
    print("Export value is %d %d" % (EXP_WORD1, EXP_WORD2))
    print("Info: current transactions completed.")
    print("Info: current transactions completed.")
    return PKT_LEN,MMEM_ADDR
# Export Data
def Export_Data(output_file,PKT_LEN,MMEM_ADDR):
    #output_file = 'output_data/output_data.bin'
    ret = os.fork()
    if ret == 0:
        os.system('./dma_from_device -d /dev/xdma0_c2h_0 -f ' + output_file + ' -s ' + str(PKT_LEN) + ' -a ' + str(
            MMEM_ADDR) + ' -c 1')  # export data
        sys.exit()
    else:
        print("Info: Wait for current read transactions to complete.")
        os.wait()
    print("Info: Current read transactions completed.")
