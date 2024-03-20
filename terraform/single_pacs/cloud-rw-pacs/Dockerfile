FROM orthancteam/orthanc:latest

COPY filter-http.lua /scripts/
COPY anonymize.py /etc/orthanc/

RUN apt update && apt install -yy python3-pydicom
ENV ORTHANC__LUA_SCRIPTS='["/scripts/filter-http.lua"]'
