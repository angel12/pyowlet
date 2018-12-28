# Owlet Unnoficial API Protocol

This document describes the Owlet Unnoficial API protocol used for communicating
with the Harmony Link device.

## Owlet Device

The Owlet connects to your home wireless network and reports information to the Ayla Networks IOT cloud

## Authentication

### Obtaining Authentication Token

The first step in authenticating is sending an Owlet username and password to
an Ayla Networks web service. The endpoint for getting an authentication token is:

    https://user-field.aylanetworks.com/users/sign_in.json

A POST request is sent to this URL with a payload of JSON. The `Content-Type` and 'Accept' 
request header must be set to `application/json` and the body of
the request should contain JSON like this:

    {
      "user": {
        "email": "email",
        "password": "password",
        "application": {
          "app_id": "OWL-id",
          "app_secret": "OWL-4163742"
        }
      }
    }

The response will also be JSON of the form:

    {
        "access_token": "access token",
        "refresh_token": "refresh token",
        "expires_in": 86400,
        "role": "EndUser",
        "role_tags": []
    }

The access token is then used in every step after this as the 'Authorization' header. It is only valid for 24 hours. 

### DSN Number

Now we need to get the list of devices tied to the account in order to get the DSN (Assuming it means Device Serial Number). 
Another post request is made, this time to: 

    https://ads-field.aylanetworks.com/apiv1/devices.json

A POST request is sent to this URL with a payload of JSON. The `Content-Type` and 'Accept' 
request header must be set to `application/json`,  as well as the 'Authorization' header set to '(access token)'.
This will return JSON as well, and should look like this:

	[
        {
            "device": {
                "product_name": "Owlet Baby Monitors",
                "model": "model",
                "dsn": "ab123456789012345",
                "oem_model": "BabyOwl",
                "sw_version": "version",
                "template_id": 0000,
                "mac": "mac",
                "unique_hardware_id": null,
                "hwsig": "sigmac",
                "lan_ip": "IP",
                "connected_at": "date/time",
                "key": 12345678,
                "lan_enabled": false,
                "has_properties": true,
                "product_class": null,
                "connection_status": "Offline",
                "lat": "lat",
                "lng": "lng",
                "locality": "zip",
                "device_type": "Wifi"
            }
        }
    ]

The DSN is used when polling the data URL to get measurements.

## Getting Measurements

Once you have both the access token and the dsn for the device you are trying to get data from, you can actually request that data. 
The request is sent in the form of a GET to:
    https://ads-field.aylanetworks.com/apiv1/dsns/(dsn)/properties.json

Notice the (dsn) in the url, this needs to be replaced with the dsn that you are trying to request information from. The request
must also contain a payload of JSON: The `Content-Type` and 'Accept' request header must be set to `application/json`,  
as well as the 'Authorization' header set to '(access token)'.

The results will be in JSON, and should look like this (with an entry for each Property Name, listed below):

	[
        {
            "property": {
                "type": "Property",
                "name": "AGE_MONTHS_OLD",
                "base_type": "integer",
                "read_only": false,
                "direction": "input",
                "scope": "user",
                "data_updated_at": "null",
                "key": 12345678,
                "device_key": 12345678,
                "product_name": "Owlet Baby Monitors",
                "track_only_changes": true,
                "display_name": "Age (Months)",
                "host_sw_version": false,
                "time_series": false,
                "derived": false,
                "app_type": null,
                "recipe": null,
                "value": null,
                "denied_roles": [],
                "ack_enabled": false,
                "retention_days": 30
            }
        },

The Properties listed in the results are:

	AGE_MONTHS_OLD
    ALRTS_DISABLED
    ALRT_SNS_BLE
    ALRT_SNS_YLW
    APP_ACTIVE
    AVERAGE_DATA
    BABY_NAME
    BASE_STATION_ON
    BATT_LEVEL
    BIRTHDATE
    BLE_MAC_ID
    BLE_RSSI
    CHARGE_STATUS
    CRIT_BATT_ALRT
    CRIT_OX_ALRT
    DEVICE_PING
    DISABLE_LOGGED_DATA
    ELEVATION
    GENDER
    HEART_RATE
    HIGH_HR_ALRT
    LATITUDE
    LIVE_DATA_STREAM
    LOCAL_BLE_MAC_ID
    LOGGED_DATA_CACHE
    LONGITUDE
    LOW_BATT_ALRT
    LOW_BATT_PRCNT
    LOW_HR_ALRT
    LOW_INTEG_READ
    LOW_OX_ALRT
    LOW_PA_ALRT
    MOVEMENT
    NURSERY_MODE
    oem_base_version
    oem_sock_version
    ON_BOARDING
    OTA_ERROR
    OTA_STATUS
    OXYGEN_LEVEL
    PREMATURE
    SHARE_DATA
    SOCK_CONNECTION
    SOCK_DISCON_ALRT
    SOCK_DIS_APP_PREF
    SOCK_DIS_NEST_PREF
    SOCK_OFF
    SOCK_REC_PLACED

The main properties I was concerned with were: 

	OXYGEN_LEVEL
    HEART_RATE
    BASE_STATION_ON
    BATT_LEVEL
    MOVEMENT
    SOCK_OFF
    CHARGE_STATUS
    BABY_NAME
    SOCK_CONNECTION
	
The value field is what will show the measurement that we are looking for. This documentation is still a work in progress, and I 
owe everything found here to the following projects:

https://github.com/bobcat0070/python-owlet
https://github.com/tescalada/python-owlet (forked from above with some minor changes)
https://github.com/arosequist/node-owlet