from .helpers import *
from typing import Any, Optional, Callable


def addAciDataChangeHistory(
    conn: SqlServerConn,
    aciDataId: int | None,
    userId: int | None,
    dateChanged: str | None,
    changes: str | None,
) -> int:
    data = {
        "aci_data_id": aciDataId,
        "user_id": userId,
        "date_changed": dateChanged,
        "changes": changes,
    }

    conn.insertRow("aci_data_change_history", data)

    return conn.getLastIdCreated("aci_data_change_history")


def addAciData(
    conn: SqlServerConn,
    aciDataId: int | None,
    cityId: int | None,
    postalCodeId: int | None,
    airportCode: int | None,
    carrier: str | None,
    area: str | None,
    rateMin: float | None,
    rate100: float | None,
    rate1000: float | None,
    rate2000: float | None,
    rate5000: float | None,
    dateCreated: str | None,
    createdBy: int | None,
    branchId: int | None,
    isActive: bool | None,
) -> int:
    aciDataRow = conn.select(
        "aci_data",
        "id",
        whereDetails={
            "city_id": cityId,
            "postal_code_id": postalCodeId,
            "airport_code": airportCode,
            "carrier": carrier,
            "area": area,
            "rate_min": rateMin,
            "rate_100": rate100,
            "rate_1000": rate1000,
            "rate_2000": rate2000,
            "rate_5000": rate5000,
            "date_created": dateCreated,
            "created_by": createdBy,
            "branch_id": branchId,
            "is_active": isActive,
        },
    )
    if aciDataRow:
        return aciDataRow[0].id
    data = {
        "city_id": cityId,
        "postal_code_id": postalCodeId,
        "airport_code": airportCode,
        "carrier": carrier,
        "area": area,
        "rate_min": rateMin,
        "rate_100": rate100,
        "rate_1000": rate1000,
        "rate_2000": rate2000,
        "rate_5000": rate5000,
        "date_created": dateCreated,
        "created_by": createdBy,
        "branch_id": branchId,
        "is_active": isActive,
    }
    conn.insertRow("aci_data", data, insertId=aciDataId)

    return conn.getLastIdCreated("aci_data")


def addAddress(
    conn: SqlServerConn,
    addressLine1: str | None,
    addressLine2: str | None | None,
    cityName: str | None,
    postalCode: str | None,
    regionDetails: dict[str, Any],
    countryDetails: dict[str, Any],
) -> int | None:

    if (
        not addressLine1
        or not cityName
        or not postalCode
        or not regionDetails
        or not countryDetails
    ):
        return None

    cityId, postalCodeId = addCityPostalCode(
        conn,
        cityName,
        postalCode,
        regionDetails=regionDetails,
        countryDetails=countryDetails,
    )

    if cityId == None or postalCodeId == None:
        return None

    addressLine1 = addressLine1.lower()

    if type(addressLine2) == str:
        addressLine2 = addressLine2.lower()
        if addressLine2.strip() == "":
            addressLine2 = None

    addressRow = conn.select(
        "address",
        "id",
        whereDetails={
            "address_line_1": addressLine1,
            "address_line_2": addressLine2,
            "city_id": cityId,
            "postal_code_id": postalCodeId,
        },
    )
    if addressRow:
        return addressRow[0].id

    addressData = {
        "address_line_1": addressLine1,
        "address_line_2": addressLine2,
        "city_id": cityId,
        "postal_code_id": postalCodeId,
    }

    conn.insertRow("address", addressData)

    return conn.getLastIdCreated("address")


def addAgentChangeHistory(
    conn: SqlServerConn,
    agentId: int | None,
    userId: int | None,
    dateChanged: str | None,
    changes: str | None,
) -> int:

    data = {
        "agent_id": agentId,
        "user_id": userId,
        "date_changed": dateChanged,
        "changes": changes,
    }
    conn.insertRow("agent_change_history", data)

    return conn.getLastIdCreated("agent_change_history")


def addAgent(
    conn: SqlServerConn,
    customerId: int | None,
    emailAddress: str | None,
    firstName: str | None,
    lastName: str | None,
    phoneId: int | None,
    mobilePhoneId: int | None,
    faxId: int | None,
    isSetToAutoNotifyEmail: bool | None,
    isActive: bool | None,
) -> int:
    agentRow = conn.select(
        "agent",
        "id",
        whereDetails={
            "customer_id": customerId,
            "email_address": emailAddress,
            "first_name": firstName,
            "last_name": lastName,
            "phone_id": phoneId,
            "mobile_phone_id": mobilePhoneId,
            "fax_id": faxId,
            "is_set_to_auto_notify_email": isSetToAutoNotifyEmail,
            "is_active": isActive,
        },
    )
    if agentRow:
        return agentRow[0].id

    data = {
        "customer_id": customerId,
        "email_address": emailAddress,
        "first_name": firstName,
        "last_name": lastName,
        "phone_id": phoneId,
        "mobile_phone_id": mobilePhoneId,
        "fax_id": faxId,
        "is_set_to_auto_notify_email": isSetToAutoNotifyEmail,
        "is_active": isActive,
    }
    conn.insertRow("agent", data)

    return conn.getLastIdCreated("agent")


def addAgentCertificationTest(
    conn: SqlServerConn,
    agentId: int | None,
    certificationTestId: int | None,
    dateTested: str | None,
    testScore: int | None,
    isActive: bool | None,
) -> int:
    agentCertificationTestRow = conn.select(
        "agent_certification_test",
        "id",
        whereDetails={
            "agent_id": agentId,
            "certification_test_id": certificationTestId,
            "date_tested": dateTested,
            "test_score": testScore,
            "is_active": isActive,
        },
    )
    if agentCertificationTestRow:
        return agentCertificationTestRow[0].id
    data = {
        "agent_id": agentId,
        "certification_test_id": certificationTestId,
        "date_tested": dateTested,
        "test_score": testScore,
        "is_active": isActive,
    }
    conn.insertRow("agent_certification_test", data)

    return conn.getLastIdCreated("agent_certification_test")


def addArchiveErrorLog(
    conn: SqlServerConn,
    orderId: int | None,
    archiveDate: str | None,
    userId: int | None,
    details: int | None,
) -> int:

    data = {
        "order_id": orderId,
        "archive_date": archiveDate,
        "user_id": userId,
        "details": details,
    }
    conn.insertRow("archive_error_log", data)

    return conn.getLastIdCreated("archive_error_log")


