from .helpers import *

from typing import List, Dict, Tuple

def addAciDataChangeHistory(
    conn : Connection,
    aciDataId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:

    data = {
        'aci_data_id' : aciDataId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    
    
    conn.sqlInsertRow('aci_data_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('aci_data_change_history')
  
def addAciData(
    conn : Connection,
    aciDataId : int,
    cityId : int,
    postalCodeId : int,
    airportCode : int,
    carrier : str,
    area : str,
    rateMin : float,
    rate100 : float,
    rate1000 : float,
    rate2000 : float,
    rate5000 : float,
    dateCreated : str,
    createdBy : int,
    branchId : int,
    isActive : bool,
) -> int:
    
    aciDataRow = conn.sqlGetInfo(
        'aci_data',
        'id',
        whereDetails={
            'city_id': cityId,
            'postal_code_id': postalCodeId,
            'airport_code': airportCode,
            'carrier': carrier,
            'area': area,
            'rate_min': rateMin,
            'rate_100': rate100,
            'rate_1000': rate1000,
            'rate_2000': rate2000,
            'rate_5000': rate5000,
            'date_created': dateCreated,
            'created_by': createdBy,
            'branch_id': branchId,
            'is_active': isActive
        }
    )       
    if aciDataRow:
        return aciDataRow[0].id
    data = {
        'city_id' : cityId,
        'postal_code_id' : postalCodeId,
        'airport_code' : airportCode,
        'carrier' : carrier,
        'area' : area,
        'rate_min' : rateMin,
        'rate_100' : rate100,
        'rate_1000' : rate1000,
        'rate_2000' : rate2000,
        'rate_5000' : rate5000,
        'date_created' : dateCreated,
        'created_by' : createdBy,
        'branch_id' : branchId,
        'is_active' : isActive,
    }
    conn.sqlInsertRow('aci_data', data, insertId=aciDataId)
    conn.commit()

    return conn.sqlGetLastIdCreated('aci_data')
  
def addAddress(
    conn : Connection,
    addressLine1 : str,
    addressLine2 : str,
    cityName : str,
    postalCode : str,
    regionDetails : Dict[str, any],
    countryDetails : Dict[str, any]
):

    if not addressLine1 or not cityName or not postalCode or not regionDetails or not countryDetails:
        return None

    cityId, postalCodeId = addCityPostalCode(conn, cityName, postalCode, regionDetails=regionDetails, countryDetails=countryDetails)
    
    if cityId == None or postalCodeId == None:
        return None
      
    addressLine1 = addressLine1.lower()
    
    if type(addressLine2) == str:
        addressLine2 = addressLine2.lower()
        if addressLine2.strip() == '':
            addressLine2 = None
        
    
    addressRow = conn.sqlGetInfo(
        'address',
        'id',
        whereDetails={
            'address_line_1': addressLine1,
            'address_line_2': addressLine2,
            'city_id': cityId,
            'postal_code_id': postalCodeId
        }
    )
    if addressRow:
        return addressRow[0].id
    
    addressData = {
        'address_line_1' : addressLine1,
        'address_line_2' : addressLine2,
        'city_id' : cityId,
        'postal_code_id' : postalCodeId
    }
    
    conn.sqlInsertRow('address', addressData)
    conn.commit()
    
    return conn.sqlGetLastIdCreated('address')
  
def addAgentChangeHistory(
    conn : Connection,
    agentId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:

    data = {
        'agent_id' : agentId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('agent_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('agent_change_history')

def addAgent(
    conn : Connection,
    customerId : int,
    emailAddress : str,
    firstName : str,
    lastName : str,
    phoneId : int,
    mobilePhoneId : int,
    faxId : int,
    isSetToAutoNotifyEmail : bool,
    isActive : bool,
) -> int:
    agentRow = conn.sqlGetInfo(
        'agent',
        'id',
        whereDetails={
            'customer_id': customerId,
            'email_address': emailAddress,
            'first_name': firstName,
            'last_name': lastName,
            'phone_id': phoneId,
            'mobile_phone_id': mobilePhoneId,
            'fax_id': faxId,
            'is_set_to_auto_notify_email': isSetToAutoNotifyEmail,
            'is_active': isActive
        }
    )
    if agentRow:
        return agentRow[0].id

    data = {
        'customer_id' : customerId,
        'email_address' : emailAddress,
        'first_name' : firstName,
        'last_name' : lastName,
        'phone_id' : phoneId,
        'mobile_phone_id' : mobilePhoneId,
        'fax_id' : faxId,
        'is_set_to_auto_notify_email' : isSetToAutoNotifyEmail,
        'is_active' : isActive,
    }
    conn.sqlInsertRow('agent', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('agent')
  
def addAgentCertificationTest(
    conn : Connection,
    agentId : int,
    certificationTestId : int,
    dateTested : str,
    testScore : int,
    isActive : bool,
) -> int:
    agentCertificationTestRow = conn.sqlGetInfo(
        'agent_certification_test',
        'id',
        whereDetails={
            'agent_id': agentId,
            'certification_test_id': certificationTestId,
            'date_tested': dateTested,
            'test_score': testScore,
            'is_active': isActive
        }
    )
    if agentCertificationTestRow:
        return agentCertificationTestRow[0].id
    data = {
        'agent_id' : agentId,
        'certification_test_id' : certificationTestId,
        'date_tested' : dateTested,
        'test_score' : testScore,
        'is_active' : isActive,
    }
    conn.sqlInsertRow('agent_certification_test', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('agent_certification_test')  
  
def addArchiveErrorLog(
    conn : Connection,
    orderId : int,
    archiveDate : str,
    userId : int,
    details : int,
) -> int:

    data = {
        'order_id' : orderId,
        'archive_date' : archiveDate,
        'user_id' : userId,
        'details' : details,
    }
    conn.sqlInsertRow('archive_error_log', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('archive_error_log')

def addArchiveHistory(
    conn : Connection,
    dateArchived : str,
    openOrders : int,
    openOrderAssessorials : int,
    openOrderDimensions : int,
    openOrderDrivers : int,
    openOrderAttachments : int,
    invoicedOrders : int,
    invoicedOrderAssessorials : int,
    invoicedOrderDimensions : int,
    invoicedOrderDrivers : int,
    invoicedOrderAttachments : int,
    remainingOrders : int,
    remainingOrderAssessorials : int,
    remainingOrderDimensions : int,
    remainingOrderDrivers : int,
    remainingOrderAttachments : int,
    dockOrders : int,
    dockOrderAssessorials : int,
    dockOrderDimensions : int,
    dockOrderDrivers : int,
    dockOrderAttachments : int,
    serviceOrders : int,
    serviceOrderAssessorials : int,
    serviceOrderDimensions : int,
    serviceOrderDrivers : int,
    serviceOrderAttachments : int,
    activeOrderHistory : int,
    activeOrderHawbs : int,
    archivedOrders : int,
    archivedOrderAssessorials : int,
    archivedOrderDimensions : int,
    archivedOrderDrivers : int,
    archivedOrderAttachments : int,
    archivedOrderHistory : int,
    archivedOrderHawbs : int,
    removedOrders : int,
    removedOrderAssessorials : int,
    removedOrderDimensions : int,
    removedOrderDrivers : int,
    removedOrderAttachments : int,
    removedOrderHistory : int,
    removedOrderHawbs : int,
) -> int:
    data = {
        'date_archived' : dateArchived,
        'open_orders' : openOrders,
        'open_order_assessorials' : openOrderAssessorials,
        'open_order_dimensions' : openOrderDimensions,
        'open_order_drivers' : openOrderDrivers,
        'open_order_attachments' : openOrderAttachments,
        'invoiced_orders' : invoicedOrders,
        'invoiced_order_assessorials' : invoicedOrderAssessorials,
        'invoiced_order_dimensions' : invoicedOrderDimensions,
        'invoiced_order_drivers' : invoicedOrderDrivers,
        'invoiced_order_attachments' : invoicedOrderAttachments,
        'remaining_orders' : remainingOrders,
        'remaining_order_assessorials' : remainingOrderAssessorials,
        'remaining_order_dimensions' : remainingOrderDimensions,
        'remaining_order_drivers' : remainingOrderDrivers,
        'remaining_order_attachments' : remainingOrderAttachments,
        'dock_orders' : dockOrders,
        'dock_order_assessorials' : dockOrderAssessorials,
        'dock_order_dimensions' : dockOrderDimensions,
        'dock_order_drivers' : dockOrderDrivers,
        'dock_order_attachments' : dockOrderAttachments,
        'service_orders' : serviceOrders,
        'service_order_assessorials' : serviceOrderAssessorials,
        'service_order_dimensions' : serviceOrderDimensions,
        'service_order_drivers' : serviceOrderDrivers,
        'service_order_attachments' : serviceOrderAttachments,
        'active_order_history' : activeOrderHistory,
        'active_order_hawbs' : activeOrderHawbs,
        'archived_orders' : archivedOrders,
        'archived_order_assessorials' : archivedOrderAssessorials,
        'archived_order_dimensions' : archivedOrderDimensions,
        'archived_order_drivers' : archivedOrderDrivers,
        'archived_order_attachments' : archivedOrderAttachments,
        'archived_order_history' : archivedOrderHistory,
        'archived_order_hawbs' : archivedOrderHawbs,
        'removed_orders' : removedOrders,
        'removed_order_assessorials' : removedOrderAssessorials,
        'removed_order_dimensions' : removedOrderDimensions,
        'removed_order_drivers' : removedOrderDrivers,
        'removed_order_attachments' : removedOrderAttachments,
        'removed_order_history' : removedOrderHistory,
        'removed_order_hawbs' : removedOrderHawbs,
    }
    conn.sqlInsertRow('archive_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('archive_history')
  
def addAssessorialChangeHistory(
    conn : Connection,
    assessorialId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:

    data = {
        'assessorial_id' : assessorialId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('assessorial_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('assessorial_change_history')
  
def addAssessorial(
    conn : Connection,
    assessorialId : int,
    branchId : int,
    assessorialName : str,
    minCharge : float,
    basisType : float,
    basisPortion : float,
    basisRate : float,
    userPrompt : str,
    dateCreated : str,
    notes : str,
    isActive : bool,
) -> int:
    assessorialRow = conn.sqlGetInfo(
        'assessorial',
        'id',
        whereDetails={
            'branch_id': branchId,
            'assessorial_name': assessorialName,
            'min_charge': minCharge,
            'basis_type': basisType,
            'basis_portion': basisPortion,
            'basis_rate': basisRate,
            'user_prompt': userPrompt,
            'date_created': dateCreated,
            'notes': notes,
            'is_active': isActive
        }
    )
    if assessorialRow:
        return assessorialRow[0].id
    data = {
        'branch_id' : branchId,
        'assessorial_name' : assessorialName,
        'min_charge' : minCharge,
        'basis_type' : basisType,
        'basis_portion' : basisPortion,
        'basis_rate' : basisRate,
        'user_prompt' : userPrompt,
        'date_created' : dateCreated,
        'notes' : notes,
        'is_active' : isActive,
    }
    conn.sqlInsertRow('assessorial', data, insertId=assessorialId)
    conn.commit()

    return conn.sqlGetLastIdCreated('assessorial')
  
def addBranchChangeHistory(
    conn : Connection,
    branchId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:

    data = {
        'branch_id' : branchId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('branch_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('branch_change_history')
  
def addBranch(
    conn : Connection,
    branchId : int,
    branchName : str,
    companyId : int,
    addressId : int,
    airportCode : str,
    email : str,
    phoneId : int,
    faxId : int,
    cartageAgentType : str,
    fuelServiceCharge : float,
    transferRate : float,
    internationalAirDimDivisor : int,
    domesticAirDimDivisor : int,
    truckDimDivisor : int,
    aciLow : str,
    aciHigh : str,
    notes : str,
    isActive : bool,
) -> int:
    branchRow = conn.sqlGetInfo(
      'branch',
      'id',
      whereDetails={
          'branch_name': branchName,
          'company_id': companyId,
          'address_id': addressId,
          'airport_code': airportCode,
          'email': email,
          'phone_id': phoneId,
          'fax_id': faxId,
          'cartage_agent_type': cartageAgentType,
          'fuel_service_charge': fuelServiceCharge,
          'transfer_rate': transferRate,
          'international_air_dim_divisor': internationalAirDimDivisor,
          'domestic_air_dim_divisor': domesticAirDimDivisor,
          'truck_dim_divisor': truckDimDivisor,
          'aci_low': aciLow,
          'aci_high': aciHigh,
          'notes': notes,
          'is_active': isActive
      }
    )
    if branchRow:
        return branchRow[0].id
    data = {
        'branch_name' : branchName,
        'company_id' : companyId,
        'address_id' : addressId,
        'airport_code' : airportCode,
        'email' : email,
        'phone_id' : phoneId,
        'fax_id' : faxId,
        'cartage_agent_type' : cartageAgentType,
        'fuel_service_charge' : fuelServiceCharge,
        'transfer_rate' : transferRate,
        'international_air_dim_divisor' : internationalAirDimDivisor,
        'domestic_air_dim_divisor' : domesticAirDimDivisor,
        'truck_dim_divisor' : truckDimDivisor,
        'aci_low' : aciLow,
        'aci_high' : aciHigh,
        'notes' : notes,
        'is_active' : isActive,
    }
    conn.sqlInsertRow('branch', data, insertId=branchId)
    conn.commit()

    return conn.sqlGetLastIdCreated('branch')

def addCertificationTest(
    conn : Connection,
    certificationTestId : id,
    certificationName : str,
    certificationTestTrainerId : int,
    isActive : bool,
) -> int:
    certificationTestRow = conn.sqlGetInfo(
        'certification_test',
        'id',
        whereDetails={
            'certification_name': certificationName,
            'certification_test_trainer_id': certificationTestTrainerId,
            'is_active': isActive
        }
    )
    if certificationTestRow:
        return certificationTestRow[0].id

    data = {
        'certification_name': certificationName,
        'certification_test_trainer_id': certificationTestTrainerId,
        'is_active': isActive,
    }
    conn.sqlInsertRow('certification_test', data, insertId=certificationTestId)
    conn.commit()

    return conn.sqlGetLastIdCreated('certification_test')
  
def addCertificationTestChangeHistory(
    conn : Connection,
    certificationTestId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:
    certificationTestChangeHistoryRow = conn.sqlGetInfo(
        'certification_test_change_history',
        'id',
        whereDetails={
            'certification_test_id': certificationTestId,
            'user_id': userId,
            'date_changed': dateChanged,
            'changes': changes
        }
    )
    if certificationTestChangeHistoryRow:
        return certificationTestChangeHistoryRow[0].id
    data = {
        'certification_test_id' : certificationTestId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('certification_test_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('certification_test_change_history')  

def addCertificationTestTrainer(
    conn : Connection,
    trainerName : str,
    isActive : bool,
) -> int:
    certificationTestTrainerRow = conn.sqlGetInfo(
        'certification_test_trainer',
        'id',
        whereDetails={
            'trainer_name': trainerName,
            'is_active': isActive
        }
    )
    if certificationTestTrainerRow:
        return certificationTestTrainerRow[0].id

    data = {
        'trainer_name' : trainerName,
        'is_active' : isActive,
    }
    conn.sqlInsertRow('certification_test_trainer', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('certification_test_trainer')
  
def addCertificationTestTrainerChangeHistory(
    conn : Connection,
    certificationTestTrainerId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:
    certificationTestTrainerChangeHistoryRow = conn.sqlGetInfo(
        'certification_test_trainer_change_history',
        'id',
        whereDetails={
            'certification_test_trainer_id': certificationTestTrainerId,
            'user_id': userId,
            'date_changed': dateChanged,
            'changes': changes
        }
    )
    if certificationTestTrainerChangeHistoryRow:
        return certificationTestTrainerChangeHistoryRow[0].id

    data = {
        'certification_test_trainer_id' : certificationTestTrainerId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('certification_test_trainer_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('certification_test_trainer_change_history')

def addCityPostalCode(
    conn : Connection,
    cityId : int,
    postalCodeId : int,
    lat : float,
    long : float,
) -> int:
    data = {
        'city_id' : cityId,
        'postal_code_id' : postalCodeId,
        'lat' : lat,
        'long' : long,
    }
    conn.sqlInsertRow('city_postal_code', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('city_postal_code')
  

def addCityRegion(
    conn : Connection,
    cityId : int,
    regionId : int,
) -> int:
    data = {
        'city_id' : cityId,
        'region_id' : regionId,
    }
    conn.sqlInsertRow('city_region', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('city_region')
  
def addCityPostalCode(
    conn : Connection,
    cityName : str,
    postalCode : str,
    regionDetails : Dict[str, str],
    countryDetails : Dict[str, str]
) -> Tuple[int] :
    
    if not cityName or not postalCode or not regionDetails or not countryDetails:
        return (None, None)
    
    cityName = cityName.lower()
    postalCode = postalCode.lower()
    
    regionId = addRegion(conn, regionDetails, countryDetails)
    
    if regionId == None:
        return (None, None)
    
    cityRow = conn.sqlGetInfo('city INNER JOIN city_region ON [city].[id] = [city_region].[city_id]', '[city].[id] AS selected_city_id', f"[city].[city_name] = '{cityName}' AND [city_region].[region_id] = '{regionId}'")
    postalCodeRow = conn.sqlGetInfo('postal_code INNER JOIN postal_code_region ON [postal_code].id = [postal_code_region].[postal_code_id]', '[postal_code].[id] AS selected_postal_code_id', f"[postal_code].[postal_code] = '{postalCode}' AND [postal_code_region].[region_id] = '{regionId}'")
    if cityRow:
        cityId = cityRow[0].selected_city_id
    else:
        cityData = {
            'city_name' : cityName
        }
        conn.sqlInsertRow('city', cityData)
        conn.commit()
        
        cityId = conn.sqlGetLastIdCreated('city')
    if postalCodeRow:
        postalCodeId = postalCodeRow[0].selected_postal_code_id
    else:
        postalCodeData = {
            'postal_code' : postalCode
        }
        conn.sqlInsertRow('postal_code', postalCodeData)
        conn.commit()
        
        postalCodeId = conn.sqlGetLastIdCreated('postal_code')
        
    if cityRow and postalCodeRow:
        return (cityId, postalCodeId)
    
    cityRegionData = {
        'city_id' : cityId,
        'region_id' : regionId
    }
    conn.sqlInsertRow('city_region', cityRegionData)
    conn.commit()
        
    postalCodeRegionData = {
        'postal_code_id' : postalCodeId,
        'region_id' : regionId
    }
    conn.sqlInsertRow('postal_code_region', postalCodeRegionData)
    conn.commit()
    
    cityPostalCodeData = {
        'city_id' : cityId,
        'postal_code_id' : postalCodeId,
        'lat' : getCityLat(cityName=cityName, postalCode=postalCode),
        'lng' : getCityLat(cityName=cityName, postalCode=postalCode)
    }
    conn.sqlInsertRow('city_postal_code', cityPostalCodeData)
    conn.commit()
    
    return (cityId, postalCodeId)
  
def addCompanyChangeHistory(
    conn : Connection,
    companyId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:

    data = {
        'company_id' : companyId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('company_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('company_change_history')
  
def addCompany(
    conn : Connection,
    companyId : int,
    companyName : str,
    addressId : int,
    phoneId : int,
    airportCode : str,
    faxId : int,
    cartageAgentType : str,
    employerIdentificationNo : str,
    email : str,
    scac : str,
    website : str,
    notes : str,
    logoPath : str,
    isTsaCompliant : bool,
    isActive : bool,
) -> int:
    data = {
        'company_name' : companyName,
        'address_id' : addressId,
        'phone_id' : phoneId,
        'airport_code' : airportCode,
        'fax_id' : faxId,
        'cartage_agent_type' : cartageAgentType,
        'employer_identification_no' : employerIdentificationNo,
        'email' : email,
        'scac' : scac,
        'website' : website,
        'notes' : notes,
        'logo_path' : logoPath,
        'is_tsa_compliant' : isTsaCompliant,
        'is_active' : isActive,
    }
    conn.sqlInsertRow('company', data, insertId=companyId)
    conn.commit()

    return conn.sqlGetLastIdCreated('company')
  
def addCountry(
    conn : Connection,
    countryDetails : Dict[str, str]
) -> int:    
    if not countryDetails:
        return None
    if 'countryName' in countryDetails:
        countryName = countryDetails['countryName'].lower().strip()
        if not countryName:
            return None
        countryRow = conn.sqlGetInfo('country', 'id', f"[country_name] = '{countryName}'")
        if countryRow:
            return countryRow[0].id
        data = {
            'iso_code_2': countryGet(name=countryName)[0]['alpha_2'].lower(),
            'iso_code_3': countryGet(name=countryName)[0]['alpha_3'].lower(),
            'country_name': countryName
        }
    elif 'isoCode2' in countryDetails:
        isoCode2 = countryDetails['isoCode2'].lower().strip()
        if not isoCode2:
            return None
        countryRow = conn.sqlGetInfo('country', 'id', f"[iso_code_2] = '{isoCode2}'")
        if countryRow:
            return countryRow[0].id
        data = {
            'iso_code_2': isoCode2,
            'iso_code_3': countryGet(alpha_2=isoCode2)[0]['alpha_3'].lower(),
            'country_name': countryGet(alpha_2=isoCode2)[0]['name'].lower()
        }
    elif 'isoCode3' in countryDetails:
        isoCode3 = countryDetails['isoCode3'].lower().strip()
        if not isoCode3:
            return None
        countryRow = conn.sqlGetInfo('country', 'id', f"[iso_code_3] = '{isoCode3}'")
        if countryRow:
            return countryRow[0].id
        data = {
            'iso_code_2': countryGet(alpha_3=isoCode3)[0]['alpha_2'].lower(),
            'iso_code_3': isoCode3,
            'country_name': countryGet(alpha_3=isoCode3)[0]['name'].lower()
        }
    elif 'default' in countryDetails:
        countryRow = conn.sqlGetInfo('country', 'id', f"[iso_code_2] = 'us'")
        if countryRow:
            return countryRow[0].id
        data = {
            'iso_code_2': 'us',
            'iso_code_3': 'usa',
            'country_name': 'united states'
        }
        
    conn.sqlInsertRow('country', data)
    conn.commit()
    
    return conn.sqlGetLastIdCreated('country')
  
def addCustomerChangeHistory(
    conn : Connection,
    customerId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:

    data = {
        'customer_id' : customerId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('customer_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('customer_change_history')
  
def addCustomerDefaultAssessorial(
    conn : Connection,
    customerId : int,
    assessorialId : int,
) -> int:
    customerDefaultAssessorialRow = conn.sqlGetInfo(
        'customer_default_assessorial',
        'id',
        whereDetails={
            'customer_id': customerId,
            'assessorial_id': assessorialId
        }
    )
    if customerDefaultAssessorialRow:
        return customerDefaultAssessorialRow[0].id

    data = {
        'customer_id' : customerId,
        'assessorial_id' : assessorialId,
    }
    conn.sqlInsertRow('customer_default_assessorial', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('customer_default_assessorial')

def addCustomer(
    conn : Connection,
    customerId : int,
    branchId : int,
    customerName : str,
    addressId : int,
    phoneId : int,
    defaultRateId : int,
    fuelServiceCharge : float,
    qbCustomerRefId : str,
    qbCustomerRefName : str,
    isQbInvoiceOmitted : bool,
    isActive : bool,
    notes : bool,
) -> int:
    customerRow = conn.sqlGetInfo(
        'customer',
        'id',
        whereDetails={
            'branch_id': branchId,
            'customer_name': customerName,
            'address_id': addressId,
            'phone_id': phoneId,
            'default_rate_id': defaultRateId,
            'fuel_service_charge': fuelServiceCharge,
            'qb_customer_ref_id': qbCustomerRefId,
            'qb_customer_ref_name': qbCustomerRefName,
            'is_qb_invoice_omitted': isQbInvoiceOmitted,
            'is_active': isActive,
            'notes': notes
        }
    )
    if customerRow:
        return customerRow[0].id

    data = {
        'branch_id' : branchId,
        'customer_name' : customerName,
        'address_id' : addressId,
        'phone_id' : phoneId,
        'default_rate_id' : defaultRateId,
        'fuel_service_charge' : fuelServiceCharge,
        'qb_customer_ref_id' : qbCustomerRefId,
        'qb_customer_ref_name' : qbCustomerRefName,
        'is_qb_invoice_omitted' : isQbInvoiceOmitted,
        'is_active' : isActive,
        'notes' : notes,
    }
    conn.sqlInsertRow('customer', data, insertId=customerId)
    conn.commit()

    return conn.sqlGetLastIdCreated('customer')
  
def addFax(
    conn : Connection,
    countryCode : str,
    areaCode : str,
    faxNumber : str,
    faxExtension : str,
) -> int:        
    faxRow = conn.sqlGetInfo('fax', 'id',
        whereDetails={
            'country_code' : countryCode,
            'area_code' : areaCode,
            'fax_number' : faxNumber,
            'fax_extension' : faxNumber
        }
    )
    if faxRow:
        return faxRow[0].id
    data = {
        'country_code' : countryCode,
        'area_code' : areaCode,
        'fax_number' : faxNumber,
        'fax_extension' : faxExtension,
    }
    conn.sqlInsertRow('fax', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('fax')
  
def addHoliday(
    conn : Connection,
    holidayName : str,
    holidayDate : str,
) -> int:
    holidayRow = conn.sqlGetInfo(
        'holiday',
        'id',
        whereDetails={
            'holiday_name': ''.join(["''" if x == "'" else x for x in holidayName]),
            'holiday_date': holidayDate
        }
    )
    if holidayRow:
        return holidayRow[0].id

    data = {
        'holiday_name': holidayName,
        'holiday_date': holidayDate,
    }
    conn.sqlInsertRow('holiday', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('holiday')

def addLocationChangeHistory(
    conn : Connection,
    locationId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:

    data = {
        'location_id' : locationId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('location_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('location_change_history')
  
def addLocationDefaultAssessorial(
    conn : Connection,
    locationId : int,
    assessorialId : int,
) -> int:
    locationDefaultAssessorialRow = conn.sqlGetInfo(
        'location_default_assessorial',
        'id',
        whereDetails={
            'location_id': locationId,
            'assessorial_id': assessorialId
        }
    )
    if locationDefaultAssessorialRow:
        return locationDefaultAssessorialRow[0].id

    data = {
        'location_id' : locationId,
        'assessorial_id' : assessorialId,
    }
    conn.sqlInsertRow('location_default_assessorial', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('location_default_assessorial')
  
def addLocation(
    conn : Connection,
    branchId : int,
    companyName : str,
    locationName : str,
    addressId : int,
    aciId : int,
    contactFirstName : str,
    contactLastName : str,
    contactEmail : str,
    contactPhoneId : int,
    isCarrier : bool,
    isLocal : bool,
    isInternational : bool,
    defaultWaitTime : int,
    isActive : bool,
) -> int:
    locationRow = conn.sqlGetInfo(
        'location',
        'id',
        whereDetails={
            'branch_id': branchId,
            'company_name': companyName,
            'location_name': locationName,
            'address_id': addressId,
            'aci_id': aciId,
            'contact_first_name': contactFirstName,
            'contact_last_name': contactLastName,
            'contact_email': contactEmail,
            'contact_phone_id': contactPhoneId,
            'is_carrier': isCarrier,
            'is_local': isLocal,
            'is_international': isInternational,
            'default_wait_time': defaultWaitTime,
            'is_active': isActive
        }
    )
    if locationRow:
        return locationRow[0].id

    data = {
        'branch_id' : branchId,
        'company_name' : companyName,
        'location_name' : locationName,
        'address_id' : addressId,
        'aci_id' : aciId,
        'contact_first_name' : contactFirstName,
        'contact_last_name' : contactLastName,
        'contact_email' : contactEmail,
        'contact_phone_id' : contactPhoneId,
        'is_carrier' : isCarrier,
        'is_local' : isLocal,
        'is_international' : isInternational,
        'default_wait_time' : defaultWaitTime,
        'is_active' : isActive,
    }
    conn.sqlInsertRow('location', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('location')
  
def addOrderAssessorial(
    conn : Connection,
    orderId : int,
    assessorialId : int,
    parentType : str,
    basisCount : float,
    totalCharge : float,
) -> int:
    orderAssessorialRow = conn.sqlGetInfo(
        'order_assessorial',
        'id',
        whereDetails={
            'order_id': orderId,
            'assessorial_id': assessorialId,
            'parent_type': parentType,
            'basis_count': basisCount,
            'total_charge': totalCharge
        }
    )
    if orderAssessorialRow:
        return orderAssessorialRow[0].id

    data = {
        'order_id' : orderId,
        'assessorial_id' : assessorialId,
        'parent_type' : parentType,
        'basis_count' : basisCount,
        'total_charge' : totalCharge,
    }
    conn.sqlInsertRow('order_assessorial', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('order_assessorial')
  
def addOrderAttachment(
    conn : Connection,
    orderId : int,
    attachmentPath : str,
    fileSize : float,
) -> int:
    orderAttachmentRow = conn.sqlGetInfo(
        'order_attachment',
        'id',
        whereDetails={
            'order_id': orderId,
            'attachment_path': attachmentPath,
            'file_size': fileSize
        }
    )
    if orderAttachmentRow:
        return orderAttachmentRow[0].id
    data = {
        'order_id' : orderId,
        'attachment_path' : attachmentPath,
        'file_size' : fileSize,
    }
    conn.sqlInsertRow('order_attachment', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('order_attachment')
  
def addOrderChangeHistory(
    conn : Connection,
    orderId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:
    data = {
        'order_id' : orderId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('order_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('order_change_history')
  
def addOrderDim(
    conn : Connection,
    orderId : int,
    unitType : str,
    unitQuantity : int,
    unitWeight : int,
    dimHeight : int,
    dimWidth : int,
    dimLength : int,
    dimWeight : float,
) -> int:
    orderDimRow = conn.sqlGetInfo(
        'order_dim',
        'id',
        whereDetails={
            'order_id': orderId,
            'unit_type': unitType,
            'unit_quantity': unitQuantity,
            'unit_weight': unitWeight,
            'dim_height': dimHeight,
            'dim_width': dimWidth,
            'dim_length': dimLength,
            'dim_weight': dimWeight
        }
    )
    if orderDimRow:
        return orderDimRow[0].id

    data = {
        'order_id' : orderId,
        'unit_type' : unitType,
        'unit_quantity' : unitQuantity,
        'unit_weight' : unitWeight,
        'dim_height' : dimHeight,
        'dim_width' : dimWidth,
        'dim_length' : dimLength,
        'dim_weight' : dimWeight,
    }
    conn.sqlInsertRow('order_dim', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('order_dim')
  
def addOrderDriver(
    conn : Connection,
    orderId : int,
    driverUserId : int,
    orderLeg : str,
    driverRole : str,
) -> int:
    orderDriverRow = conn.sqlGetInfo(
        'order_driver',
        'id',
        whereDetails={
            'order_id': orderId,
            'driver_user_id' : driverUserId,
            'order_leg': orderLeg,
            'driver_role': driverRole
        }
    )
    if orderDriverRow:
        return orderDriverRow[0].id

    data = {
        'order_id' : orderId,
        'order_leg' : orderLeg,
        'driver_role' : driverRole,
    }
    conn.sqlInsertRow('order_driver', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('order_driver')

def addOrderStatusChangeHistory(
    conn : Connection,
    orderStatusId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:

    data = {
        'order_status_id' : orderStatusId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('order_status_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('order_status_change_history')
  
def addOrderStatus(
    conn : Connection,
    orderStatusId : int,
    sequenceNumber : int,
    orderStatusName : str,
    isOnManifest : bool,
    isSetToAutoNotify : bool,
    isActive : bool,
    branchId : int,
) -> int:
    orderStatusRow = conn.sqlGetInfo(
        'order_status',
        'id',
        whereDetails={
            'order_status_name': orderStatusName,
            'is_on_manifest': isOnManifest,
            'is_set_to_auto_notify': isSetToAutoNotify,
            'is_active': isActive,
            'branch_id': branchId
        }
    )
    if orderStatusRow:
        return orderStatusRow[0].id
    data = {
        'order_status_name' : orderStatusName,
        'is_on_manifest' : isOnManifest,
        'sequence_number' : sequenceNumber,
        'is_set_to_auto_notify' : isSetToAutoNotify,
        'is_active' : isActive,
        'branch_id' : branchId,
    }
    conn.sqlInsertRow('order_status', data, insertId=orderStatusId)
    conn.commit()

    return conn.sqlGetLastIdCreated('order_status')
  
def addOrderType(
    conn : Connection,
    orderTypeId : int,
    orderTypeName : str,
) -> int:
    orderTypeRow = conn.sqlGetInfo(
        'order_type',
        'id',
        whereDetails={
            'order_type_name': orderTypeName
        }
    )
    if orderTypeRow:
        return orderTypeRow[0].id

    data = {
        'order_type_name' : orderTypeName,
    }
    conn.sqlInsertRow('order_type', data, insertId=orderTypeId)
    conn.commit()

    return conn.sqlGetLastIdCreated('order_type')

def addOrder(
    conn : Connection,
    orderId : int,
    branchId : int,
    orderTypeId : int,
    customerId : int,
    agentId : int,
    rateId : int,
    hawb : str,
    mawb : str,
    orderNotes : str,
    puTimeStart : str,
    puTimeEnd : str,
    delTimeStart : str,
    delTimeEnd : str,
    puLocationId : int,
    puNotes : str,
    delLocationId : int,
    delNotes : str,
    driverName : str,
    podSignee : str,
    podTimeSigned : str,
    podNotes : str,
    statusId : int,
    ratingWeightCharges : float,
    ratingFuelCharges : float,
    ratingServiceCharges : float,
    ratingTotalCharges : float,
    ratingTotalExpenses : float,
    ratingStorageCharges : float,
    ratingAdjustments : float,
    ratingNotes : float,
    quickbooksCustomerListId : str,
    quickbooksCustomerName : str,
    quickbooksInvoiceReferenceNumber : str,
    quickbooksLineSequenceNumber : str,
    isAutoAssessorials : bool,
    isWeightChargeCalculated : bool,
) -> int:

    data = {
        'branch_id' : branchId,
        'order_type_id' : orderTypeId,
        'customer_id' : customerId,
        'agent_id' : agentId,
        'rate_id' : rateId,
        'hawb' : hawb,
        'mawb' : mawb,
        'order_notes' : orderNotes,
        'pu_time_start' : puTimeStart,
        'pu_time_end' : puTimeEnd,
        'del_time_start' : delTimeStart,
        'del_time_end' : delTimeEnd,
        'pu_location_id' : puLocationId,
        'pu_notes' : puNotes,
        'del_location_id' : delLocationId,
        'del_notes' : delNotes,
        'driver_name' : driverName,
        'pod_signee' : podSignee,
        'pod_time_signed' : podTimeSigned,
        'pod_notes' : podNotes,
        'status_id' : statusId,
        'rating_weight_charges' : ratingWeightCharges,
        'rating_fuel_charges' : ratingFuelCharges,
        'rating_service_charges' : ratingServiceCharges,
        'rating_total_charges' : ratingTotalCharges,
        'rating_total_expenses' : ratingTotalExpenses,
        'rating_storage_charges' : ratingStorageCharges,
        'rating_adjustments' : ratingAdjustments,
        'rating_notes' : ratingNotes,
        'quickbooks_customer_list_id' : quickbooksCustomerListId,
        'quickbooks_customer_name' : quickbooksCustomerName,
        'quickbooks_invoice_reference_number' : quickbooksInvoiceReferenceNumber,
        'quickbooks_line_sequence_number' : quickbooksLineSequenceNumber,
        'is_auto_assessorials' : isAutoAssessorials,
        'is_weight_charge_calculated' : isWeightChargeCalculated,
    }
    conn.sqlInsertRow('order', data, insertId=orderId)
    conn.commit()

    return conn.sqlGetLastIdCreated('order')
  
def addOvernightMaintenanceHistory(
    conn : Connection,
    dateOvernightMaintenance : str,
    userId : int,
    openOrdersIn : int,
    openOrderAssessorialsIn : int,
    openOrderDimensionsIn : int,
    openOrderDriversIn : int,
    openOrderAttachmentsIn : int,
    invoicedOrdersIn : int,
    invoicedOrderAssessorialsIn : int,
    invoicedOrderDimensionsIn : int,
    invoicedOrderDriversIn : int,
    invoicedOrderAttachmentsIn : int,
    remainingOrdersIn : int,
    remainingOrderAssessorialsIn : int,
    remainingOrderDimensionsIn : int,
    remainingOrderDriversIn : int,
    remainingOrderAttachmentsIn : int,
    openOrdersOut : int,
    openOrderAssessorialsOut : int,
    openOrderDimensionsOut : int,
    openOrderDriversOut : int,
    openOrderAttachmentsOut : int,
    invoicedOrdersOut : int,
    invoicedOrderAssessorialsOut : int,
    invoicedOrderDimensionsOut : int,
    invoicedOrderDriversOut : int,
    invoicedOrderAttachmentsOut : int,
    remainingOrdersOut : int,
    remainingOrderAssessorialsOut : int,
    remainingOrderDimensionsOut : int,
    remainingOrderDriversOut : int,
    remainingOrderAttachmentsOut : int,
) -> int:

    data = {
        'date_overnight_maintenance' : dateOvernightMaintenance,
        'user_id' : userId,
        'open_orders_in' : openOrdersIn,
        'open_order_assessorials_in' : openOrderAssessorialsIn,
        'open_order_dimensions_in' : openOrderDimensionsIn,
        'open_order_drivers_in' : openOrderDriversIn,
        'open_order_attachments_in' : openOrderAttachmentsIn,
        'invoiced_orders_in' : invoicedOrdersIn,
        'invoiced_order_assessorials_in' : invoicedOrderAssessorialsIn,
        'invoiced_order_dimensions_in' : invoicedOrderDimensionsIn,
        'invoiced_order_drivers_in' : invoicedOrderDriversIn,
        'invoiced_order_attachments_in' : invoicedOrderAttachmentsIn,
        'remaining_orders_in' : remainingOrdersIn,
        'remaining_order_assessorials_in' : remainingOrderAssessorialsIn,
        'remaining_order_dimensions_in' : remainingOrderDimensionsIn,
        'remaining_order_drivers_in' : remainingOrderDriversIn,
        'remaining_order_attachments_in' : remainingOrderAttachmentsIn,
        'open_orders_out' : openOrdersOut,
        'open_order_assessorials_out' : openOrderAssessorialsOut,
        'open_order_dimensions_out' : openOrderDimensionsOut,
        'open_order_drivers_out' : openOrderDriversOut,
        'open_order_attachments_out' : openOrderAttachmentsOut,
        'invoiced_orders_out' : invoicedOrdersOut,
        'invoiced_order_assessorials_out' : invoicedOrderAssessorialsOut,
        'invoiced_order_dimensions_out' : invoicedOrderDimensionsOut,
        'invoiced_order_drivers_out' : invoicedOrderDriversOut,
        'invoiced_order_attachments_out' : invoicedOrderAttachmentsOut,
        'remaining_orders_out' : remainingOrdersOut,
        'remaining_order_assessorials_out' : remainingOrderAssessorialsOut,
        'remaining_order_dimensions_out' : remainingOrderDimensionsOut,
        'remaining_order_drivers_out' : remainingOrderDriversOut,
        'remaining_order_attachments_out' : remainingOrderAttachmentsOut,
    }
    conn.sqlInsertRow('overnight_maintenance_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('overnight_maintenance_history')
  
def addPhone(
    conn : Connection,
    countryCode : str,
    areaCode : str,
    phoneNumber : str,
    phoneExtension : str,
) -> int:
    if areaCode == '' or phoneNumber == '':
        return None
    
    phoneRow = conn.sqlGetInfo('phone', 'id',
        whereDetails={
            'country_code' : countryCode,
            'area_code' : areaCode,
            'phone_number' : phoneNumber,
            'phone_extension' : phoneExtension
        }
    )
    if phoneRow:
        return phoneRow[0].id
    data = {
        'country_code' : countryCode,
        'area_code' : areaCode,
        'phone_number' : phoneNumber,
        'phone_extension' : phoneExtension,
    }
    conn.sqlInsertRow('phone', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('phone')
  
def addPositionChangeHistory(
    conn : Connection,
    positionId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:

    data = {
        'position_id' : positionId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('position_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('position_change_history')
  
def addPosition(
    conn : Connection,
    positionId : int,
    positionName : str,
    securityLevel : int,
    isActive : bool,
    branchId : int,
) -> int:
    positionRow = conn.sqlGetInfo(
        'position',
        'id',
        whereDetails={
            'position_name' : positionName,
            'security_level' : securityLevel,
            'is_active' : isActive,
            'branch_id' : branchId
        }
    )
    if positionRow:
        return positionRow[0].id
    data = {
        'position_name' : positionName,
        'security_level' : securityLevel,
        'is_active' : isActive,
        'branch_id' : branchId,
    }
    conn.sqlInsertRow('position', data, insertId=positionId)
    conn.commit()

    return conn.sqlGetLastIdCreated('position')
  
def addPostalCodeRegion(
    conn : Connection,
    postalCodeId : int,
    regionId : int,
) -> int:
    data = {
        'postal_code_id' : postalCodeId,
        'region_id' : regionId,
    }
    conn.sqlInsertRow('postal_code_region', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('postal_code_region')

def addRateArea(
    conn : Connection,
    rateId : int,
    area : str,
    rateMin : float,
    rate100 : float,
    rate1000 : float,
    rate2000 : float,
    rate5000 : float,
    rateMax : float,
) -> int:
    rateAreaRow = conn.sqlGetInfo(
        'rate_area',
        'id',
        whereDetails={
            'rate_id': rateId,
            'area': area,
            'rate_min': rateMin,
            'rate_100': rate100,
            'rate_1000': rate1000,
            'rate_2000': rate2000,
            'rate_5000': rate5000,
            'rate_max': rateMax
        }
    )
    if rateAreaRow:
        return rateAreaRow[0].id

    data = {
        'rate_id' : rateId,
        'area' : area,
        'rate_min' : rateMin,
        'rate_100' : rate100,
        'rate_1000' : rate1000,
        'rate_2000' : rate2000,
        'rate_5000' : rate5000,
        'rate_max' : rateMax,
    }
    conn.sqlInsertRow('rate_area', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('rate_area')
  
def addRateChangeHistory(
    conn : Connection,
    rateId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:

    data = {
        'rate_id' : rateId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('rate_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('rate_change_history')
  
def addRate(
    conn : Connection,
    rateId : int,
    rateName : str,
    branchId : int,
    isDefault : bool,
    isActive : bool,
    dateAdded : str,
    addedByUserId : int,
) -> int:
    rateRow = conn.sqlGetInfo(
        'rate',
        'id',
        whereDetails={
            'rate_name': rateName,
            'branch_id': branchId,
            'is_default': isDefault,
            'is_active': isActive,
            'date_added': dateAdded,
            'added_by_user_id': addedByUserId
        }
    )
    if rateRow:
        return rateRow[0].id

    data = {
        'rate_name' : rateName,
        'branch_id' : branchId,
        'is_default' : isDefault,
        'is_active' : isActive,
        'date_added' : dateAdded,
        'added_by_user_id' : addedByUserId,
    }
    conn.sqlInsertRow('rate', data, insertId=rateId)
    conn.commit()

    return conn.sqlGetLastIdCreated('rate')
  
def addRegion(
    conn : Connection,
    regionDetails : Dict[str, str],
    countryDetails : Dict[str, str]
) -> int : 
    if not regionDetails or not countryDetails:
        return None
    
    countryId = addCountry(conn, countryDetails=countryDetails)
    countryIsoCode = conn.sqlGetInfo('country', 'iso_code_2', f"[id] = '{countryId}'")[0].iso_code_2
    
    
    if 'regionName' in regionDetails:      
        regionName = regionDetails['regionName'].lower().strip()
        
        if not regionName:
          return None
        regionRow = conn.sqlGetInfo('region', 'id', f"[region_name] = '{regionName}' AND [country_id] = {countryId}")
        if regionRow:
            return regionRow[0].id
        
        for region in regionGet(name=regionName):
            if region['code'][0:1].lower() == countryIsoCode:
                correctRegion = region
                break
        data = {
            'region_name' : regionName,
            'iso_code' : correctRegion[3:].lower(),
            'country_id' : countryId
        } 
    elif 'isoCode' in regionDetails:
        isoCode = regionDetails['isoCode'].lower().strip()
        if not isoCode:
            return None
        regionRow = conn.sqlGetInfo('region', 'id', f"[iso_code] = '{isoCode}' AND [country_id] = '{countryId}'")
        if regionRow:
            return regionRow[0].id
        data = {
            'region_name': regionGet(code=f'{countryIsoCode}-{isoCode}'.upper())[0]['name'].lower(),
            'iso_code' : isoCode,
            'country_id' : countryId
        }
        
    conn.sqlInsertRow('region', data)    
    conn.commit()
    
    return conn.sqlGetLastIdCreated('region')
  
def addSpecialChangeHistory(
    conn : Connection,
    specialId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:

    data = {
        'special_id' : specialId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('special_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('special_change_history')
  
def addSpecial(
    conn : Connection,
    oldId : int,
    branchId : int,
    weekday : int,
    startTime : int,
    endTime : int,
    area : str,
    isActive : bool,
) -> int:
    specialRow = conn.sqlGetInfo(
        'special',
        'id',
        whereDetails={
            'old_id': oldId,
            'branch_id': branchId,
            'weekday': weekday,
            'start_time': startTime,
            'end_time': endTime,
            'area': area,
            'is_active': isActive
        }
    )
    if specialRow:
        return specialRow[0].id

    data = {
        'old_id' : oldId,
        'branch_id' : branchId,
        'weekday' : weekday,
        'start_time' : startTime,
        'end_time' : endTime,
        'area' : area,
        'is_active' : isActive,
    }
    conn.sqlInsertRow('special', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('special')
  

def addUserChangeHistory(
    conn : Connection,
    userChangedId : int,
    userId : int,
    dateChanged : str,
    changes : str,
) -> int:

    data = {
        'user_changed_id' : userChangedId,
        'user_id' : userId,
        'date_changed' : dateChanged,
        'changes' : changes,
    }
    conn.sqlInsertRow('user_change_history', data)
    conn.commit()

    return conn.sqlGetLastIdCreated('user_change_history')
  
def addUser(
    conn : Connection,
    userId : int,
    username : str,
    email : str,
    passwordHash : str,
    passwordSalt : str,
    namePrefix : str,
    firstName : str,
    lastName : str,
    nameSuffix : str,
    addressId : int,
    branchId : int,
    commissionRate : float,
    dateHired : str,
    dateTerminated : str,
    phoneMainId : int,
    phoneHomeId : int,
    phoneMobileId : int,
    positionId : int,
    tsaNumber : str,
    tsaType : str,
    tsaTaken : str,
    isActive : bool,
    isDefaultDocOwner : bool,
    isSecurityCoordinator : bool,
    isTsaTrainer : bool,
) -> int:
    userRow = conn.sqlGetInfo(
        'user',
        'id',
        whereDetails    ={
            'username': username,
            'email': email,
            'password_hash': passwordHash,
            'password_salt': passwordSalt,
            'name_prefix': namePrefix,
            'first_name': firstName,
            'last_name': lastName,
            'name_suffix': nameSuffix,
            'address_id': addressId,
            'branch_id': branchId,
            'commission_rate': commissionRate,
            'date_hired': dateHired,
            'date_terminated': dateTerminated,
            'phone_main_id': phoneMainId,
            'phone_home_id': phoneHomeId,
            'phone_mobile_id': phoneMobileId,
            'position_id': positionId,
            'tsa_number': tsaNumber,
            'tsa_type': tsaType,
            'tsa_taken': tsaTaken,
            'is_active': isActive,
            'is_default_doc_owner': isDefaultDocOwner,
            'is_security_coordinator': isSecurityCoordinator,
            'is_tsa_trainer': isTsaTrainer
        }
    )
    if userRow:
        return userRow[0].id
    data = {
        'username' : username,
        'email' : email,
        'password_hash' : passwordHash,
        'password_salt' : passwordSalt,
        'name_prefix' : namePrefix,
        'first_name' : firstName,
        'last_name' : lastName,
        'name_suffix' : nameSuffix,
        'address_id' : addressId,
        'branch_id' : branchId,
        'commission_rate' : commissionRate,
        'date_hired' : dateHired,
        'date_terminated' : dateTerminated,
        'phone_main_id' : phoneMainId,
        'phone_home_id' : phoneHomeId,
        'phone_mobile_id' : phoneMobileId,
        'position_id' : positionId,
        'tsa_number' : tsaNumber,
        'tsa_type' : tsaType,
        'tsa_taken' : tsaTaken,
        'is_active' : isActive,
        'is_default_doc_owner' : isDefaultDocOwner,
        'is_security_coordinator' : isSecurityCoordinator,
        'is_tsa_trainer' : isTsaTrainer,
    }
    conn.sqlInsertRow('user', data, insertId=userId)
    conn.commit()

    return conn.sqlGetLastIdCreated('user')
  
