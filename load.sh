curl --location --request POST 'http://localhost:5000/application' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name":"My new APP",
    "check_interval": 20,
    "check_data":{
    	"method":"POST",
        "endpoint":"http://myapplication.com/check",
    	"headers":"",
    	"body":""
    },
    "expected":{
    	"code": "200",
    	"headers":"",
    	"body":""
    },
    "http_notification":{
    	"method":"POST",
    	"headers":{"Content-Type": "application/json","Authorization": "Bearer 12345678901234567890123456789"},
    	"endpoint":"https://interview-notifier-svc.spotahome.net/api/v1/notification",
    	"body":{"service": "${FAILING_SERVICE}","description": "${FAILING_SERVICE_DESCRIPTION}"
}
    }
}'

curl --location --request POST 'http://localhost:5000/application' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name":"PYCHECKER",
    "check_interval": 40,
    "check_data":{
    	"method":"GET",
        "endpoint":"http://localhost:5000/check",
    	"headers":"",
    	"body":""
    },
    "expected":{
    	"code": "200",
    	"headers":"",
    	"body":""
    },
    "http_notification":{
    	"method":"POST",
    	"headers":{"Content-Type": "application/json","Authorization": "Bearer 12345678901234567890123456789"},
    	"endpoint":"https://interview-notifier-svc.spotahome.net/api/v1/notification",
    	"body":{"service": "${FAILING_SERVICE}","description": "${FAILING_SERVICE_DESCRIPTION}"}
    }
}'

curl --location --request POST 'http://localhost:5000/application' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name":"PYCHECKER_NO_INFO",
    "check_interval": 40,
    "check_data":{
    	"method":"GET",
        "endpoint":"http://localhost:5000/check"
    },
    "expected":{
    	"code": "200"
    },
    "http_notification":{
    	"method":"POST",
    	"headers":{"Content-Type": "application/json","Authorization": "Bearer 12345678901234567890123456789"},
    	"endpoint":"https://interview-notifier-svc.spotahome.net/api/v1/notification",
    	"body":{"service": "${FAILING_SERVICE}","description": "${FAILING_SERVICE_DESCRIPTION}"}
    }
}'


