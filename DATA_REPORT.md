Task 1 – Data Understanding (Documentation)
In this README.md (or a separate DATA_REPORT.md if you prefer), briefly describe:

1 - The main entities in the dataset (see data/ folder).
2 - Data Quality: Identify issues such as missing values, duplicates, or inconsistent formatting (e.g., location names).
3 - Schema: Explain how you handled the payload field in the events table (Note: It contains JSON data).
4 - Assumptions you had to make.
------------------------------------------------------------------------------------------------------------------------- 

1- use cases extract from data provided

### users:
- there is one user_id duplicated

### devices:
- each user assign to one user
- each user can be assigned one or more devices
- 25 devices are not assigned to any users (missing values)
- 108 devices are undefined location

### events:
- each event is assigned to one device on one specific date-time
- all events' types are "telemetry"
- all events' values are based on a JSON document data stored in "payload"
- each event's data (payload) includes "metadata" or "status"
- device_id = "d_f4abcb9e" has 1517 events, which is "unusually high"


### data structure for creating tables:
### users:		
- user_id    - 	string     (PK)  	(found one duplicate value)
- signup_date 	 datetime      -    	    (sign up date)
- region   	  string or enum 	 (the region signed up from)
- platform   	string or enum 	 (the platform signed up from)

### devices:   		
- device_id  	 string  (PK)  	combined columns primary key
- user_id      	 string  (PK)  	(found some missing values)
- network       	 string   	 (local area network)
- device_type   	 string   	(smart devices which connect through the network) 
- firmware_version 	string    	(the version of embedded software involved hardware) 
- location       	string    	(location where connected to the network)

### events		
- event_id   	string (PK)	
- device_id   	string   	 (the device that connects through a network)
- event_type  	string   	 (all are telemetry)
- event_value  	string	(points to payload)
- event_ts   	datetime  	(date and time of connect)
- payload    	string   	 (a JSON document which includes metadata or connection status)