def addArchiveHistory(
    conn: SqlServerConn,
    dateArchived: str | None,
    openOrders: int | None,
    openOrderAssessorials: int | None,
    openOrderDimensions: int | None,
    openOrderDrivers: int | None,
    openOrderAttachments: int | None,
    invoicedOrders: int | None,
    invoicedOrderAssessorials: int | None,
    invoicedOrderDimensions: int | None,
    invoicedOrderDrivers: int | None,
    invoicedOrderAttachments: int | None,
    remainingOrders: int | None,
    remainingOrderAssessorials: int | None,
    remainingOrderDimensions: int | None,
    remainingOrderDrivers: int | None,
    remainingOrderAttachments: int | None,
    dockOrders: int | None,
    dockOrderAssessorials: int | None,
    dockOrderDimensions: int | None,
    dockOrderDrivers: int | None,
    dockOrderAttachments: int | None,
    serviceOrders: int | None,
    serviceOrderAssessorials: int | None,
    serviceOrderDimensions: int | None,
    serviceOrderDrivers: int | None,
    serviceOrderAttachments: int | None,
    activeOrderHistory: int | None,
    activeOrderHawbs: int | None,
    archivedOrders: int | None,
    archivedOrderAssessorials: int | None,
    archivedOrderDimensions: int | None,
    archivedOrderDrivers: int | None,
    archivedOrderAttachments: int | None,
    archivedOrderHistory: int | None,
    archivedOrderHawbs: int | None,
    removedOrders: int | None,
    removedOrderAssessorials: int | None,
    removedOrderDimensions: int | None,
    removedOrderDrivers: int | None,
    removedOrderAttachments: int | None,
    removedOrderHistory: int | None,
    removedOrderHawbs: int | None,
) -> int:
    data = {
        "date_archived": dateArchived,
        "open_orders": openOrders,
        "open_order_assessorials": openOrderAssessorials,
        "open_order_dimensions": openOrderDimensions,
        "open_order_drivers": openOrderDrivers,
        "open_order_attachments": openOrderAttachments,
        "invoiced_orders": invoicedOrders,
        "invoiced_order_assessorials": invoicedOrderAssessorials,
        "invoiced_order_dimensions": invoicedOrderDimensions,
        "invoiced_order_drivers": invoicedOrderDrivers,
        "invoiced_order_attachments": invoicedOrderAttachments,
        "remaining_orders": remainingOrders,
        "remaining_order_assessorials": remainingOrderAssessorials,
        "remaining_order_dimensions": remainingOrderDimensions,
        "remaining_order_drivers": remainingOrderDrivers,
        "remaining_order_attachments": remainingOrderAttachments,
        "dock_orders": dockOrders,
        "dock_order_assessorials": dockOrderAssessorials,
        "dock_order_dimensions": dockOrderDimensions,
        "dock_order_drivers": dockOrderDrivers,
        "dock_order_attachments": dockOrderAttachments,
        "service_orders": serviceOrders,
        "service_order_assessorials": serviceOrderAssessorials,
        "service_order_dimensions": serviceOrderDimensions,
        "service_order_drivers": serviceOrderDrivers,
        "service_order_attachments": serviceOrderAttachments,
        "active_order_history": activeOrderHistory,
        "active_order_hawbs": activeOrderHawbs,
        "archived_orders": archivedOrders,
        "archived_order_assessorials": archivedOrderAssessorials,
        "archived_order_dimensions": archivedOrderDimensions,
        "archived_order_drivers": archivedOrderDrivers,
        "archived_order_attachments": archivedOrderAttachments,
        "archived_order_history": archivedOrderHistory,
        "archived_order_hawbs": archivedOrderHawbs,
        "removed_orders": removedOrders,
        "removed_order_assessorials": removedOrderAssessorials,
        "removed_order_dimensions": removedOrderDimensions,
        "removed_order_drivers": removedOrderDrivers,
        "removed_order_attachments": removedOrderAttachments,
        "removed_order_history": removedOrderHistory,
        "removed_order_hawbs": removedOrderHawbs,
    }
    conn.insertRow("archive_history", data)

    return conn.getLastIdCreated("archive_history")


def addAssessorialChangeHistory(
    conn: SqlServerConn,
    assessorialId: int | None,
    userId: int | None,
    dateChanged: str | None,
    changes: str | None,
) -> int:

    data = {
        "assessorial_id": assessorialId,
        "user_id": userId,
        "date_changed": dateChanged,
        "changes": changes,
    }
    conn.insertRow("assessorial_change_history", data)

    return conn.getLastIdCreated("assessorial_change_history")


def addAssessorial(
    conn: SqlServerConn,
    assessorialId: int | None,
    branchId: int | None,
    assessorialName: str | None,
    minCharge: float | None,
    basisType: str,
    basisPortion: float | None,
    basisRate: float | None,
    userPrompt: str | None,
    dateCreated: str | None,
    notes: str | None,
    isActive: bool | None,
) -> int:
    assessorialRow = conn.select(
        "assessorial",
        "id",
        whereDetails={
            "branch_id": branchId,
            "assessorial_name": assessorialName,
            "min_charge": minCharge,
            "basis_type": basisType,
            "basis_portion": basisPortion,
            "basis_rate": basisRate,
            "user_prompt": userPrompt,
            "date_created": dateCreated,
            "notes": notes,
            "is_active": isActive,
        },
    )
    if assessorialRow:
        return assessorialRow[0].id
    data = {
        "branch_id": branchId,
        "assessorial_name": assessorialName,
        "min_charge": minCharge,
        "basis_type": basisType,
        "basis_portion": basisPortion,
        "basis_rate": basisRate,
        "user_prompt": userPrompt,
        "date_created": dateCreated,
        "notes": notes,
        "is_active": isActive,
    }
    conn.insertRow("assessorial", data, insertId=assessorialId)

    return conn.getLastIdCreated("assessorial")


def addBranchChangeHistory(
    conn: SqlServerConn,
    branchId: int | None,
    userId: int | None,
    dateChanged: str | None,
    changes: str | None,
) -> int:

    data = {
        "branch_id": branchId,
        "user_id": userId,
        "date_changed": dateChanged,
        "changes": changes,
    }
    conn.insertRow("branch_change_history", data)

    return conn.getLastIdCreated("branch_change_history")


