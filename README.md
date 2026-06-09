# huaweicloud-obs-delete-marker-object-restoration
This repository is home to a script that automatically scans the target OBS bucket and restores all objects with the <code>delete marker</code> set.

## FunctionGraph
In order to run the script, it is necessary to create a <a href="https://support.huaweicloud.com/eu/usermanual-functiongraph/functiongraph_01_1441.html">FunctionGraph</a> function on Huawei Cloud first and foremost. The runtime is <code>Python3.9</code> and the function is <code>Event-Based</code>. The <code>agency</code> should have at least the following permissions:

```json
{
    "Version": "1.1",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "obs:object:GetObject",
                "obs:object:DeleteObjectVersion",
                "obs:bucket:ListAllMyBuckets",
                "obs:bucket:ListBucketVersions",
                "obs:bucket:ListBucket",
                "obs:object:GetObjectVersion"
            ]
        }
    ]
}
```
Once created, the following parameters must be configured:

### Dependencies
Import the dependency <code>esdk_obs_python-3.22.2_python39</code>.

### Environment Variables
Configure the following environment variables for the function:
<ul>
  <li><code>region</code>: <a href="https://support.huaweicloud.com/intl/en-us/usermanual-organizations/org_03_0082.html">Region code</a> where the OBS bucket has been created;</li>
  <li><code>bucket_name</code>: Name of the target OBS bucket;</li>
  <li><code>page_size</code>: Defaults to 1000. It is the number of objects that can be retrieved by a single <code>listObjects</code> API call.</li>
</ul>

### (Optional) Execution Timeout (s)
Even though it is not a mandatory parameter modification, if the OBS bucket has a massive amount of objects, there is a risk of function timeout. It is suggested to increase the execution timeout. 

### (Optional) Memory (MB)
Even though it is not a mandatory parameter modification, if the OBS bucket has a massive amount of objects, there is a risk of memory overflow. It is suggested to increase the function memory.
