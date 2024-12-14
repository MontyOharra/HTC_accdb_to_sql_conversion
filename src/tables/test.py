if __name__ == '__main__':
  names = [
    'HTC300_G040_T010C_Remaining_Orders.py',
    'HTC300_G040_T010D_Dock_Orders.py',
    'HTC300_G040_T010E_Service_Orders.py',
    'HTC400_G040_T010_Orders.py',
    'HTC300_G040_T011A_Open_Order_Assessorials.py',
    'HTC300_G040_T011B_Invoiced_Order_Assessorials.py',
    'HTC300_G040_T011C_Remaining_Order_Assessorials.py',
    'HTC300_G040_T011D_Dock_Order_Assessorials.py',
    'HTC300_G040_T011E_Service_Order_Assessorials.py',
    'HTC400_G040_T011_Order_Assessorials.py',
    'HTC300_G040_T012A_Open_Order_Dims.py',
    'HTC300_G040_T012B_Invoiced_Order_Dims.py',
    'HTC300_G040_T012C_Remaining_Order_Dims.py',
    'HTC300_G040_T012D_Dock_Order_Dims.py',
    'HTC300_G040_T012E_Service_Order_Dims.py',
    'HTC400_G040_T012_Order_Dims.py',
    'HTC300_G040_T013A_Open_Order_Drivers.py',
    'HTC300_G040_T013B_Invoiced_Order_Drivers.py',
    'HTC300_G040_T013C_Remaining_Order_Drivers.py',
    'HTC300_G040_T013D_Dock_Order_Drivers.py',
    'HTC300_G040_T013E_Service_Order_Drivers.py',
    'HTC400_G040_T013_Order_Drivers.py',
    'HTC300_G040_T014A_Open_Order_Attachments.py',
    'HTC300_G040_T014B_Invoiced_Order_Attachments.py',
    'HTC300_G040_T014C_Remaining_Order_Attachments.py',
    'HTC300_G040_T014D_Dock_Order_Attachments.py',
    'HTC300_G040_T014E_Service_Order_Attachments.py',
    'HTC400_G040_T014_Order_Attachments.py',
    'HTC300_G040_T030_Orders_Update_History.py',
    'HTC300_G050_T010_Accessorials.py',
    'HTC300_G050_T010_Accessorials_Update_History.py',
  ]
  
  for name in names:
    # Creates a new file with the same name as the original file in the directory "./src/tables/access/"
    open(f'./src/tables/access/{name}', 'w+').close()