def addBranch(
    conn: SqlServerConn,
    branchId: int | None,
    branchName: str | None,
    companyId: int | None,
    addressId: int | None,
    airportCode: str | None,
    email: str | None,
    phoneId: int | None,
    faxId: int | None,
    cartageAgentType: str | None,
    fuelServiceCharge: float | None,
    transferRate: float | None,
    internationalAirDimDivisor: int | None,
    domesticAirDimDivisor: int | None,
    truckDimDivisor: int | None,
    aciLow: str | None,
    aciHigh: str | None,
    notes: str | None,
    isActive: bool | None,
) -> int:
    branchRow = conn.select(
        "branch",
        "id",
        whereDetails={
            "branch_name": branchName,
            "company_id": companyId,
            "address_id": addressId,
            "airport_code": airportCode,
            "email": email,
            "phone_id": phoneId,
            "fax_id": faxId,
            "cartage_agent_type": cartageAgentType,
            "fuel_service_charge": fuelServiceCharge,
            "transfer_rate": transferRate,
            "international_air_dim_divisor": internationalAirDimDivisor,
            "domestic_air_dim_divisor": domesticAirDimDivisor,
            "truck_dim_divisor": truckDimDivisor,
            "aci_low": aciLow,
            "aci_high": aciHigh,
            "notes": notes,
            "is_active": isActive,
        },
    )
    if branchRow:
        return branchRow[0].id
    data = {
        "branch_name": branchName,
        "company_id": companyId,
        "address_id": addressId,
        "airport_code": airportCode,
        "email": email,
        "phone_id": phoneId,
        "fax_id": faxId,
        "cartage_agent_type": cartageAgentType,
        "fuel_service_charge": fuelServiceCharge,
        "transfer_rate": transferRate,
        "international_air_dim_divisor": internationalAirDimDivisor,
        "domestic_air_dim_divisor": domesticAirDimDivisor,
        "truck_dim_divisor": truckDimDivisor,
        "aci_low": aciLow,
        "aci_high": aciHigh,
        "notes": notes,
        "is_active": isActive,
    }
    conn.insertRow("branch", data, insertId=branchId)

    return conn.getLastIdCreated("branch")


def addCertificationTest(
    conn: SqlServerConn,
    certificationTestId: int | None,
    certificationName: str | None,
    certificationTestTrainerId: int | None,
    isActive: bool | None,
) -> int:
    certificationTestRow = conn.select(
        "certification_test",
        "id",
        whereDetails={
            "certification_name": certificationName,
            "certification_test_trainer_id": certificationTestTrainerId,
            "is_active": isActive,
        },
    )
    if certificationTestRow:
        return certificationTestRow[0].id

    data = {
        "certification_name": certificationName,
        "certification_test_trainer_id": certificationTestTrainerId,
        "is_active": isActive,
    }
    conn.insertRow("certification_test", data, insertId=certificationTestId)

    return conn.getLastIdCreated("certification_test")


def addCertificationTestChangeHistory(
    conn: SqlServerConn,
    certificationTestId: int | None,
    userId: int | None,
    dateChanged: str | None,
    changes: str | None,
) -> int:
    certificationTestChangeHistoryRow = conn.select(
        "certification_test_change_history",
        "id",
        whereDetails={
            "certification_test_id": certificationTestId,
            "user_id": userId,
            "date_changed": dateChanged,
            "changes": changes,
        },
    )
    if certificationTestChangeHistoryRow:
        return certificationTestChangeHistoryRow[0].id
    data = {
        "certification_test_id": certificationTestId,
        "user_id": userId,
        "date_changed": dateChanged,
        "changes": changes,
    }
    conn.insertRow("certification_test_change_history", data)

    return conn.getLastIdCreated("certification_test_change_history")


def addCertificationTestTrainer(
    conn: SqlServerConn,
    trainerName: str | None,
    isActive: bool | None,
) -> int:
    certificationTestTrainerRow = conn.select(
        "certification_test_trainer",
        "id",
        whereDetails={"trainer_name": trainerName, "is_active": isActive},
    )
    if certificationTestTrainerRow:
        return certificationTestTrainerRow[0].id

    data = {
        "trainer_name": trainerName,
        "is_active": isActive,
    }
    conn.insertRow("certification_test_trainer", data)

    return conn.getLastIdCreated("certification_test_trainer")


def addCertificationTestTrainerChangeHistory(
    conn: SqlServerConn,
    certificationTestTrainerId: int | None,
    userId: int | None,
    dateChanged: str | None,
    changes: str | None,
) -> int:
    certificationTestTrainerChangeHistoryRow = conn.select(
        "certification_test_trainer_change_history",
        "id",
        whereDetails={
            "certification_test_trainer_id": certificationTestTrainerId,
            "user_id": userId,
            "date_changed": dateChanged,
            "changes": changes,
        },
    )
    if certificationTestTrainerChangeHistoryRow:
        return certificationTestTrainerChangeHistoryRow[0].id

    data = {
        "certification_test_trainer_id": certificationTestTrainerId,
        "user_id": userId,
        "date_changed": dateChanged,
        "changes": changes,
    }
    conn.insertRow("certification_test_trainer_change_history", data)

    return conn.getLastIdCreated("certification_test_trainer_change_history")


def addCityRegion(
    conn: SqlServerConn,
    cityId: int | None,
    regionId: int | None,
) -> int:
    data = {
        "city_id": cityId,
        "region_id": regionId,
    }
    conn.insertRow("city_region", data)

    return conn.getLastIdCreated("city_region")


def addCityPostalCode(
    conn: SqlServerConn,
    cityName: str | None,
    postalCode: str | None,
    regionDetails: dict[str, str],
    countryDetails: dict[str, str],
) -> tuple[int | None, int | None]:

    if not cityName or not postalCode or not regionDetails or not countryDetails:
        return (None, None)

    cityName = cityName.lower()
    postalCode = postalCode.lower()

    regionId = addRegion(conn, regionDetails, countryDetails)

    if regionId == None:
        return (None, None)

    cityRow = conn.select(
        "[city] INNER JOIN [city_region] ON [city].[id] = [city_region].[city_id]",
        "[city].[id] AS selected_city_id",
        f"[city].[city_name] = '{cityName}' AND [city_region].[region_id] = {regionId}",
    )
    postalCodeRow = conn.select(
        "postal_code INNER JOIN postal_code_region ON [postal_code].id = [postal_code_region].[postal_code_id]",
        "[postal_code].[id] AS selected_postal_code_id",
        f"[postal_code].[postal_code] = '{postalCode}' AND [postal_code_region].[region_id] = '{regionId}'",
    )
    if cityRow:
        cityId = cityRow[0].selected_city_id
    else:
        cityData = {"city_name": cityName}
        conn.insertRow("city", cityData)

        cityId = conn.getLastIdCreated("city")
    if postalCodeRow:
        postalCodeId = postalCodeRow[0].selected_postal_code_id
    else:
        postalCodeData = {"postal_code": postalCode}
        conn.insertRow("postal_code", postalCodeData)

        postalCodeId = conn.getLastIdCreated("postal_code")

    if cityRow and postalCodeRow:
        return (cityId, postalCodeId)

    cityRegionData = {"city_id": cityId, "region_id": regionId}
    conn.insertRow("city_region", cityRegionData)

    postalCodeRegionData = {"postal_code_id": postalCodeId, "region_id": regionId}
    conn.insertRow("postal_code_region", postalCodeRegionData)

    cityPostalCodeData = {
        "city_id": cityId,
        "postal_code_id": postalCodeId,
        "lat": getCityLat(cityName=cityName, postalCode=postalCode),
        "lng": getCityLat(cityName=cityName, postalCode=postalCode),
    }
    conn.insertRow("city_postal_code", cityPostalCodeData)

    return (cityId, postalCodeId)


