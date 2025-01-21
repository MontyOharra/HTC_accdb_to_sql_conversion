from typing import List
from src.types.types import ForeignKey

aciDataChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('aci_data_change_history', 'aci_data_id', 'aci_data', 'id'),
    ForeignKey('aci_data_change_history', 'user_id', 'user', 'id'),
]

aciDataForeignKeys: List[ForeignKey] = [
    ForeignKey('aci_data', 'city_id', 'city', 'id'),
    ForeignKey('aci_data', 'postal_code_id', 'postal_code', 'id'),
    ForeignKey('aci_data', 'created_by', 'user', 'id'),
    ForeignKey('aci_data', 'branch_id', 'branch', 'id'),
]

addressForeignKeys: List[ForeignKey] = [
    ForeignKey('address', 'city_id', 'city', 'id'),
    ForeignKey('address', 'postal_code_id', 'postal_code', 'id'),
]

agentForeignKeys: List[ForeignKey] = [
    ForeignKey('agent', 'customer_id', 'customer', 'id'),
    ForeignKey('agent', 'phone_id', 'phone', 'id'),
    ForeignKey('agent', 'mobile_phone_id', 'phone', 'id'),
    ForeignKey('agent', 'fax_id', 'fax', 'id'),
]

agentChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('agent_change_history', 'agent_id', 'agent', 'id'),
    ForeignKey('agent_change_history', 'user_id', 'user', 'id'),
]

agentCertificationTestForeignKeys: List[ForeignKey] = [
    ForeignKey('agent_certification_test', 'agent_id', 'agent', 'id'),
    ForeignKey('agent_certification_test', 'certification_test_id', 'certification_test', 'id'),
]

archiveErrorLogForeignKeys: List[ForeignKey] = [
    ForeignKey('archive_error_log', 'order_id', 'order', 'id'),
    ForeignKey('archive_error_log', 'user_id', 'user', 'id'),
]

archiveHistoryForeignKeys: List[ForeignKey] = [
  
]

assessorialChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('assessorial_change_history', 'assessorial_id', 'assessorial', 'id'),
    ForeignKey('assessorial_change_history', 'user_id', 'user', 'id'),
]

assessorialForeignKeys: List[ForeignKey] = [
    ForeignKey('assessorial', 'branch_id', 'branch', 'id'),
]

branchChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('branch_change_history', 'branch_id', 'branch', 'id'),
    ForeignKey('branch_change_history', 'user_id', 'user', 'id'),
]

branchForeignKeys: List[ForeignKey] = [
    ForeignKey('branch', 'company_id', 'company', 'id'),
    ForeignKey('branch', 'phone_id', 'phone', 'id'),
    ForeignKey('branch', 'fax_id', 'fax', 'id'),
]

certificationTestForeignKeys: List[ForeignKey] = [
    ForeignKey('certification_test', 'certification_test_trainer_id', 'certification_test_trainer', 'id'),
]

certificationTestChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('certification_test_change_history', 'certification_test_id', 'certification_test', 'id'),
    ForeignKey('certification_test_change_history', 'user_id', 'user', 'id'),
]

certificationTestTrainerForeignKeys: List[ForeignKey] = [
  
]

certificationTestTrainerChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('certification_test_trainer_change_history', 'certification_test_trainer_id', 'certification_test_trainer', 'id'),
    ForeignKey('certification_test_trainer_change_history', 'user_id', 'user', 'id'),
]

cityPostalCodeForeignKeys: List[ForeignKey] = [
    ForeignKey('city_postal_code', 'city_id', 'city', 'id'),
    ForeignKey('city_postal_code', 'postal_code_id', 'postal_code', 'id'),
]

cityRegionForeignKeys: List[ForeignKey] = [
    ForeignKey('city_region', 'city_id', 'city', 'id'),
    ForeignKey('city_region', 'region_id', 'region', 'id'),
]

cityForeignKeys: List[ForeignKey] = [
  
]

companyChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('company_change_history', 'company_id', 'company', 'id'),
    ForeignKey('company_change_history', 'user_id', 'user', 'id'),
]

companyForeignKeys: List[ForeignKey] = [
    ForeignKey('company', 'address_id', 'address', 'id'),
    ForeignKey('company', 'phone_id', 'phone', 'id'),
    ForeignKey('company', 'fax_id', 'fax', 'id'),
]

countryForeignKeys: List[ForeignKey] = [
  
]

customerChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('customer_change_history', 'customer_id', 'customer', 'id'),
    ForeignKey('customer_change_history', 'user_id', 'user', 'id'),
]

customerDefaultAssessorialForeignKeys: List[ForeignKey] = [
    ForeignKey('customer_default_assessorial', 'customer_id', 'customer', 'id'),
    ForeignKey('customer_default_assessorial', 'assessorial_id', 'assessorial', 'id'),
]

customerForeignKeys: List[ForeignKey] = [
    ForeignKey('customer', 'branch_id', 'branch', 'id'),
    ForeignKey('customer', 'address_id', 'address', 'id'),
    ForeignKey('customer', 'phone_id', 'phone', 'id'),
    ForeignKey('customer', 'default_rate_id', 'rate', 'id'),
]

faxForeignKeys: List[ForeignKey] = [
  
]

