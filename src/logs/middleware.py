from datetime import datetime

from fastapi import Request

from starlette.middleware.base import BaseHTTPMiddleware

from logs.conflog import async_collection


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print(request)
        print(request.form.__dict__)
        start_time = datetime.now()
        response = await call_next(request)
        end_time = datetime.now()
        process_time = (end_time - start_time).total_seconds()

        # todo1: get user id(email) & masking
        # todo2: get ip address & masking
        # todo3: get request data

        log_data = {
            "method": request.method,
            "url": request.url.path,
            "status_code": response.status_code,
            "process_time": process_time,
            "created_at": start_time,
            # "user_email": ,
            #  "ip_address": ,
            #  "request_data": ,
        }

        await async_collection.insert_one(log_data)
        
        return response