def addCompanyChangeHistory(
    conn: SqlServerConn,
    companyId: int | None,
    userId: int | None,
    dateChanged: str | None,
    changes: str | None,
) -> int:

    data = {
        "company_id": companyId,
        "user_id": userId,
        "date_changed": dateChanged,
        "changes": changes,
    }
    conn.insertRow("company_change_history", data)

    return conn.getLastIdCreated("company_change_history")


def addCompany(
    conn: SqlServerConn,
    companyId: int | None,
    companyName: str | None,
    addressId: int | None,
    phoneId: int | None,
    airportCode: str | None,
    faxId: int | None,
    cartageAgentType: str | None,
    employerIdentificationNo: str | None,
    email: str | None,
    scac: str | None,
    website: str | None,
    notes: str | None,
    logoPath: str | None,
    isTsaCompliant: bool | None,
    isActive: bool | None,
) -> int:
    data = {
        "company_name": companyName,
        "address_id": addressId,
        "phone_id": phoneId,
        "airport_code": airportCode,
        "fax_id": faxId,
        "cartage_agent_type": cartageAgentType,
        "employer_identification_no": employerIdentificationNo,
        "email": email,
        "scac": scac,
        "website": website,
        "notes": notes,
        "logo_path": logoPath,
        "is_tsa_compliant": isTsaCompliant,
        "is_active": isActive,
    }
    conn.insertRow("company", data, insertId=companyId)

    return conn.getLastIdCreated("company")


def addCountry(
    conn: SqlServerConn, countryDetails: dict[str, str]
) -> int | None:
    if not countryDetails:
        return None
    if "countryName" in countryDetails:
        countryName = countryDetails["countryName"].lower().strip()
        if not countryName:
            return None
        countryRow = conn.select("country", "id", f"[country_name] = '{countryName}'")
        if countryRow:
            return countryRow[0].id
        data = {
            "iso_code_2": countryGet(name=countryName)[0]["alpha_2"].lower(),
            "iso_code_3": countryGet(name=countryName)[0]["alpha_3"].lower(),
            "country_name": countryName,
        }
    elif "isoCode2" in countryDetails:
        isoCode2 = countryDetails["isoCode2"].lower().strip()
        if not isoCode2:
            return None
        countryRow = conn.select("country", "id", f"[iso_code_2] = '{isoCode2}'")
        if countryRow:
            return countryRow[0].id
        print(f'IsoCode2 : {isoCode2}')
        data = {
            "iso_code_2": isoCode2,
            "iso_code_3": countryGet(alpha_2=isoCode2)[0]["alpha_3"].lower(),
            "country_name": countryGet(alpha_2=isoCode2)[0]["name"].lower(),
        }
    elif "isoCode3" in countryDetails:
        isoCode3 = countryDetails["isoCode3"].lower().strip()
        if not isoCode3:
            return None
        countryRow = conn.select("country", "id", f"[iso_code_3] = '{isoCode3}'")
        if countryRow:
            return countryRow[0].id
        print(f'IsoCode3 : {isoCode3}')
        data = {
            "iso_code_2": countryGet(alpha_3=isoCode3)[0]["alpha_2"].lower(),
            "iso_code_3": isoCode3,
            "country_name": countryGet(alpha_3=isoCode3)[0]["name"].lower(),
        }
    elif "default" in countryDetails:
        countryRow = conn.select("country", "id", f"[iso_code_2] = 'us'")
        if countryRow:
            return countryRow[0].id
        data = {
            "iso_code_2": "us",
            "iso_code_3": "usa",
            "country_name": "united states",
        }

    conn.insertRow("country", data)

    return conn.getLastIdCreated("country")


def addCustomerChangeHistory(
    conn: SqlServerConn,
    customerId: int | None,
    userId: int | None,
    dateChanged: str | None,
    changes: str | None,
) -> int:

    data = {
        "customer_id": customerId,
        "user_id": userId,
        "date_changed": dateChanged,
        "changes": changes,
    }
    conn.insertRow("customer_change_history", data)

    return conn.getLastIdCreated("customer_change_history")


def addCustomerDefaultAssessorial(
    conn: SqlServerConn,
    customerId: int | None,
    assessorialId: int | None,
) -> int:
    customerDefaultAssessorialRow = conn.select(
        "customer_default_assessorial",
        "id",
        whereDetails={"customer_id": customerId, "assessorial_id": assessorialId},
    )
    if customerDefaultAssessorialRow:
        return customerDefaultAssessorialRow[0].id

    data = {
        "customer_id": customerId,
        "assessorial_id": assessorialId,
    }
    conn.insertRow("customer_default_assessorial", data)

    return conn.getLastIdCreated("customer_default_assessorial")


def addCustomer(
    conn: SqlServerConn,
    customerId: int | None,
    branchId: int | None,
    customerName: str | None,
    addressId: int | None,
    phoneId: int | None,
    defaultRateId: int | None,
    fuelServiceCharge: float | None,
    qbCustomerRefId: str | None,
    qbCustomerRefName: str | None,
    isQbInvoiceOmitted: bool | None,
    isActive: bool | None,
    notes: bool | None,
) -> int:
    customerRow = conn.select(
        "customer",
        "id",
        whereDetails={
            "branch_id": branchId,
            "customer_name": customerName,
            "address_id": addressId,
            "phone_id": phoneId,
            "default_rate_id": defaultRateId,
            "fuel_service_charge": fuelServiceCharge,
            "qb_customer_ref_id": qbCustomerRefId,
            "qb_customer_ref_name": qbCustomerRefName,
            "is_qb_invoice_omitted": isQbInvoiceOmitted,
            "is_active": isActive,
            "notes": notes,
        },
    )
    if customerRow:
        return customerRow[0].id

    data = {
        "branch_id": branchId,
        "customer_name": customerName,
        "address_id": addressId,
        "phone_id": phoneId,
        "default_rate_id": defaultRateId,
        "fuel_service_charge": fuelServiceCharge,
        "qb_customer_ref_id": qbCustomerRefId,
        "qb_customer_ref_name": qbCustomerRefName,
        "is_qb_invoice_omitted": isQbInvoiceOmitted,
        "is_active": isActive,
        "notes": notes,
    }
    conn.insertRow("customer", data, insertId=customerId)

    return conn.getLastIdCreated("customer")


