# Vendor Management System with Performance Metrics
This repository contains a RESTful API built using Django REST Framework for managing vendors,and purchase orders.

## Prerequisites
- Python (version 3.x recommended)
- Django
- Django REST Framework

# Setup Instructions

## CLone the Repository
- use git command to clone the repo
- git clone https://github.com/Sameeksha-12/vendor_management_system_api.git

## Install Dependencies:
- pip install django
- pip install djangorestframework
- or use the requirements.txt file and run pip install -r requirements.txt
  
## Setup the Database                    
- python manage.py makemigrations      
- python manage.py migrate

## Create Superuser and Generate Token
- python manage.py createsuperuser
- curl -X POST -d "username=your_superuser_username&password=your_superuser_password" http://localhost:8000/api-token-auth/
- Running the above curl command should generate a token which we will further use.

## Running the server
- python manage.py runserver


## Run an API endpoint
- Make sure that you do not have any unmigrated changes.
- Run the server using python manage.py runserver
- Open a new cmd prompt terminal and cd into your project folder

# Testing API endpoints.
- we can test API endpoints using curl commands. 

## Create a vendor:
### using curl:
- curl -H "Authorization: Your_token" -X POST http://127.0.0.1:8000/api/vendors/ -d "vendor_code=vc&name=Vendor_name&contact_details=9999999999&address=India"
### Output of the API endpoint:
- This endpoint creates the vendor

## List all Vendors details:
### using curl:
- curl -H "Authorization: Your_token" http://127.0.0.1:8000/api/vendors/
### Output of this API endpoint:
- This endpoint lists all the vendors along with their details

## Retrieve a specific vendor's details:
### using curl:
- curl -H "Authorization: Your_token" http://127.0.0.1:8000/api/vendors/{vendor_id}/
### Output of this API endpoint:
- This endpoint retrieves the details of vendor with particular vendor_id. 

## Update a vendor's details:
### using curl:
#### PUT method:
- curl -H "Authorization: Your_token" -X PUT http://127.0.0.1:8000/api/vendors/{vendor_id}/ -d "vendor_code=updated_code&name=Updated_Vendor_Name&contact_details=Updated_Contact_Details&address=Updated_Address"
#### PATCH method:
- curl -H "Authorization: Your_token" -X PATCH http://127.0.0.1:8000/api/vendors/{vendor_id}/ -d "name=updated_vendor_name"
- you may change any attribute not just name
### Output of this API endpoint:
- This API endpoint utilizes the PATCH method to update the vendor's details while excluding the vendor's ID.
-  Unlike the PUT method, which replaces the entire entity and creates a new one, PATCH specifically updates only the provided fields, allowing for partial updates.

## Delete a vendor:
### using curl:
- curl -H "Authorization: your_token" -X DELETE http://127.0.0.1:8000/api/vendors/{vendor_id}/
### Output of this API endpoint:
- This endpoint deletes the vendor with given vendor_id.

## Create a purchase_order:
### using curl:
- curl -H "Authorization: your_token" -X POST http://127.0.0.1:8000/api/purchase_orders/ -d "vendor=04&order_date=2024-05-01T12:00:00&delivery_date=2024-05-10T12:00:00&items=[{\"name\":\"Item 5\",\"price\":20,\"quantity\":30}]&issue_date=2024-01-02T12:00:00&quantity=10"
### Output of this API endpoint:
- This endpoint is used to create a purchase_order with given details.

## List all purchase_orders details:
### using curl:
- curl -H "Authorization: your_token" http://127.0.0.1:8000/api/purchase_orders/
### Output of this API endpoint:
- This endpoint lists all the purchase_orders along with the details.

## Retrieve a specific purchase_order's details:
### using curl:
- curl -H "Authorization: your_token" http://127.0.0.1:8000/api/purchase_orders/{po_id}/
### Output of this API endpoint:
- This endpoint retrieves the particular purchase_order with the given id along with its details.

## Update a purchase_order's details:
### using curl:
#### PUT method:
- curl -H "Authorization: your_token" -X PUT http://127.0.0.1:8000/api/purchase_orders/{po_id}/ -d "vendor=04&order_date=2024-05-01T12:00:00&delivery_date=2024-05-10T12:00:00&items=[{\"name\":\"Item 5\",\"price\":20,\"quantity\":30}]&issue_date=2024-01-02T12:00:00&quantity=10"
- - use all the updated details here and you may also add status,delivered_date,quality_rating attibutes when the order is completed.Or you may use patch to partial updations.
#### PATCH method:
- curl -H "Authorization: Token your_obtained_token" -X PATCH http://127.0.0.1:8000/api/purchase_orders/{po_id}/ -d "status=completed&quality_rating=5&delivered_date=2024-05-06T12:00:00"
### Output of this API endpoint:
- PUT handles updates by replacing the entire entity, so it creates a new entity.PATCH handles by only updating the given fields.(we can provide any no of fields in PATCH method.)

## Delete a purchase_order:
### using curl:
- curl -H "Authorization: your_token" -X DELETE http://127.0.0.1:8000/api/purchase_orders/{po_id}/
### Output of this API endpoint:
- This endpoint is used to delete a purchase_order with given po_id.

## Retrieve a vendor's performance metrics:
### using curl:
- curl -H "Authorization: Token your_obtained_token" http://127.0.0.1:8000/api/vendors/{vendor_id}/performance/
### About this API endpoint:
- This endpoint retrieves the performance metrics for a vendor based on the provided vendor ID. These metrics include the on-time delivery rate, average quality rating, average response time, and fulfillment rate.
- The on-time delivery rate is determined each time a purchase order (PO) status transitions to "completed". It represents the percentage of POs delivered before their specified delivery date out of the total completed POs.
- The average quality rating is calculated whenever a quality_rating is assigned to the vendor. It represents the average rating given to the vendor across all POs.
- The average response time is computed whenever a purchase order is acknowledged by the vendor. It reflects the average duration between the issue date and acknowledgment date for all POs assigned to the vendor.
- The fulfillment rate is computed when a purchase order's status is updated to "completed". It indicates the percentage of successfully fulfilled POs (i.e., those with a status of "completed" without any issues) out of the total number of POs issued to the vendor.

## Acknowledging a PO and recalculating the average_response_time:
### using curl:
- curl -H "Authorization: your_token" -X POST http://127.0.0.1:8000/api/purchase_orders/{po_id}/acknowledge/ 
### Output of this API endpoint:
- Whenever this endpoint is hit, the current date and time will be assigned as the acknowledgement_date to the po and the average_response_time is recalculated
- We may retrieve the particular po and vendor details to verify if the response_time and acknowledgement_date have changed.

# Running the tests:
- cd into the project directory
- run 'python manage.py test'
