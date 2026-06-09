# -*- coding:utf-8 -*-
# Owner: Diogo Lourenzon Hatz

from obs import ObsClient, Object, DeleteObjectsRequest, Versions

def queryDeleteMarkerObjects(client, bucketName, pageSize):
    objectList = []
 
    nextKeyMarker = None
    nextVersionIdMarker = None
    index = 1

    while True:
        resp = client.listVersions(bucketName, Versions(key_marker=nextKeyMarker, version_id_marker=nextVersionIdMarker,
                                                           max_keys=pageSize))
        print('Page:' + str(index) + '\n')
        for version in resp.body.markers:
            print('\t' + version.key + ' versionId[' + version.versionId + ']')
            objectList.append(Object(version.key, version.versionId))

        if not resp.body.head.isTruncated:
            break

        nextKeyMarker = resp.body.head.nextKeyMarker
        nextVersionIdMarker = resp.body.head.nextVersionIdMarker
        index += 1
    
    return objectList


def deleteDeleteMarkerObjects(client, bucketName, objectList):
    startIndex = 0
    endIndex = 0

    while(startIndex < len(objectList)):
        endIndex = len(objectList) if (endIndex + 1000) > len(objectList) else endIndex + 1000

        resp = client.deleteObjects(bucketName, DeleteObjectsRequest(False, objectList[startIndex:endIndex]))

        print('Deleted Successfully:')
        if resp.body.deleted:
            for delete in resp.body.deleted:
                print('\t' + str(delete))

        print('Deleted Failed:')
        if resp.body.error:
            for err in resp.body.error:
                print('\t' + str(err))

        startIndex = endIndex


def handler (event, context):
    ak = context.getSecurityAccessKey()
    sk = context.getSecuritySecretKey()
    st = context.getSecurityToken()

    region = context.getUserData("region")
    bucketName = context.getUserData("bucket_name")
    pageSize = context.getUserData("page_size")
    endpoint = f"https://obs.{region}.myhuaweicloud.com"
 
    client = ObsClient(access_key_id=ak, secret_access_key=sk, security_token=st, server=endpoint)
 
    objectList = queryDeleteMarkerObjects(client, bucketName, pageSize)
    deleteDeleteMarkerObjects(client, bucketName, objectList)