def addFax(
    conn: SqlServerConn,
    countryCode: str | None,
    areaCode: str | None,
    faxNumber: str | None,
    faxExtension: str | None,
) -> int | None:
    if areaCode == "" or faxNumber == "":
        return None

    faxRow = conn.select(
        "fax",
        "id",
        whereDetails={
            "country_code": countryCode,
            "area_code": areaCode,
            "fax_number": faxNumber,
            "fax_extension": faxNumber,
        },
    )
    if faxRow:
        return faxRow[0].id
    data = {
        "country_code": countryCode,
        "area_code": areaCode,
        "fax_number": faxNumber,
        "fax_extension": faxExtension,
    }
    conn.insertRow("fax", data)

    return conn.getLastIdCreated("fax")


def addHoliday(
    conn: SqlServerConn,
    holidayName: str,
    holidayDate: str,
) -> int:
    holidayRow = conn.select(
        "holiday",
        "id",
        whereDetails={
            "holiday_name": "".join(["''" if x == "'" else x for x in holidayName]),
            "holiday_date": holidayDate,
        },
    )
    if holidayRow:
        return holidayRow[0].id

    data = {
        "holiday_name": holidayName,
        "holiday_date": holidayDate,
    }
    conn.insertRow("holiday", data)

    return conn.getLastIdCreated("holiday")


def addLocationChangeHistory(
    conn: SqlServerConn,
    locationId: int | None,
    userId: int | None,
    dateChanged: str | None,
    changes: str | None,
) -> int:

    data = {
        "location_id": locationId,
        "user_id": userId,
        "date_changed": dateChanged,
        "changes": changes,
    }
    conn.insertRow("location_change_history", data)

    return conn.getLastIdCreated("location_change_history")


def addLocationDefaultAssessorial(
    conn: SqlServerConn,
    locationId: int | None,
    assessorialId: int | None,
) -> int:
    locationDefaultAssessorialRow = conn.select(
        "location_default_assessorial",
        "id",
        whereDetails={"location_id": locationId, "assessorial_id": assessorialId},
    )
    if locationDefaultAssessorialRow:
        return locationDefaultAssessorialRow[0].id

    data = {
        "location_id": locationId,
        "assessorial_id": assessorialId,
    }
    conn.insertRow("location_default_assessorial", data)

    return conn.getLastIdCreated("location_default_assessorial")


def addLocation(
    conn: SqlServerConn,
    locationId: int | None,
    branchId: int | None,
    companyName: str | None,
    locationName: str | None,
    addressId: int | None,
    aciId: int | None,
    contactFirstName: str | None,
    contactLastName: str | None,
    contactEmail: str | None,
    contactPhoneId: int | None,
    isCarrier: bool | None,
    isLocal: bool | None,
    isInternational: bool | None,
    defaultWaitTime: int | None,
    isActive: bool | None,
) -> int:
    locationRow = conn.select(
        "location",
        "id",
        whereDetails={
            "branch_id": branchId,
            "company_name": companyName,
            "location_name": locationName,
            "address_id": addressId,
            "aci_id": aciId,
            "contact_first_name": contactFirstName,
            "contact_last_name": contactLastName,
            "contact_email": contactEmail,
            "contact_phone_id": contactPhoneId,
            "is_carrier": isCarrier,
            "is_local": isLocal,
            "is_international": isInternational,
            "default_wait_time": defaultWaitTime,
            "is_active": isActive,
        },
    )
    if locationRow:
        return locationRow[0].id

    data = {
        "branch_id": branchId,
        "company_name": companyName,
        "location_name": locationName,
        "address_id": addressId,
        "aci_id": aciId,
        "contact_first_name": contactFirstName,
        "contact_last_name": contactLastName,
        "contact_email": contactEmail,
        "contact_phone_id": contactPhoneId,
        "is_carrier": isCarrier,
        "is_local": isLocal,
        "is_international": isInternational,
        "default_wait_time": defaultWaitTime,
        "is_active": isActive,
    }
    conn.insertRow("location", data, insertId=locationId)

    return conn.getLastIdCreated("location")


def addOrderAssessorial(
    conn: SqlServerConn,
    orderId: int | None,
    assessorialId: int | None,
    parentType: str | None,
    basisCount: float | None,
    totalCharge: float | None,
) -> int:
    orderAssessorialRow = conn.select(
        "order_assessorial",
        "id",
        whereDetails={
            "order_id": orderId,
            "assessorial_id": assessorialId,
            "parent_type": parentType,
            "basis_count": basisCount,
            "total_charge": totalCharge,
        },
    )
    if orderAssessorialRow:
        return orderAssessorialRow[0].id

    data = {
        "order_id": orderId,
        "assessorial_id": assessorialId,
        "parent_type": parentType,
        "basis_count": basisCount,
        "total_charge": totalCharge,
    }
    conn.insertRow("order_assessorial", data)

    return conn.getLastIdCreated("order_assessorial")


def addOrderAttachment(
    conn: SqlServerConn,
    orderId: int | None,
    attachmentPath: str | None,
    fileSize: float | None,
) -> int:
    orderAttachmentRow = conn.select(
        "order_attachment",
        "id",
        whereDetails={
            "order_id": orderId,
            "attachment_path": attachmentPath,
            "file_size": fileSize,
        },
    )
    if orderAttachmentRow:
        return orderAttachmentRow[0].id
    data = {
        "order_id": orderId,
        "attachment_path": attachmentPath,
        "file_size": fileSize,
    }
    conn.insertRow("order_attachment", data)

    return conn.getLastIdCreated("order_attachment")


def addOrderChangeHistory(
    conn: SqlServerConn,
    orderId: int | None,
    userId: int | None,
    dateChanged: str | None,
    changes: str | None,
) -> int:
    data = {
        "order_id": orderId,
        "user_id": userId,
        "date_changed": dateChanged,
        "changes": changes,
    }
    conn.insertRow("order_change_history", data)

    return conn.getLastIdCreated("order_change_history")


def addOrderDim(
    conn: SqlServerConn,
    orderId: int | None,
    unitType: str | None,
    unitQuantity: int | None,
    unitWeight: int | None,
    dimHeight: int | None,
    dimWidth: int | None,
    dimLength: int | None,
    dimWeight: float | None,
) -> int:
    orderDimRow = conn.select(
        "order_dim",
        "id",
        whereDetails={
            "order_id": orderId,
            "unit_type": unitType,
            "unit_quantity": unitQuantity,
            "unit_weight": unitWeight,
            "dim_height": dimHeight,
            "dim_width": dimWidth,
            "dim_length": dimLength,
            "dim_weight": dimWeight,
        },
    )
    if orderDimRow:
        return orderDimRow[0].id

    data = {
        "order_id": orderId,
        "unit_type": unitType,
        "unit_quantity": unitQuantity,
        "unit_weight": unitWeight,
        "dim_height": dimHeight,
        "dim_width": dimWidth,
        "dim_length": dimLength,
        "dim_weight": dimWeight,
    }
    conn.insertRow("order_dim", data)

    return conn.getLastIdCreated("order_dim")


