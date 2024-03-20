from io import BytesIO

from pydicom import dcmread, dcmwrite
from pydicom.filebase import DicomFileLike
import hashlib
import orthanc

# from https://pydicom.github.io/pydicom/stable/auto_examples/memory_dataset.html
def write_dataset_to_bytes(dataset):
    with BytesIO() as buffer:
        memory_dataset = DicomFileLike(buffer)
        dcmwrite(memory_dataset, dataset)
        memory_dataset.seek(0)
        return memory_dataset.read()

def ReceivedInstanceCallback(receivedDicom, origin):
    if origin == orthanc.InstanceOrigin.REST_API:
        orthanc.LogWarning('DICOM instance received from the REST API')
    elif origin == orthanc.InstanceOrigin.DICOM_PROTOCOL:
        orthanc.LogWarning('DICOM instance received from the DICOM protocol')
    
    dataset = dcmread(BytesIO(receivedDicom))

#    if dataset.PatientID.startswith('001-'):
#        orthanc.LogWarning('Discard instance')
#        return orthanc.ReceivedInstanceAction.DISCARD, None

    if dataset.PatientID.startswith('Anon-'):
        orthanc.LogWarning('Store source instance as it is')
        return orthanc.ReceivedInstanceAction.KEEP_AS_IS, None

    else:
        orthanc.LogWarning('Modify the source instance')
        dataset.PatientName = hashlib.sha1(dataset.PatientName.encode("utf-8")).hexdigest() #str(dataset.PatientName).upper()
        dataset.PatientID = 'Anon-' + hashlib.sha1(dataset.PatientID.encode("utf-8")).hexdigest() #dataset.PatientID
        dataset.InstitutionName = "ANONYMIZED INSTITUTION"
        return orthanc.ReceivedInstanceAction.MODIFY, write_dataset_to_bytes(dataset)

orthanc.RegisterReceivedInstanceCallback(ReceivedInstanceCallback)