holidayForeignKeys: List[ForeignKey] = [
  
]

locationChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('location_change_history', 'location_id', 'location', 'id'),
    ForeignKey('location_change_history', 'user_id', 'user', 'id'),
]

locationDefaultAssessorialForeignKeys: List[ForeignKey] = [
    ForeignKey('location_default_assessorial', 'location_id', 'location', 'id'),
    ForeignKey('location_default_assessorial', 'assessorial_id', 'assessorial', 'id'),
]

locationForeignKeys: List[ForeignKey] = [
    ForeignKey('location', 'branch_id', 'branch', 'id'),
    ForeignKey('location', 'address_id', 'address', 'id'),
    ForeignKey('location', 'aci_id', 'aci_data', 'id'),
    ForeignKey('location', 'contact_phone_id', 'phone', 'id'),
]

orderAssessorialForeignKeys: List[ForeignKey] = [
    ForeignKey('order_assessorial', 'order_id', 'order', 'id'),
    ForeignKey('order_assessorial', 'assessorial_id', 'assessorial', 'id'),
]

orderAttachmentForeignKeys: List[ForeignKey] = [
    ForeignKey('order_attachment', 'order_id', 'order', 'id'),
]

orderChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('order_change_history', 'order_id', 'order', 'id'),
    ForeignKey('order_change_history', 'user_id', 'user', 'id'),
]

orderDimForeignKeys: List[ForeignKey] = [
    ForeignKey('order_dim', 'order_id', 'order', 'id'),
]

orderDriverForeignKeys: List[ForeignKey] = [
    ForeignKey('order_driver', 'order_id', 'order', 'id'),
    ForeignKey('order_driver', 'driver_user_id', 'user', 'id'),
]

orderStatusChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('order_status_change_history', 'order_status_id', 'order_status', 'id'),
    ForeignKey('order_status_change_history', 'user_id', 'user', 'id'),
]

orderStatusForeignKeys: List[ForeignKey] = [
    ForeignKey('order_status', 'branch_id', 'branch', 'id'),
]

orderTypeForeignKeys: List[ForeignKey] = [
  
]

orderForeignKeys: List[ForeignKey] = [
    ForeignKey('order', 'branch_id', 'branch', 'id'),
    ForeignKey('order', 'order_type_id', 'order_type', 'id'),
    ForeignKey('order', 'customer_id', 'customer', 'id'),
    ForeignKey('order', 'agent_id', 'agent', 'id'),
    ForeignKey('order', 'rate_id', 'rate', 'id'),
    ForeignKey('order', 'pu_location_id', 'location', 'id'),
    ForeignKey('order', 'pu_contact_phone_id', 'phone', 'id'),
    ForeignKey('order', 'del_location_id', 'location', 'id'),
    ForeignKey('order', 'del_contact_phone_id', 'phone', 'id'),
    ForeignKey('order', 'status_id', 'order_status', 'id'),
]

overnightMaintenanceHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('overnight_maintenance_history', 'user_id', 'user', 'id'),
]

phoneForeignKeys: List[ForeignKey] = [
  
]

positionChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('position_change_history', 'position_id', 'position', 'id'),
    ForeignKey('position_change_history', 'user_id', 'user', 'id'),
]

positionForeignKeys: List[ForeignKey] = [
    ForeignKey('position', 'branch_id', 'branch', 'id'),
]

postalCodeRegionForeignKeys: List[ForeignKey] = [
    ForeignKey('postal_code_region', 'postal_code_id', 'postal_code', 'id'),
    ForeignKey('postal_code_region', 'region_id', 'region', 'id'),
]

postalCodeForeignKeys: List[ForeignKey] = [
  
]

rateAreaForeignKeys: List[ForeignKey] = [
    ForeignKey('rate_area', 'rate_id', 'rate', 'id'),
]

rateChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('rate_change_history', 'rate_id', 'rate', 'id'),
    ForeignKey('rate_change_history', 'user_id', 'user', 'id'),
]

rateForeignKeys: List[ForeignKey] = [
    ForeignKey('rate', 'branch_id', 'branch', 'id'),
    ForeignKey('rate', 'added_by_user_id', 'user', 'id'),
]

regionForeignKeys: List[ForeignKey] = [
    ForeignKey('region', 'country_id', 'country', 'id'),
]

specialChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('special_change_history', 'special_id', 'special', 'id'),
    ForeignKey('special_change_history', 'user_id', 'user', 'id'),
]

specialForeignKeys: List[ForeignKey] = [
    ForeignKey('special', 'branch_id', 'branch', 'id'),
]

userChangeHistoryForeignKeys: List[ForeignKey] = [
    ForeignKey('user_change_history', 'user_changed_id', 'user', 'id'),
    ForeignKey('user_change_history', 'user_id', 'user', 'id'),
]

userForeignKeys: List[ForeignKey] = [
    ForeignKey('user', 'address_id', 'address', 'id'),
    ForeignKey('user', 'branch_id', 'branch', 'id'),
    ForeignKey('user', 'phone_main_id', 'phone', 'id'),
    ForeignKey('user', 'phone_home_id', 'phone', 'id'),
    ForeignKey('user', 'phone_mobile_id', 'phone', 'id'),
    ForeignKey('user', 'position_id', 'position', 'id'),
]