def addOrderDriver(
    conn: SqlServerConn,
    orderId: int | None,
    driverUserId: int | None,
    orderLeg: str | None,
    driverRole: str | None,
) -> int:
    orderDriverRow = conn.select(
        "order_driver",
        "id",
        whereDetails={
            "order_id": orderId,
            "driver_user_id": driverUserId,
            "order_leg": orderLeg,
            "driver_role": driverRole,
        },
    )
    if orderDriverRow:
        return orderDriverRow[0].id

    data = {
        "order_id": orderId,
        "order_leg": orderLeg,
        "driver_role": driverRole,
    }
    conn.insertRow("order_driver", data)

    return conn.getLastIdCreated("order_driver")


def addOrderStatusChangeHistory(
    conn: SqlServerConn,
    orderStatusId: int | None,
    userId: int | None,
    dateChanged: str | None,
    changes: str | None,
) -> int:

    data = {
        "order_status_id": orderStatusId,
        "user_id": userId,
        "date_changed": dateChanged,
        "changes": changes,
    }
    conn.insertRow("order_status_change_history", data)

    return conn.getLastIdCreated("order_status_change_history")


def addOrderStatus(
    conn: SqlServerConn,
    orderStatusId: int | None,
    sequenceNumber: int | None,
    orderStatusName: str | None,
    isOnManifest: bool | None,
    isSetToAutoNotify: bool | None,
    isActive: bool | None,
    branchId: int | None,
) -> int:
    orderStatusRow = conn.select(
        "order_status",
        "id",
        whereDetails={
            "order_status_name": orderStatusName,
            "is_on_manifest": isOnManifest,
            "is_set_to_auto_notify": isSetToAutoNotify,
            "is_active": isActive,
            "branch_id": branchId,
        },
    )
    if orderStatusRow:
        return orderStatusRow[0].id
    data = {
        "order_status_name": orderStatusName,
        "is_on_manifest": isOnManifest,
        "sequence_number": sequenceNumber,
        "is_set_to_auto_notify": isSetToAutoNotify,
        "is_active": isActive,
        "branch_id": branchId,
    }
    conn.insertRow("order_status", data, insertId=orderStatusId)

    return conn.getLastIdCreated("order_status")


def addOrderType(
    conn: SqlServerConn,
    orderTypeId: int | None,
    orderTypeName: str | None,
) -> int:
    orderTypeRow = conn.select(
        "order_type", "id", whereDetails={"order_type_name": orderTypeName}
    )
    if orderTypeRow:
        return orderTypeRow[0].id

    data = {
        "order_type_name": orderTypeName,
    }
    conn.insertRow("order_type", data, insertId=orderTypeId)

    return conn.getLastIdCreated("order_type")


def addOrder(
    conn: SqlServerConn,
    orderId: int | None,
    branchId: int | None,
    orderTypeId: int | None,
    customerId: int | None,
    agentId: int | None,
    rateId: int | None,
    hawb: str | None,
    mawb: str | None,
    orderNotes: str | None,
    puTimeStart: str | None,
    puTimeEnd: str | None,
    delTimeStart: str | None,
    delTimeEnd: str | None,
    puLocationId: int | None,
    puNotes: str | None,
    delLocationId: int | None,
    delNotes: str | None,
    driverName: str | None,
    podSignee: str | None,
    podTimeSigned: str | None,
    podNotes: str | None,
    statusId: int | None,
    ratingWeightCharges: float | None,
    ratingFuelCharges: float | None,
    ratingServiceCharges: float | None,
    ratingTotalCharges: float | None,
    ratingTotalExpenses: float | None,
    ratingStorageCharges: float | None,
    ratingAdjustments: float | None,
    ratingNotes: float | None,
    quickbooksCustomerListId: str | None,
    quickbooksCustomerName: str | None,
    quickbooksInvoiceReferenceNumber: str | None,
    quickbooksLineSequenceNumber: str | None,
    isAutoAssessorials: bool | None,
    isWeightChargeCalculated: bool | None,
) -> int:

    data = {
        "branch_id": branchId,
        "order_type_id": orderTypeId,
        "customer_id": customerId,
        "agent_id": agentId,
        "rate_id": rateId,
        "hawb": hawb,
        "mawb": mawb,
        "order_notes": orderNotes,
        "pu_time_start": puTimeStart,
        "pu_time_end": puTimeEnd,
        "del_time_start": delTimeStart,
        "del_time_end": delTimeEnd,
        "pu_location_id": puLocationId,
        "pu_notes": puNotes,
        "del_location_id": delLocationId,
        "del_notes": delNotes,
        "driver_name": driverName,
        "pod_signee": podSignee,
        "pod_time_signed": podTimeSigned,
        "pod_notes": podNotes,
        "status_id": statusId,
        "rating_weight_charges": ratingWeightCharges,
        "rating_fuel_charges": ratingFuelCharges,
        "rating_service_charges": ratingServiceCharges,
        "rating_total_charges": ratingTotalCharges,
        "rating_total_expenses": ratingTotalExpenses,
        "rating_storage_charges": ratingStorageCharges,
        "rating_adjustments": ratingAdjustments,
        "rating_notes": ratingNotes,
        "quickbooks_customer_list_id": quickbooksCustomerListId,
        "quickbooks_customer_name": quickbooksCustomerName,
        "quickbooks_invoice_reference_number": quickbooksInvoiceReferenceNumber,
        "quickbooks_line_sequence_number": quickbooksLineSequenceNumber,
        "is_auto_assessorials": isAutoAssessorials,
        "is_weight_charge_calculated": isWeightChargeCalculated,
    }
    conn.insertRow("order", data, insertId=orderId)

    return conn.getLastIdCreated("order")


def addOvernightMaintenanceHistory(
    conn: SqlServerConn,
    dateOvernightMaintenance: str | None,
    userId: int | None,
    openOrdersIn: int | None,
    openOrderAssessorialsIn: int | None,
    openOrderDimensionsIn: int | None,
    openOrderDriversIn: int | None,
    openOrderAttachmentsIn: int | None,
    invoicedOrdersIn: int | None,
    invoicedOrderAssessorialsIn: int | None,
    invoicedOrderDimensionsIn: int | None,
    invoicedOrderDriversIn: int | None,
    invoicedOrderAttachmentsIn: int | None,
    remainingOrdersIn: int | None,
    remainingOrderAssessorialsIn: int | None,
    remainingOrderDimensionsIn: int | None,
    remainingOrderDriversIn: int | None,
    remainingOrderAttachmentsIn: int | None,
    openOrdersOut: int | None,
    openOrderAssessorialsOut: int | None,
    openOrderDimensionsOut: int | None,
    openOrderDriversOut: int | None,
    openOrderAttachmentsOut: int | None,
    invoicedOrdersOut: int | None,
    invoicedOrderAssessorialsOut: int | None,
    invoicedOrderDimensionsOut: int | None,
    invoicedOrderDriversOut: int | None,
    invoicedOrderAttachmentsOut: int | None,
    remainingOrdersOut: int | None,
    remainingOrderAssessorialsOut: int | None,
    remainingOrderDimensionsOut: int | None,
    remainingOrderDriversOut: int | None,
    remainingOrderAttachmentsOut: int | None,
) -> int:

    data = {
        "date_overnight_maintenance": dateOvernightMaintenance,
        "user_id": userId,
        "open_orders_in": openOrdersIn,
        "open_order_assessorials_in": openOrderAssessorialsIn,
        "open_order_dimensions_in": openOrderDimensionsIn,
        "open_order_drivers_in": openOrderDriversIn,
        "open_order_attachments_in": openOrderAttachmentsIn,
        "invoiced_orders_in": invoicedOrdersIn,
        "invoiced_order_assessorials_in": invoicedOrderAssessorialsIn,
        "invoiced_order_dimensions_in": invoicedOrderDimensionsIn,
        "invoiced_order_drivers_in": invoicedOrderDriversIn,
        "invoiced_order_attachments_in": invoicedOrderAttachmentsIn,
        "remaining_orders_in": remainingOrdersIn,
        "remaining_order_assessorials_in": remainingOrderAssessorialsIn,
        "remaining_order_dimensions_in": remainingOrderDimensionsIn,
        "remaining_order_drivers_in": remainingOrderDriversIn,
        "remaining_order_attachments_in": remainingOrderAttachmentsIn,
        "open_orders_out": openOrdersOut,
        "open_order_assessorials_out": openOrderAssessorialsOut,
        "open_order_dimensions_out": openOrderDimensionsOut,
        "open_order_drivers_out": openOrderDriversOut,
        "open_order_attachments_out": openOrderAttachmentsOut,
        "invoiced_orders_out": invoicedOrdersOut,
        "invoiced_order_assessorials_out": invoicedOrderAssessorialsOut,
        "invoiced_order_dimensions_out": invoicedOrderDimensionsOut,
        "invoiced_order_drivers_out": invoicedOrderDriversOut,
        "invoiced_order_attachments_out": invoicedOrderAttachmentsOut,
        "remaining_orders_out": remainingOrdersOut,
        "remaining_order_assessorials_out": remainingOrderAssessorialsOut,
        "remaining_order_dimensions_out": remainingOrderDimensionsOut,
        "remaining_order_drivers_out": remainingOrderDriversOut,
        "remaining_order_attachments_out": remainingOrderAttachmentsOut,
    }
    conn.insertRow("overnight_maintenance_history", data)

    return conn.getLastIdCreated("overnight_maintenance_history")


def addPhone(
    conn: SqlServerConn,
    countryCode: str | None,
    areaCode: str | None,
    phoneNumber: str | None,
    phoneExtension: str | None,
) -> int | None:
    if areaCode == "" or phoneNumber == "":
        return None

    phoneRow = conn.select(
        "phone",
        "id",
        whereDetails={
            "country_code": countryCode,
            "area_code": areaCode,
            "phone_number": phoneNumber,
            "phone_extension": phoneExtension,
        },
    )
    if phoneRow:
        return phoneRow[0].id
    data = {
        "country_code": countryCode,
        "area_code": areaCode,
        "phone_number": phoneNumber,
        "phone_extension": phoneExtension,
    }
    conn.insertRow("phone", data)

    return conn.getLastIdCreated("phone")


def addPositionChangeHistory(
    conn: SqlServerConn,
    positionId: int | None,
    userId: int | None,
    dateChanged: str | None,
    changes: str | None,
) -> int:

    data = {
        "position_id": positionId,
        "user_id": userId,
        "date_changed": dateChanged,
        "changes": changes,
    }
    conn.insertRow("position_change_history", data)

    return conn.getLastIdCreated("position_change_history")


def addPosition(
    conn: SqlServerConn,
    positionId: int | None,
    positionName: str | None,
    securityLevel: int | None,
    isActive: bool | None,
    branchId: int | None,
) -> int:
    positionRow = conn.select(
        "position",
        "id",
        whereDetails={
            "position_name": positionName,
            "security_level": securityLevel,
            "is_active": isActive,
            "branch_id": branchId,
        },
    )
    if positionRow:
        return positionRow[0].id
    data = {
        "position_name": positionName,
        "security_level": securityLevel,
        "is_active": isActive,
        "branch_id": branchId,
    }
    conn.insertRow("position", data, insertId=positionId)

    return conn.getLastIdCreated("position")


def addPostalCodeRegion(
    conn: SqlServerConn,
    postalCodeId: int | None,
    regionId: int | None,
) -> int:
    data = {
        "postal_code_id": postalCodeId,
        "region_id": regionId,
    }
    conn.insertRow("postal_code_region", data)

    return conn.getLastIdCreated("postal_code_region")


def addRateArea(
    conn: SqlServerConn,
    rateId: int | None,
    area: str | None,
    rateMin: float | None,
    rate100: float | None,
    rate1000: float | None,
    rate2000: float | None,
    rate5000: float | None,
    rateMax: float | None,
) -> int:
    rateAreaRow = conn.select(
        "rate_area",
        "id",
        whereDetails={
            "rate_id": rateId,
            "area": area,
            "rate_min": rateMin,
            "rate_100": rate100,
            "rate_1000": rate1000,
            "rate_2000": rate2000,
            "rate_5000": rate5000,
            "rate_max": rateMax,
        },
    )
    if rateAreaRow:
        return rateAreaRow[0].id

    data = {
        "rate_id": rateId,
        "area": area,
        "rate_min": rateMin,
        "rate_100": rate100,
        "rate_1000": rate1000,
        "rate_2000": rate2000,
        "rate_5000": rate5000,
        "rate_max": rateMax,
    }
    conn.insertRow("rate_area", data)

    return conn.getLastIdCreated("rate_area")


def addRateChangeHistory(
    conn: SqlServerConn,
    rateId: int | None,
    userId: int | None,
    dateChanged: str | None,
    changes: str | None,
) -> int:

    data = {
        "rate_id": rateId,
        "user_id": userId,
        "date_changed": dateChanged,
        "changes": changes,
    }
    conn.insertRow("rate_change_history", data)

    return conn.getLastIdCreated("rate_change_history")


def addRate(
    conn: SqlServerConn,
    rateId: int | None,
    rateName: str | None,
    branchId: int | None,
    isDefault: bool | None,
    isActive: bool | None,
    dateAdded: str | None,
    addedByUserId: int | None,
) -> int:
    rateRow = conn.select(
        "rate",
        "id",
        whereDetails={
            "rate_name": rateName,
            "branch_id": branchId,
            "is_default": isDefault,
            "is_active": isActive,
            "date_added": dateAdded,
            "added_by_user_id": addedByUserId,
        },
    )
    if rateRow:
        return rateRow[0].id

    data = {
        "rate_name": rateName,
        "branch_id": branchId,
        "is_default": isDefault,
        "is_active": isActive,
        "date_added": dateAdded,
        "added_by_user_id": addedByUserId,
    }
    conn.insertRow("rate", data, insertId=rateId)

    return conn.getLastIdCreated("rate")


def addRegion(
    conn: SqlServerConn,
    regionDetails: dict[str, str],
    countryDetails: dict[str, str],
) -> int | None:
    if not regionDetails or not countryDetails:
        return None

    countryId = addCountry(conn, countryDetails=countryDetails)
    countrySelectInfo = conn.select("country", "iso_code_2", f"[id] = '{countryId}'")
    if not countrySelectInfo == None:
        countryIsoCode = countrySelectInfo[0].iso_code_2

    if "regionName" in regionDetails:
        regionName = regionDetails["regionName"].lower().strip()

        if not regionName:
            return None
        regionRow = conn.select(
            "region",
            "id",
            f"[region_name] = '{regionName}' AND [country_id] = {countryId}",
        )
        if regionRow:
            return regionRow[0].id

        for region in regionGet(name=regionName):
            if region["code"][0:1].lower() == countryIsoCode:
                correctRegion = region
                break
        data = {
            "region_name": regionName,
            "iso_code": correctRegion["name"][3:].lower(),
            "country_id": countryId,
        }
    elif "isoCode" in regionDetails:
        isoCode = regionDetails["isoCode"].lower().strip()
        if not isoCode:
            return None
        regionRow = conn.select(
            "region", "id", f"[iso_code] = '{isoCode}' AND [country_id] = '{countryId}'"
        )
        if regionRow:
            return regionRow[0].id
        data = {
            "region_name": regionGet(code=f"{countryIsoCode}-{isoCode}".upper())[0][
                "name"
            ].lower(),
            "iso_code": isoCode,
            "country_id": countryId,
        }

    conn.insertRow("region", data)

    return conn.getLastIdCreated("region")


def addSpecialChangeHistory(
    conn: SqlServerConn,
    specialId: int | None,
    userId: int | None,
    dateChanged: str | None,
    changes: str | None,
) -> int:

    data = {
        "special_id": specialId,
        "user_id": userId,
        "date_changed": dateChanged,
        "changes": changes,
    }
    conn.insertRow("special_change_history", data)

    return conn.getLastIdCreated("special_change_history")


def addSpecial(
    conn: SqlServerConn,
    oldId: int | None,
    branchId: int | None,
    weekday: int | None,
    startTime: int | None,
    endTime: int | None,
    area: str | None,
    isActive: bool | None,
) -> int:
    specialRow = conn.select(
        "special",
        "id",
        whereDetails={
            "old_id": oldId,
            "branch_id": branchId,
            "weekday": weekday,
            "start_time": startTime,
            "end_time": endTime,
            "area": area,
            "is_active": isActive,
        },
    )
    if specialRow:
        return specialRow[0].id

    data = {
        "old_id": oldId,
        "branch_id": branchId,
        "weekday": weekday,
        "start_time": startTime,
        "end_time": endTime,
        "area": area,
        "is_active": isActive,
    }
    conn.insertRow("special", data)

    return conn.getLastIdCreated("special")


def addUserChangeHistory(
    conn: SqlServerConn,
    userChangedId: int | None,
    userId: int | None,
    dateChanged: str | None,
    changes: str | None,
) -> int:

    data = {
        "user_changed_id": userChangedId,
        "user_id": userId,
        "date_changed": dateChanged,
        "changes": changes,
    }
    conn.insertRow("user_change_history", data)

    return conn.getLastIdCreated("user_change_history")


def addUser(
    conn: SqlServerConn,
    userId: int | None,
    username: str | None,
    email: str | None,
    passwordHash: str | None,
    passwordSalt: str | None,
    namePrefix: str | None,
    firstName: str | None,
    lastName: str | None,
    nameSuffix: str | None,
    addressId: int | None,
    branchId: int | None,
    commissionRate: float | None,
    dateHired: str | None,
    dateTerminated: str | None,
    phoneMainId: int | None,
    phoneHomeId: int | None,
    phoneMobileId: int | None,
    positionId: int | None,
    tsaNumber: str | None,
    tsaType: str | None,
    tsaTaken: str | None,
    isActive: bool | None,
    isDefaultDocOwner: bool | None,
    isSecurityCoordinator: bool | None,
    isTsaTrainer: bool | None,
) -> int:
    userRow = conn.select(
        "user",
        "id",
        whereDetails={
            "username": username,
            "email": email,
            "password_hash": passwordHash,
            "password_salt": passwordSalt,
            "name_prefix": namePrefix,
            "first_name": firstName,
            "last_name": lastName,
            "name_suffix": nameSuffix,
            "address_id": addressId,
            "branch_id": branchId,
            "commission_rate": commissionRate,
            "date_hired": dateHired,
            "date_terminated": dateTerminated,
            "phone_main_id": phoneMainId,
            "phone_home_id": phoneHomeId,
            "phone_mobile_id": phoneMobileId,
            "position_id": positionId,
            "tsa_number": tsaNumber,
            "tsa_type": tsaType,
            "tsa_taken": tsaTaken,
            "is_active": isActive,
            "is_default_doc_owner": isDefaultDocOwner,
            "is_security_coordinator": isSecurityCoordinator,
            "is_tsa_trainer": isTsaTrainer,
        },
    )
    if userRow:
        return userRow[0].id
    data = {
        "username": username,
        "email": email,
        "password_hash": passwordHash,
        "password_salt": passwordSalt,
        "name_prefix": namePrefix,
        "first_name": firstName,
        "last_name": lastName,
        "name_suffix": nameSuffix,
        "address_id": addressId,
        "branch_id": branchId,
        "commission_rate": commissionRate,
        "date_hired": dateHired,
        "date_terminated": dateTerminated,
        "phone_main_id": phoneMainId,
        "phone_home_id": phoneHomeId,
        "phone_mobile_id": phoneMobileId,
        "position_id": positionId,
        "tsa_number": tsaNumber,
        "tsa_type": tsaType,
        "tsa_taken": tsaTaken,
        "is_active": isActive,
        "is_default_doc_owner": isDefaultDocOwner,
        "is_security_coordinator": isSecurityCoordinator,
        "is_tsa_trainer": isTsaTrainer,
    }
    conn.insertRow("user", data, insertId=userId)

    return conn.getLastIdCreated("user")
